#!/usr/bin/env python3
"""scripts/manual_verification.py

Automated wrapper for manual CLI verification using Python.
Loads environment variables from a .env file via python-dotenv and then
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

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


def ensure_env() -> None:
    """Load .env and validate required environment variables."""
    env_path = Path.cwd() / ".env"
    load_dotenv(dotenv_path=env_path if env_path.exists() else None)

    required = ["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        print(
            f"[ERROR] Missing required environment variables: {', '.join(missing)}.\n"
            "Set them in your shell or add them to a .env file.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"[INFO] Environment variables loaded from {env_path}")


def run_command(cmd: list[str]) -> None:
    """Run a command via `pdm run` and stream output."""
    print(f"\n[INFO] Running: {' '.join(cmd)}")
    subprocess.run(["pdm", "run", *cmd], check=True)


def main() -> None:
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
