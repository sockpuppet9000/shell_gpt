from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Callable, Dict, Optional

import requests


DEFAULT_CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
DEFAULT_ISSUER = "https://auth.openai.com"
DEFAULT_PORT = 1455
LOGIN_TIMEOUT = 15 * 60


@dataclass
class TokenBundle:
    id_token: str
    access_token: str
    refresh_token: str
    account_id: Optional[str] = None


@dataclass
class AuthRecord:
    openai_api_key: Optional[str]
    tokens: Optional[TokenBundle]
    last_refresh: Optional[datetime]


def _codex_home() -> Path:
    return Path(os.getenv("CODEX_HOME", "~/.codex")).expanduser()


def _auth_file() -> Path:
    return _codex_home() / "auth.json"


def _read_sgpt_rc() -> Optional[str]:
    rc = Path(os.path.expanduser("~/.config/shell_gpt/.sgptrc"))
    if not rc.exists():
        return None
    try:
        for line in rc.read_text().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("OPENAI_API_KEY="):
                return stripped.split("=", 1)[1].strip()
    except Exception:
        return None
    return None


def _ensure_parent(path: Path) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def _load_auth_record() -> Optional[AuthRecord]:
    path = _auth_file()
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text())
    except Exception:
        return None

    api_key = raw.get("OPENAI_API_KEY") or raw.get("openai_api_key")

    tokens_data = raw.get("tokens")
    tokens: Optional[TokenBundle]
    if isinstance(tokens_data, dict):
        tokens = TokenBundle(
            id_token=str(tokens_data.get("id_token", "")),
            access_token=str(tokens_data.get("access_token", "")),
            refresh_token=str(tokens_data.get("refresh_token", "")),
            account_id=(
                str(tokens_data.get("account_id"))
                if tokens_data.get("account_id") is not None
                else None
            ),
        )
    else:
        tokens = None

    last_refresh_raw = raw.get("last_refresh")
    last_refresh: Optional[datetime]
    if isinstance(last_refresh_raw, str):
        try:
            last_refresh = datetime.fromisoformat(last_refresh_raw.replace("Z", "+00:00"))
        except ValueError:
            last_refresh = None
    else:
        last_refresh = None

    return AuthRecord(api_key, tokens, last_refresh)


def _write_auth_record(record: AuthRecord) -> None:
    path = _auth_file()
    _ensure_parent(path)

    payload: Dict[str, object] = {
        "OPENAI_API_KEY": record.openai_api_key,
        "tokens": None,
        "last_refresh": record.last_refresh.isoformat().replace("+00:00", "Z")
        if record.last_refresh
        else None,
    }

    if record.tokens:
        payload["tokens"] = {
            "id_token": record.tokens.id_token,
            "access_token": record.tokens.access_token,
            "refresh_token": record.tokens.refresh_token,
            "account_id": record.tokens.account_id,
        }

    with path.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2)
        fp.write("\n")

    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def discover_openai_api_key() -> Optional[str]:
    env = os.getenv("OPENAI_API_KEY")
    if env:
        return env

    rc_value = _read_sgpt_rc()
    if rc_value:
        return rc_value

    record = _load_auth_record()
    if not record:
        return None

    if record.openai_api_key:
        return record.openai_api_key

    if record.tokens and record.tokens.id_token:
        try:
            api_key = obtain_api_key(DEFAULT_ISSUER, DEFAULT_CLIENT_ID, record.tokens.id_token)
        except Exception:
            return None

        updated = AuthRecord(
            openai_api_key=api_key,
            tokens=record.tokens,
            last_refresh=datetime.now(timezone.utc),
        )
        try:
            _write_auth_record(updated)
        except Exception:
            pass
        return api_key

    return None


def ensure_env_api_key() -> None:
    if "OPENAI_API_KEY" in os.environ:
        return
    key = discover_openai_api_key()
    if key:
        os.environ["OPENAI_API_KEY"] = key


