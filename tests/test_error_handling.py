"""Automated tests that verify CLI error-handling behaviour.

When any renderer raises an exception, the CLI should transform it into a
user-friendly Click error message, exit with a non-zero code, and *not* print a
traceback.
"""

from __future__ import annotations

import pytest
from click.testing import CliRunner

# CLI entry-point
from cloudflare_browser_render.cli import cli


class DummyAPIError(Exception):
    """Stub exception to simulate Cloudflare SDK failures."""


# Endpoint definitions: (patch_target, args)
ENDPOINTS: list[tuple[str, list[str]]] = [
    (
        "cloudflare_browser_render.renderers.content.render_content",
        ["content", "https://example.com"],
    ),
    (
        "cloudflare_browser_render.renderers.screenshot.render_screenshot",
        ["screenshot", "https://example.com"],
    ),
    (
        "cloudflare_browser_render.renderers.pdf.render_pdf",
        ["pdf", "https://example.com"],
    ),
    (
        "cloudflare_browser_render.renderers.snapshot.render_snapshot",
        ["snapshot", "https://example.com"],
    ),
    (
        "cloudflare_browser_render.renderers.scrape.render_scrape",
        ["scrape", "https://example.com", "h1"],
    ),
    (
        "cloudflare_browser_render.renderers.json.render_json",
        ["json", "https://example.com"],
    ),
    (
        "cloudflare_browser_render.renderers.links.render_links",
        ["links", "https://example.com"],
    ),
    (
        "cloudflare_browser_render.renderers.markdown.render_markdown",
        ["markdown", "https://example.com"],
    ),
]


@pytest.mark.parametrize("patch_target, cli_args", ENDPOINTS)
def test_cli_handles_errors_gracefully(
    monkeypatch, patch_target: str, cli_args: list[str]
) -> None:
    """Ensure each CLI subcommand exits cleanly when its renderer raises."""

    # Monkey-patch the renderer to raise our dummy error.
    def _raise_dummy(*_args, **_kwargs):  # noqa: ANN001
        raise DummyAPIError("boom")

    # monkeypatch.setattr() requires separating the module and attribute.
    import importlib

    module_path, attr_name = patch_target.rsplit(".", 1)
    module = importlib.import_module(module_path)
    monkeypatch.setattr(module, attr_name, _raise_dummy, raising=True)

    # Also patch the reference already imported into cloudflare_browser_render.cli
    import cloudflare_browser_render.cli as cli_module  # noqa: E402

    if hasattr(cli_module, attr_name):
        monkeypatch.setattr(cli_module, attr_name, _raise_dummy, raising=True)

    # Also patch the callback's global reference that Click captured at definition
    cmd_name = cli_args[0]
    callback = cli.commands[cmd_name].callback
    monkeypatch.setitem(callback.__globals__, attr_name, _raise_dummy)

    runner = CliRunner()
    result = runner.invoke(cli, cli_args)

    # The Click framework should convert DummyAPIError into a user-friendly
    # ClickException, exit with code 1, and suppress the traceback.
    assert result.exit_code == 1, result.output
    # Click wraps errors in a SystemExit; ensure we didn't get the original exception.
    if result.exception is not None:
        # Allow SystemExit but nothing else.
        assert isinstance(result.exception, SystemExit), result.exception
    assert "Error: boom" in result.output
    assert "Traceback" not in result.output
