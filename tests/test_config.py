from __future__ import annotations

import pytest

from cloudflare_browser_render import config


def test_get_api_token_missing(monkeypatch) -> None:
    monkeypatch.setenv(config.API_TOKEN_ENV, "")
    with pytest.raises(RuntimeError) as ei:
        config.get_api_token()
    assert config.API_TOKEN_ENV in str(ei.value)


def test_get_account_id_missing(monkeypatch) -> None:
    monkeypatch.setenv(config.ACCOUNT_ID_ENV, "")
    with pytest.raises(RuntimeError) as ei:
        config.get_account_id()
    assert config.ACCOUNT_ID_ENV in str(ei.value)
