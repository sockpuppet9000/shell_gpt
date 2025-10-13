from __future__ import annotations

import json
import base64
from datetime import datetime, timezone
from typing import Any

import pytest

from sgpt.codex_auth import (
    AuthRecord,
    TokenBundle,
    exchange_code_for_tokens,
    obtain_api_key,
    refresh_tokens,
)
from sgpt.codex_auth import _extract_account_id, _load_auth_record, _write_auth_record


class _Response:
    def __init__(self, status_code: int, payload: Any) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload)

    def json(self) -> Any:
        return self._payload


def _patch_post(monkeypatch, status: int, payload: Any) -> None:
    def _fake_post(*_args, **_kwargs):
        return _Response(status, payload)

    monkeypatch.setattr("sgpt.codex_auth.requests.post", _fake_post)


def test_exchange_code_for_tokens(monkeypatch):
    payload = {
        "id_token": "header.payload.signature",
        "access_token": "access",
        "refresh_token": "refresh",
    }
    _patch_post(monkeypatch, 200, payload)
    result = exchange_code_for_tokens(
        "https://issuer",
        "client",
        "http://localhost/callback",
        "verifier",
        "code",
    )
    assert isinstance(result, TokenBundle)
    assert result.id_token == payload["id_token"]
    assert result.refresh_token == payload["refresh_token"]


def test_exchange_code_for_tokens_error(monkeypatch):
    _patch_post(monkeypatch, 500, {"error": "boom"})
    with pytest.raises(RuntimeError):
        exchange_code_for_tokens(
            "https://issuer",
            "client",
            "http://localhost/callback",
            "verifier",
            "code",
        )


def test_obtain_api_key(monkeypatch):
    _patch_post(monkeypatch, 200, {"access_token": "sk-live"})
    token = obtain_api_key("https://issuer", "client", "id-token")
    assert token == "sk-live"


def test_obtain_api_key_error(monkeypatch):
    _patch_post(monkeypatch, 403, {"error": "denied"})
    with pytest.raises(RuntimeError):
        obtain_api_key("https://issuer", "client", "id-token")


def test_refresh_tokens(monkeypatch):
    payload = {
        "id_token": "header.payload.signature",
        "access_token": "new-access",
        "refresh_token": "new-refresh",
    }
    _patch_post(monkeypatch, 200, payload)
    bundle = refresh_tokens("https://issuer", "client", "old-refresh")
    assert bundle.access_token == "new-access"
    assert bundle.refresh_token == "new-refresh"


def test_refresh_tokens_missing_refresh(monkeypatch):
    payload = {
        "id_token": "header.payload.signature",
        "access_token": "new-access",
    }
    _patch_post(monkeypatch, 200, payload)
    bundle = refresh_tokens("https://issuer", "client", "old-refresh")
    assert bundle.refresh_token == "old-refresh"


def test_extract_account_id():
    header = json.dumps({"alg": "none", "typ": "JWT"}).encode()
    payload = json.dumps(
        {
            "https://api.openai.com/auth": {
                "chatgpt_account_id": "account-123",
            }
        }
    ).encode()
    token = ".".join(
        (
            base64.urlsafe_b64encode(header).decode().rstrip("="),
            base64.urlsafe_b64encode(payload).decode().rstrip("="),
            "sig",
        )
    )
    assert _extract_account_id(token) == "account-123"


def test_write_and_load_auth_record(monkeypatch, tmp_path):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    record = AuthRecord(
        openai_api_key="sk-test",
        tokens=TokenBundle(
            id_token="header.payload.signature",
            access_token="access",
            refresh_token="refresh",
            account_id="account-123",
        ),
        last_refresh=datetime.now(timezone.utc),
    )
    _write_auth_record(record)
    loaded = _load_auth_record()
    assert loaded is not None
    assert loaded.openai_api_key == "sk-test"
    assert loaded.tokens and loaded.tokens.account_id == "account-123"