def _urlsafe_b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _generate_pkce() -> tuple[str, str]:
    verifier = _urlsafe_b64(secrets.token_bytes(64))
    challenge = _urlsafe_b64(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def _generate_state() -> str:
    return _urlsafe_b64(secrets.token_bytes(32))


def _build_authorize_url(
    issuer: str,
    client_id: str,
    redirect_uri: str,
    code_challenge: str,
    state: str,
) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email offline_access",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "id_token_add_organizations": "true",
        "codex_cli_simplified_flow": "true",
        "state": state,
    }
    query = urllib.parse.urlencode(params)
    return f"{issuer.rstrip('/')}/oauth/authorize?{query}"


def exchange_code_for_tokens(
    issuer: str,
    client_id: str,
    redirect_uri: str,
    code_verifier: str,
    code: str,
) -> TokenBundle:
    response = requests.post(
        f"{issuer.rstrip('/')}/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=urllib.parse.urlencode(
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "code_verifier": code_verifier,
            }
        ),
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"Token endpoint returned status {response.status_code}: {response.text}"
        )

    data = response.json()
    id_token = data.get("id_token")
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    if not (id_token and access_token and refresh_token):
        raise RuntimeError("Token response missing required fields")

    account_id = _extract_account_id(id_token)
    return TokenBundle(id_token=id_token, access_token=access_token, refresh_token=refresh_token, account_id=account_id)


def _extract_account_id(id_token: str) -> Optional[str]:
    try:
        parts = id_token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        padding = "=" * (-len(payload) % 4)
        payload_json = base64.urlsafe_b64decode(payload + padding)
        parsed = json.loads(payload_json)
        auth_section = parsed.get("https://api.openai.com/auth")
        if isinstance(auth_section, dict):
            account = auth_section.get("chatgpt_account_id")
            if isinstance(account, str):
                return account
    except Exception:
        return None
    return None


def obtain_api_key(issuer: str, client_id: str, id_token: str) -> str:
    payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "client_id": client_id,
        "requested_token": "openai-api-key",
        "subject_token": id_token,
        "subject_token_type": "urn:ietf:params:oauth:token-type:id_token",
    }

    response = requests.post(
        f"{issuer.rstrip('/')}/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=urllib.parse.urlencode(payload),
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"API key exchange failed with status {response.status_code}: {response.text}"
        )

    data = response.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError("API key exchange response missing access_token")
    return str(token)


def refresh_tokens(issuer: str, client_id: str, refresh_token: str) -> TokenBundle:
    response = requests.post(
        f"{issuer.rstrip('/')}/oauth/token",
        headers={"Content-Type": "application/json"},
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
        },
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"Failed to refresh token: {response.status_code}: {response.text}"
        )

    data = response.json()
    id_token = data.get("id_token")
    access_token = data.get("access_token")
    new_refresh = data.get("refresh_token", refresh_token)
    if not (id_token and access_token and new_refresh):
        raise RuntimeError("Refresh response missing required fields")

    account_id = _extract_account_id(id_token)
    return TokenBundle(
        id_token=id_token,
        access_token=access_token,
        refresh_token=new_refresh,
        account_id=account_id,
    )


class _LoginContext:
    def __init__(
        self,
        *,
        issuer: str,
        client_id: str,
        redirect_uri: str,
        code_verifier: str,
        state: str,
    ) -> None:
        self.issuer = issuer
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.code_verifier = code_verifier
        self.state = state
        self.event = threading.Event()
        self.error: Optional[str] = None
        self.tokens: Optional[TokenBundle] = None
        self.api_key: Optional[str] = None
        self.success = False


