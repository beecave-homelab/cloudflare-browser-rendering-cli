from __future__ import annotations

import importlib

from click.testing import CliRunner

cli_module = importlib.import_module("cloudflare_browser_render.cli")


class DummyError(Exception):
    """Stub error used to test --debug bubbling behavior."""


def test_debug_flag_bubbles_exceptions(monkeypatch) -> None:
    def boom(_url: str):  # noqa: ANN001
        raise DummyError("boom")

    # Patch the callback's globals via the Click command mapping
    callback = cli_module.cli.commands["content"].callback
    monkeypatch.setitem(callback.__globals__, "render_content", boom)

    runner = CliRunner()
    result = runner.invoke(cli_module.cli, ["--debug", "content", "https://example.com"])

    assert isinstance(result.exception, DummyError)
    assert result.exit_code != 0
