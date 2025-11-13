from __future__ import annotations

from pathlib import Path

import pytest

from cloudflare_browser_render import utils


def test_save_text_and_save_bytes(tmp_path: Path) -> None:
    text_path = tmp_path / "out.txt"
    bin_path = tmp_path / "out.bin"

    p1 = utils.save_text("hello", str(text_path))
    p2 = utils.save_bytes(b"\x01\x02", str(bin_path))

    assert p1 == text_path and text_path.read_text() == "hello"
    assert p2 == bin_path and bin_path.read_bytes() == b"\x01\x02"


def test_print_json_does_not_crash(capsys) -> None:  # noqa: ANN001
    utils.print_json({"a": 1})
    captured = capsys.readouterr()
    # Ensure something was printed
    assert captured.out or captured.err


def test_call_with_retry_success_without_retry() -> None:
    assert utils.call_with_retry(lambda: "ok") == "ok"


def test_call_with_retry_retries_then_success(monkeypatch) -> None:
    calls = {"n": 0}

    # Use a simple Exception subclass to simulate the SDK RateLimitError
    class DummyRateLimitError(Exception):
        pass

    monkeypatch.setattr(utils, "RateLimitError", DummyRateLimitError, raising=True)

    def fn():  # noqa: ANN202
        calls["n"] += 1
        if calls["n"] < 3:
            raise utils.RateLimitError("rate")
        return "ok"

    # Avoid sleeping during tests
    monkeypatch.setattr(utils, "time", type("T", (), {"sleep": lambda _x: None}))

    assert utils.call_with_retry(fn, max_retries=5, base_delay=0.01) == "ok"
    assert calls["n"] == 3


def test_call_with_retry_exhausted_raises(monkeypatch) -> None:
    class DummyRateLimitError(Exception):
        pass

    monkeypatch.setattr(utils, "RateLimitError", DummyRateLimitError, raising=True)

    def fn():  # noqa: ANN202
        raise utils.RateLimitError("rate")

    monkeypatch.setattr(utils, "time", type("T", (), {"sleep": lambda _x: None}))

    with pytest.raises(utils.RateLimitError):
        utils.call_with_retry(fn, max_retries=2, base_delay=0.01)