def _handler_factory(context: _LoginContext) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args) -> None:  # noqa: A003 - signature fixed by BaseHTTPRequestHandler
            return

        def do_GET(self) -> None:  # noqa: N802 - inherited name
            parsed = urllib.parse.urlsplit(self.path)
            path = parsed.path

            if path == "/auth/callback":
                params = dict(urllib.parse.parse_qsl(parsed.query))
                if params.get("state") != context.state:
                    self._respond(400, "State mismatch")
                    context.error = "OAuth state mismatch"
                    context.event.set()
                    return

                code = params.get("code")
                if not code:
                    self._respond(400, "Missing authorization code")
                    context.error = "Authorization code missing"
                    context.event.set()
                    return

                try:
                    tokens = exchange_code_for_tokens(
                        context.issuer,
                        context.client_id,
                        context.redirect_uri,
                        context.code_verifier,
                        code,
                    )
                    api_key = obtain_api_key(context.issuer, context.client_id, tokens.id_token)
                    record = AuthRecord(
                        openai_api_key=api_key,
                        tokens=tokens,
                        last_refresh=datetime.now(timezone.utc),
                    )
                    _write_auth_record(record)
                except Exception as exc:  # pragma: no cover - network errors hard to emulate in tests
                    message = f"Login failed: {exc}"
                    context.error = message
                    self._respond(500, message)
                    context.event.set()
                    return

                context.tokens = tokens
                context.api_key = api_key
                context.success = True
                self.send_response(302)
                self.send_header("Location", f"http://localhost:{self.server.server_address[1]}/success")
                self.end_headers()
                context.event.set()
                return

            if path == "/success":
                self._respond(200, _SUCCESS_HTML, content_type="text/html; charset=utf-8")
                context.event.set()
                return

            if path == "/cancel":
                context.error = "Login cancelled"
                context.event.set()
                self._respond(200, "Login cancelled")
                return

            self._respond(404, "Not Found")

        def _respond(self, status: int, body: str, *, content_type: str = "text/plain; charset=utf-8") -> None:
            encoded = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    return Handler


_SUCCESS_HTML = """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <title>Shell GPT Login</title>
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 2rem; }
      .card { max-width: 520px; margin: 0 auto; padding: 2rem; border-radius: 1rem; background: #f5f5f7; box-shadow: 0 12px 32px rgba(15, 15, 15, 0.12); }
      h1 { margin-top: 0; font-size: 1.8rem; }
      p { color: #1f1f24; line-height: 1.5; }
    </style>
  </head>
  <body>
    <div class=\"card\">
      <h1>You're all set!</h1>
      <p>Return to your terminal to continue using Shell GPT.</p>
    </div>
  </body>
</html>
"""


def perform_login(
    *,
    open_browser: bool = True,
    port: Optional[int] = DEFAULT_PORT,
    issuer: str = DEFAULT_ISSUER,
    client_id: str = DEFAULT_CLIENT_ID,
    echo: Callable[[str], None] = print,
) -> bool:
    verifier, challenge = _generate_pkce()
    state = _generate_state()

    # Bind server and capture actual port.
    bound_port = port or DEFAULT_PORT
    server: Optional[HTTPServer] = None
    context = _LoginContext(
        issuer=issuer,
        client_id=client_id,
        redirect_uri=f"http://localhost:{bound_port}/auth/callback",
        code_verifier=verifier,
        state=state,
    )
    for attempt in range(2):
        try:
            server = HTTPServer(("127.0.0.1", bound_port), _handler_factory(context))
            break
        except OSError:
            if attempt == 0:
                bound_port = 0
                context.redirect_uri = "http://localhost:0/auth/callback"
                continue
            raise

    assert server is not None  # For mypy/static checkers
    actual_port = server.server_address[1]
    context.redirect_uri = f"http://localhost:{actual_port}/auth/callback"

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    authorize_url = _build_authorize_url(
        issuer,
        client_id,
        context.redirect_uri,
        challenge,
        state,
    )

    echo(
        "Starting browser-based login. If the browser does not open, copy the URL below and paste it into the address bar:\n"
    )
    echo(f"  {authorize_url}\n")

    if open_browser:
        try:
            webbrowser.open(authorize_url)
        except Exception:
            echo("Unable to open the browser automatically. Please open the URL manually.")

    echo("Waiting for authorization...")

    start_time = time.monotonic()
    success = False
    try:
        while True:
            remaining = LOGIN_TIMEOUT - (time.monotonic() - start_time)
            if remaining <= 0:
                context.error = "Login timed out after 15 minutes"
                break
            if context.event.wait(timeout=min(1.0, remaining)):
                success = context.success
                break
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

    if success:
        echo("Login successful. Credentials saved to Codex auth.json.")
        ensure_env_api_key()
        return True

    if context.error:
        echo(context.error)
    else:
        echo("Login did not complete.")
    return False

