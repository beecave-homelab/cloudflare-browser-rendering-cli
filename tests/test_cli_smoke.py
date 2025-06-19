"""Automated smoke-tests for the Click CLI.

Each test monkey-patches the renderer modules` _cf` client with a stub that
returns predictable responses, then invokes the corresponding CLI command via
Click's `CliRunner`.  We assert that each sub-command exits with status 0 —
proving that the CLI/renderer integration works independently of the live
Cloudflare API.
"""

from __future__ import annotations

import types
from typing import Any, Callable

import pytest
from click.testing import CliRunner

from cloudflare_browser_render.cli import cli as cli_group

# ---------------------------------------------------------------------------
# Helpers: stub client & raw-response wrappers
# ---------------------------------------------------------------------------


class _Raw:
    """Mimics the Cloudflare SDK *APIResponse* used with `.with_raw_response`."""

    def __init__(self, payload: Any):
        self._payload = payload

    # Behaviour for `.text()` (content / markdown endpoints)
    def text(self) -> str:  # noqa: D401 – Click expects .text()
        return str(self._payload)

    # Behaviour for `.json()` (json / scrape / snapshot / links endpoints)
    def json(self) -> Any:  # noqa: D401 – mimics SDK signature
        return self._payload

    # Behaviour for `.read()` (pdf / screenshot endpoints)
    def read(self) -> bytes:  # noqa: D401 – mimics SDK signature
        if isinstance(self._payload, bytes):  # already bytes → return as-is
            return self._payload
        return bytes(str(self._payload), "utf-8")

    # Attribute used by some renderer comments (not strictly required here)
    @property
    def content(self) -> bytes:  # noqa: D401 – matches httpx.Response API
        return self.read()


class _EndpointStub:
    """Callable stub returned from `with_raw_response` chain."""

    def __init__(self, factory: Callable[[], Any]):
        self._factory = factory

    # `.with_raw_response` returns an object exposing `.create(...)`.
    @property
    def with_raw_response(self):  # noqa: D401 – property name mirrors SDK
        return self

    # pylint: disable=unused-argument – signature matches SDK.
    def create(self, *args, **kwargs):  # noqa: D401 – mirrors SDK
        return _Raw(self._factory())


@pytest.fixture()
def stub_client(monkeypatch):
    """Replace each renderer module's `_cf` singleton with a predictable stub."""
    # Mapping: endpoint name → value factory used by the renderer tests.
    endpoint_payloads: dict[str, Callable[[], Any]] = {
        "content": lambda: "stub-content",
        "markdown": lambda: "# stub-markdown",
        "json": lambda: {"key": "value"},
        "scrape": lambda: {"selector": "h1", "text": "stub"},
        "snapshot": lambda: {"id": "abc123"},
        "links": lambda: ["https://example.com"],
        "pdf": lambda: b"%PDF-stub%\n",
        "screenshot": lambda: b"\x89PNG\r\nstub",
    }

    # Build a browser_rendering namespace with dynamic attributes.
    browser_rendering = types.SimpleNamespace(
        **{
            name: types.SimpleNamespace(
                create=_EndpointStub(func).create, with_raw_response=_EndpointStub(func)
            )
            for name, func in endpoint_payloads.items()
        }
    )

    stub = types.SimpleNamespace(browser_rendering=browser_rendering)

    # Patch every renderer module's captured `_cf`.
    import importlib
    import pkgutil

    renderer_pkg = importlib.import_module("cloudflare_browser_render.renderers")
    for mod_info in pkgutil.iter_modules(renderer_pkg.__path__):
        module = importlib.import_module(
            f"cloudflare_browser_render.renderers.{mod_info.name}"
        )
        # Only patch modules that define the sentinel `_cf` attribute.
        if hasattr(module, "_cf"):
            monkeypatch.setattr(module, "_cf", stub)


# ---------------------------------------------------------------------------
# Smoke tests — one per sub-command
# ---------------------------------------------------------------------------


def _run_cli(runner: CliRunner, *args: str):
    """Invoke CLI and assert success."""
    result = runner.invoke(cli_group, list(args))
    assert result.exit_code == 0, result.output


@pytest.mark.usefixtures("stub_client")
@pytest.mark.parametrize(
    "args",
    [
        ("content", "https://example.com"),
        ("screenshot", "https://example.com"),
        ("pdf", "https://example.com"),
        ("snapshot", "https://example.com"),
        ("scrape", "https://example.com", "h1.title"),
        ("json", "https://example.com"),
        ("links", "https://example.com"),
        ("markdown", "https://example.com"),
    ],
)
def test_cli_smoke(args):
    """Run each CLI subcommand with stubbed client and assert success."""
    runner = CliRunner()
    _run_cli(runner, *args)
