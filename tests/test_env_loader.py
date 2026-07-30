"""Tests for the deterministic ``.env`` discovery and loading in ``env_loader``.

Each test isolates the loader by clearing the ``lru_cache`` and controlling
``HOME``, ``PWD``, and the process environment via ``monkeypatch``.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from cloudflare_browser_render.utils import env_loader
from cloudflare_browser_render.utils.env_loader import EnvLoadResult, load_project_env

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_loader():
    """Clear the lru_cache and restore a clean process environment per test."""
    load_project_env.cache_clear()
    saved_environ = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(saved_environ)
    load_project_env.cache_clear()


def _make_env(home: Path, *rel_parts: str) -> Path:
    """Create a ``.env`` file at ``home / rel_parts``.

    Returns:
        The path to the created file.
    """
    path = home.joinpath(*rel_parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _write_env(path: Path, content: str) -> None:
    path.write_text(content)


# ---------------------------------------------------------------------------
# 1. Absent file
# ---------------------------------------------------------------------------


def test__load_project_env__no_file_returns_not_loaded(tmp_path, monkeypatch):
    """When no .env file exists, loaded is False and path is None."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    result = load_project_env()
    assert result.loaded is False
    assert result.path is None
    assert result.key_count == len(os.environ)


# ---------------------------------------------------------------------------
# 2. Each location
# ---------------------------------------------------------------------------


def test__load_project_env__loads_from_xdg_config_dir(tmp_path, monkeypatch):
    """File at ~/.config/cloudflare-browser-rendering-cli/.env is loaded."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = _make_env(
        tmp_path, ".config", "cloudflare-browser-rendering-cli", ".env"
    )
    _write_env(env_file, "TEST_VAR_XDG=xdg_value\n")
    result = load_project_env()
    assert result.loaded is True
    assert result.path == env_file
    assert result.env.get("TEST_VAR_XDG") == "xdg_value"


def test__load_project_env__loads_from_short_config_dir(tmp_path, monkeypatch):
    """File at ~/.config/cbr/.env is loaded when the long dir is absent."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = _make_env(tmp_path, ".config", "cbr", ".env")
    _write_env(env_file, "TEST_VAR_CBR=cbr_value\n")
    result = load_project_env()
    assert result.loaded is True
    assert result.path == env_file
    assert result.env.get("TEST_VAR_CBR") == "cbr_value"


def test__load_project_env__loads_from_pwd(tmp_path, monkeypatch):
    """File at ${PWD}/.env is loaded when config dirs are absent."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "TEST_VAR_PWD=pwd_value\n")
    result = load_project_env()
    assert result.loaded is True
    assert result.path == env_file
    assert result.env.get("TEST_VAR_PWD") == "pwd_value"


# ---------------------------------------------------------------------------
# 3. First-match precedence
# ---------------------------------------------------------------------------


def test__load_project_env__xdg_takes_precedence_over_cbr(tmp_path, monkeypatch):
    """Long config dir wins over short config dir."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    xdg = _make_env(tmp_path, ".config", "cloudflare-browser-rendering-cli", ".env")
    cbr = _make_env(tmp_path, ".config", "cbr", ".env")
    _write_env(xdg, "TEST_VAR=xdg\n")
    _write_env(cbr, "TEST_VAR=cbr\n")
    result = load_project_env()
    assert result.path == xdg
    assert result.env.get("TEST_VAR") == "xdg"


def test__load_project_env__cbr_takes_precedence_over_pwd(tmp_path, monkeypatch):
    """Short config dir wins over PWD."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    cbr = _make_env(tmp_path, ".config", "cbr", ".env")
    pwd_env = tmp_path / ".env"
    _write_env(cbr, "TEST_VAR=cbr\n")
    _write_env(pwd_env, "TEST_VAR=pwd\n")
    result = load_project_env()
    assert result.path == cbr
    assert result.env.get("TEST_VAR") == "cbr"


def test__load_project_env__all_three_precedence(tmp_path, monkeypatch):
    """Full discovery order: XDG > CBR > PWD."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    xdg = _make_env(tmp_path, ".config", "cloudflare-browser-rendering-cli", ".env")
    _make_env(tmp_path, ".config", "cbr", ".env")
    (tmp_path / ".env").write_text("TEST_VAR=pwd\n")
    _write_env(xdg, "TEST_VAR=xdg\n")
    result = load_project_env()
    assert result.path == xdg
    assert result.env.get("TEST_VAR") == "xdg"


# ---------------------------------------------------------------------------
# 4. Default non-overwrite
# ---------------------------------------------------------------------------


def test__load_project_env__default_does_not_override(tmp_path, monkeypatch):
    """Pre-existing env vars are preserved by default."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "EXISTING_VAR=from_file\nNEW_VAR=added\n")
    monkeypatch.setenv("EXISTING_VAR", "from_process")
    result = load_project_env()
    assert result.env.get("EXISTING_VAR") == "from_process"
    assert result.env.get("NEW_VAR") == "added"


# ---------------------------------------------------------------------------
# 5. Explicit override
# ---------------------------------------------------------------------------


def test__load_project_env__override_replaces_existing(tmp_path, monkeypatch):
    """override=True lets .env values replace process env vars."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "EXISTING_VAR=from_file\n")
    monkeypatch.setenv("EXISTING_VAR", "from_process")
    result = load_project_env(override=True)
    assert result.env.get("EXISTING_VAR") == "from_file"


