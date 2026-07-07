"""Automated wrapper for manual CLI verification using Python.

Loads environment variables through the package constants module and then
executes each `cloudflare-render` subcommand through PDM.

Usage:
    python scripts/manual_verification.py [URL] [CSS_SELECTOR]

    URL           - Target webpage (default: https://example.com)
    CSS_SELECTOR  - Selector for scrape endpoint (default: h1)

Example:
    # Ensure .env contains CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID
    pdm install
    python scripts/manual_verification.py https://example.com "h1.title"
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from cloudflare_browser_render.config import ACCOUNT_ID_ENV, API_TOKEN_ENV
from cloudflare_browser_render.utils.constant import (
    CLOUDFLARE_ACCOUNT_ID,
    CLOUDFLARE_API_TOKEN,
)


def ensure_env() -> None:
    """Validate required environment variables via the constants module."""
    env_path = Path.cwd() / ".env"

    required = {
        API_TOKEN_ENV: CLOUDFLARE_API_TOKEN,
        ACCOUNT_ID_ENV: CLOUDFLARE_ACCOUNT_ID,
    }
    missing = [var for var, value in required.items() if not value]
    if missing:
        print(
            f"[ERROR] Missing required environment variables: {', '.join(missing)}.\n"
            "Set them in your shell or add them to a .env file.",
            file=sys.stderr,
        )
        sys.exit(1)

    if env_path.exists():
        print(f"[INFO] Environment variables loaded from {env_path}")
    else:
        print("[INFO] Environment variables loaded from the active shell")


def run_command(cmd: list[str]) -> None:
    """Run a command via `pdm run` and stream output."""
    print(f"\n[INFO] Running: {' '.join(cmd)}")
    subprocess.run(["pdm", "run", *cmd], check=True)


def main() -> None:
    """Run all CLI subcommands against *url* for manual verification."""
    ensure_env()

    url: str = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    selector: str = sys.argv[2] if len(sys.argv) > 2 else "h1"

    commands = [
        ["cloudflare-render", "content", url],
        ["cloudflare-render", "screenshot", url, "-o", "screenshot.png"],
        ["cloudflare-render", "pdf", url, "-o", "page.pdf"],
        ["cloudflare-render", "snapshot", url],
        ["cloudflare-render", "scrape", url, selector, "-o", "heading.json"],
        ["cloudflare-render", "json", url, "-o", "page.json"],
        ["cloudflare-render", "links", url, "-o", "links.json"],
        ["cloudflare-render", "markdown", url, "-o", "page.md"],
    ]

    for cmd in commands:
        run_command(cmd)

    print("\n[INFO] Manual verification script completed successfully.")


if __name__ == "__main__":
    main()
