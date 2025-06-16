"""Utility helpers for CLI operations."""
from pathlib import Path
import json
from typing import Any
from rich.console import Console

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
