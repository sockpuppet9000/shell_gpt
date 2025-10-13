from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional


def _read_sgpt_rc() -> Optional[str]:
    rc = Path(os.path.expanduser("~/.config/shell_gpt/.sgptrc"))
    if not rc.exists():
        return None
    try:
        for line in rc.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None


def _read_codex_auth_json() -> Optional[str]:
    codex_home = Path(os.getenv("CODEX_HOME", "~/.codex")).expanduser()
    auth_path = codex_home / "auth.json"
    if not auth_path.exists():
        return None
    try:
        data = json.loads(auth_path.read_text())
        # ChatGPT plan logins record OAuth tokens instead of an API key, so the
        # OPENAI_API_KEY field is only present when Codex has an actual key to
        # reuse (for example, after piping a usage-based API key via
        # `codex login --with-api-key`).
        return data.get("OPENAI_API_KEY") or data.get("openai_api_key")
    except Exception:
        return None


def discover_openai_api_key() -> Optional[str]:
    value = os.getenv("OPENAI_API_KEY")
    if value:
        return value

    value = _read_sgpt_rc()
    if value:
        return value

    return _read_codex_auth_json()
