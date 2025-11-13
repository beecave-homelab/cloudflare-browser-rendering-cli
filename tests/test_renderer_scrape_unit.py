from __future__ import annotations

import types

from cloudflare_browser_render.renderers import scrape


class _Raw:
    def __init__(self, payload):  # noqa: ANN001
        self._payload = payload

    def json(self):  # noqa: D401, ANN201
        return self._payload


class _EndpointStub:
    def __init__(self, handler):  # noqa: ANN001
        self._handler = handler

    @property
    def with_raw_response(self):  # noqa: D401, ANN201
        return self

    def create(self, *args, **kwargs):  # noqa: D401, ANN001, ANN201
        return _Raw(self._handler(*args, **kwargs))


def test_render_scrape_includes_expression_and_returns_json(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def handler(*, account_id, elements, url):  # noqa: ANN001
        captured["account_id"] = account_id
        captured["elements"] = elements
        captured["url"] = url
        return {"ok": True}

    browser_rendering = types.SimpleNamespace(scrape=_EndpointStub(handler))
    stub_client = types.SimpleNamespace(browser_rendering=browser_rendering)

    monkeypatch.setattr(scrape, "_cf", stub_client, raising=True)
    monkeypatch.setattr(scrape, "_account_id", "acc-1", raising=True)

    result = scrape.render_scrape("https://example.com", "h1.title", "x+1")

    assert result == {"ok": True}
    assert captured["account_id"] == "acc-1"
    assert captured["url"] == "https://example.com"
    assert captured["elements"] == [{"selector": "h1.title", "expression": "x+1"}]


def test_render_scrape_without_expression(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def handler(*, account_id, elements, url):  # noqa: ANN001
        captured["elements"] = elements
        return {"ok": True}

    browser_rendering = types.SimpleNamespace(scrape=_EndpointStub(handler))
    stub_client = types.SimpleNamespace(browser_rendering=browser_rendering)

    monkeypatch.setattr(scrape, "_cf", stub_client, raising=True)
    monkeypatch.setattr(scrape, "_account_id", "acc-1", raising=True)

    result = scrape.render_scrape("https://example.com", "h1.title", None)

    assert result == {"ok": True}
    assert captured["elements"] == [{"selector": "h1.title"}]
