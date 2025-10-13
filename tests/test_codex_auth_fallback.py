from __future__ import annotations

import json
from pathlib import Path

from sgpt.auth_fallback import discover_openai_api_key


def _write_sgpt_rc(home: Path, value: str) -> None:
    config_dir = home / ".config" / "shell_gpt"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / ".sgptrc").write_text(f"OPENAI_API_KEY={value}\n")


def _write_codex_auth(codex_home: Path, key: str) -> None:
    codex_home.mkdir(parents=True, exist_ok=True)
    (codex_home / "auth.json").write_text(json.dumps({"OPENAI_API_KEY": key}))


def test_env_precedence(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    _write_sgpt_rc(tmp_path, "rc-key")
    _write_codex_auth(tmp_path / "codex", "codex-key")

    assert discover_openai_api_key() == "env-key"


def test_sgpt_config_precedence(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    _write_sgpt_rc(tmp_path, "rc-key")
    _write_codex_auth(tmp_path / "codex", "codex-key")

    assert discover_openai_api_key() == "rc-key"


def test_codex_fallback(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    codex_home = tmp_path / "codex"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    _write_codex_auth(codex_home, "codex-key")

    assert discover_openai_api_key() == "codex-key"


def test_malformed_codex_json(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    codex_home = tmp_path / "codex"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    codex_home.mkdir(parents=True, exist_ok=True)
    (codex_home / "auth.json").write_text("not-json")

    assert discover_openai_api_key() is None