# ---------------------------------------------------------------------------
# 6. Cache isolation / behavior
# ---------------------------------------------------------------------------


def test__load_project_env__cache_isolation_override_vs_default(tmp_path, monkeypatch):
    """override=True must not reuse the cached override=False result."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "CACHED_VAR=from_file\n")
    monkeypatch.setenv("CACHED_VAR", "from_process")

    default_result = load_project_env(override=False)
    assert default_result.env.get("CACHED_VAR") == "from_process"

    override_result = load_project_env(override=True)
    assert override_result.env.get("CACHED_VAR") == "from_file"

    # Cached results must remain stable on repeat calls.
    assert load_project_env(override=False).env.get("CACHED_VAR") == "from_process"
    assert load_project_env(override=True).env.get("CACHED_VAR") == "from_file"


def test__load_project_env__cache_returns_same_object(tmp_path, monkeypatch):
    """Repeated calls with the same arg return the cached object."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    first = load_project_env(override=False)
    second = load_project_env(override=False)
    assert first is second


# ---------------------------------------------------------------------------
# 7. Safe diagnostics
# ---------------------------------------------------------------------------


def test__diagnostics__safe_no_values(tmp_path, monkeypatch):
    """Diagnostics dict contains only metadata, never values."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "SECRET_TOKEN=supersecret\n")
    monkeypatch.setenv("SECRET_TOKEN", "supersecret")
    result = load_project_env()
    diag = result.diagnostics
    assert set(diag.keys()) == {"loaded", "path", "key_count"}
    assert diag["loaded"] is True
    assert diag["path"] == str(env_file)
    assert isinstance(diag["key_count"], int)
    # No environment value may appear anywhere in diagnostics.
    diag_str = str(diag)
    assert "supersecret" not in diag_str


def test__diagnostics__repr_leaks_no_values(tmp_path, monkeypatch):
    """Repr of EnvLoadResult must not expose env values."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "LEAK_TEST=leakme\n")
    result = load_project_env()
    assert "leakme" not in repr(result)
    assert "LEAK_TEST" not in repr(result)


# ---------------------------------------------------------------------------
# 8. Unreadable / malformed handling
# ---------------------------------------------------------------------------


def test__load_project_env__malformed_file_still_loads(tmp_path, monkeypatch):
    """Malformed lines in .env are skipped by python-dotenv without crashing."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "=no_key\nBAD LINE\nGOOD_VAR=good\n")
    result = load_project_env()
    assert result.loaded is True
    assert result.env.get("GOOD_VAR") == "good"


def test__load_project_env__empty_file_is_loaded(tmp_path, monkeypatch):
    """An empty .env file is loaded but adds no keys."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    _write_env(env_file, "")
    result = load_project_env()
    assert result.loaded is True
    assert result.path == env_file


# ---------------------------------------------------------------------------
# 9. Pipx-style invocation (HOME points elsewhere, PWD has .env)
# ---------------------------------------------------------------------------


def test__load_project_env__pipx_style_pwd_fallback(tmp_path, monkeypatch):
    """Simulate pipx install: HOME has no config dirs, PWD/.env is used."""
    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.chdir(work_dir)
    env_file = work_dir / ".env"
    _write_env(env_file, "PIPX_VAR=pipx_value\n")
    result = load_project_env()
    assert result.path == env_file
    assert result.env.get("PIPX_VAR") == "pipx_value"


def test__load_project_env__pipx_style_config_dir_preferred(tmp_path, monkeypatch):
    """Pipx install with config dir present: config dir wins over PWD."""
    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.chdir(work_dir)
    config_env = _make_env(fake_home, ".config", "cbr", ".env")
    _write_env(config_env, "PIPX_VAR=config\n")
    pwd_env = work_dir / ".env"
    _write_env(pwd_env, "PIPX_VAR=pwd\n")
    result = load_project_env()
    assert result.path == config_env
    assert result.env.get("PIPX_VAR") == "config"


# ---------------------------------------------------------------------------
# 10. EnvLoadResult dataclass
# ---------------------------------------------------------------------------


def test__env_load_result__is_frozen():
    """EnvLoadResult is immutable."""
    result = EnvLoadResult(env={}, loaded=False, path=None, key_count=0)
    with pytest.raises((AttributeError, TypeError)):
        result.loaded = True  # type: ignore[misc]


def test__find_env_file__returns_none_when_absent(tmp_path, monkeypatch):
    """_find_env_file returns None when no candidate exists."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    assert env_loader._find_env_file() is None  # pylint: disable=protected-access


def test__find_env_file__returns_first_match(tmp_path, monkeypatch):
    """_find_env_file returns the first existing candidate."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(tmp_path)
    cbr = _make_env(tmp_path, ".config", "cbr", ".env")
    _write_env(cbr, "X=1\n")
    assert env_loader._find_env_file() == cbr  # pylint: disable=protected-access
