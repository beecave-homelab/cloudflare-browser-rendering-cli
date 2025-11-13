from __future__ import annotations

import importlib

cli_module = importlib.import_module("cloudflare_browser_render.cli")


def test_interactive_no_endpoint_returns(monkeypatch) -> None:
    class Sel:
        def ask(self):  # noqa: D401
            return None

    monkeypatch.setattr(cli_module.questionary, "select", lambda *a, **k: Sel())
    cli_module._interactive_flow()


def test_interactive_json_path(monkeypatch) -> None:
    class Sel:
        def ask(self):  # noqa: D401
            return "json"

    class Txt:
        def ask(self):  # noqa: D401
            return "https://example.com"

    monkeypatch.setattr(cli_module.questionary, "select", lambda *a, **k: Sel())
    monkeypatch.setattr(cli_module.questionary, "text", lambda *a, **k: Txt())

    monkeypatch.setattr(cli_module, "render_json", lambda url: {"ok": 1})

    called = {"obj": None}
    monkeypatch.setattr(
        cli_module, "print_json", lambda obj: called.__setitem__("obj", obj)
    )

    cli_module._interactive_flow()
    assert called["obj"] == {"ok": 1}


def test_interactive_scrape_path(monkeypatch) -> None:
    class Sel:
        def ask(self):  # noqa: D401
            return "scrape"

    responses = ["https://example.com", "h1.title"]

    class Txt:
        def ask(self):  # noqa: D401
            return responses.pop(0)

    monkeypatch.setattr(cli_module.questionary, "select", lambda *a, **k: Sel())
    monkeypatch.setattr(cli_module.questionary, "text", lambda *a, **k: Txt())

    called = {"args": None}

    def fake_scrape(url: str, selector: str, expression=None):  # noqa: ANN001, D401
        called["args"] = (url, selector, expression)
        return {"ok": 1}

    monkeypatch.setattr(cli_module, "render_scrape", fake_scrape, raising=True)
    monkeypatch.setattr(cli_module, "print_json", lambda obj: None)

    cli_module._interactive_flow()

    assert called["args"] == ("https://example.com", "h1.title", None)
