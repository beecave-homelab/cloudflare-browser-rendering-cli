"""Application-wide configuration constants."""

from __future__ import annotations

from .env_loader import load_project_env

_ENV = load_project_env()

CLOUDFLARE_API_TOKEN: str = _ENV.get("CLOUDFLARE_API_TOKEN", "")
CLOUDFLARE_ACCOUNT_ID: str = _ENV.get("CLOUDFLARE_ACCOUNT_ID", "")

__all__ = [
    "CLOUDFLARE_ACCOUNT_ID",
    "CLOUDFLARE_API_TOKEN",
]
