"""Tests for running the package as a module (python -m cloudflare_browser_render).

Covers cloudflare_browser_render.__main__ by simulating the __main__ execution
and asserting that cli.main(...) is invoked with the expected prog_name.
"""

from __future__ import annotations

import runpy
import sys
import types


def test_module_entrypoint_invokes_cli_main(monkeypatch):
    """Ensure that running the module calls cli.main with the correct prog name."""

    class DummyCli:
        def __init__(self) -> None:
            self.calls: list[str] = []

        def main(self, *, prog_name: str) -> None:  # matches Click's Command.main usage
            self.calls.append(prog_name)

    dummy_cli = DummyCli()

    # Provide a fake cloudflare_browser_render.cli module with a `cli` object.
    fake_cli_module = types.ModuleType("cloudflare_browser_render.cli")
    fake_cli_module.cli = dummy_cli  # type: ignore[attr-defined]

    monkeypatch.setitem(sys.modules, "cloudflare_browser_render.cli", fake_cli_module)

    # Execute as if `python -m cloudflare_browser_render`.
    runpy.run_module("cloudflare_browser_render.__main__", run_name="__main__")

    assert dummy_cli.calls == ["cloudflare-render"]
