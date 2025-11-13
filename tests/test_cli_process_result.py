from __future__ import annotations

import json
import importlib
from pathlib import Path

cli_module = importlib.import_module("cloudflare_browser_render.cli")


def test_process_result_writes_bytes_string_json(tmp_path: Path) -> None:
    # bytes
    bpath = tmp_path / "out.bin"
    cli_module._process_result(b"abc", str(bpath))
    assert bpath.read_bytes() == b"abc"

    # string
    spath = tmp_path / "out.txt"
    cli_module._process_result("hello", str(spath))
    assert spath.read_text() == "hello"

    # json-like
    jpath = tmp_path / "out.json"
    payload = {"a": 1}
    cli_module._process_result(payload, str(jpath))
    assert json.loads(jpath.read_text()) == payload


def test_process_result_prints_warning_for_bytes(capsys) -> None:  # noqa: ANN001
    cli_module._process_result(b"abc", None)
    out = capsys.readouterr().out
    assert "Binary data received" in out and "Use --output to save it" in out


def test_process_result_prints_string(capsys) -> None:  # noqa: ANN001
    cli_module._process_result("hello", None)
    out = capsys.readouterr().out
    assert "hello" in out


def test_process_result_prints_json(monkeypatch) -> None:
    called: dict[str, object] = {}

    def fake_print_json(obj):  # noqa: ANN001
        called["obj"] = obj

    monkeypatch.setattr(cli_module, "print_json", fake_print_json, raising=True)
    cli_module._process_result({"x": 1}, None)
    assert called.get("obj") == {"x": 1}
