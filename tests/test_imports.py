"""Basic import tests to ensure the CLI entry module is importable.

Running this test early in the suite catches packaging or dependency issues
that would otherwise make all subsequent tests fail.
"""

from cloudflare_browser_render import cli


def test_cli_exists():
    """Verify that the top-level `cli` entry-point is callable."""
    assert callable(cli)
