"""Utility helpers for CLI operations."""

import json
import time
from pathlib import Path
from typing import Any, Callable, TypeVar

from rich.console import Console

# Cloudflare SDK error class for rate-limiting
try:
    from cloudflare import RateLimitError  # type: ignore
except ImportError:  # pragma: no cover – fallback for old SDKs
    RateLimitError = Exception  # type: ignore  # noqa: N816

T = TypeVar("T")

console = Console()


def save_bytes(data: bytes, filename: str) -> Path:
    path = Path(filename)
    path.write_bytes(data)
    console.print(f"[green]Saved file to {path}[/green]")
    return path


def save_text(data: str, filename: str) -> Path:
    path = Path(filename)
    path.write_text(data)
    console.print(f"[green]Saved file to {path}[/green]")
    return path


def print_json(data: Any) -> None:
    console.print_json(json.dumps(data))


# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------


def call_with_retry(
    func: Callable[[], T], *, max_retries: int = 3, base_delay: float = 1.0
) -> T:  # noqa: D401
    """Call *func* and retry automatically on Cloudflare *RateLimitError*.

    Parameters
    ----------
    func
        A zero-argument callable that performs the Cloudflare SDK request.
    max_retries
        Number of attempts before giving up (default **3**).
    base_delay
        Initial delay in seconds before retrying. Each subsequent retry doubles
        this delay (exponential back-off).

    Returns
    -------
    T
        The return value of *func*.
    """

    delay = base_delay
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise  # re-raise after final attempt

            console.print(
                f"[yellow]Rate limit hit (attempt {attempt + 1}/{max_retries}). "
                f"Retrying in {delay:.1f}s …[/yellow]"
            )
            time.sleep(delay)
            delay *= 2  # exponential back-off

    # This point should never be reached – kept for static analysers.
    raise RuntimeError("call_with_retry exhausted retries unexpectedly")
