"""Configuration for Cloudflare Browser Rendering CLI."""

from __future__ import annotations

from cloudflare_browser_render.utils.constant import (
    CLOUDFLARE_ACCOUNT_ID,
    CLOUDFLARE_API_TOKEN,
)

API_TOKEN_ENV = "CLOUDFLARE_API_TOKEN"
ACCOUNT_ID_ENV = "CLOUDFLARE_ACCOUNT_ID"


def get_api_token() -> str:
    """Retrieve API token from environment variables.

    Returns:
        The Cloudflare API token.

    Raises:
        RuntimeError: If the API token is not found in environment variables.

    """
    token = CLOUDFLARE_API_TOKEN
    if not token:
        raise RuntimeError(f"{API_TOKEN_ENV} not found in environment or .env file")
    return token


def get_account_id() -> str:
    """Retrieve Cloudflare Account ID from environment variables.

    Returns:
        The Cloudflare Account ID.

    Raises:
        RuntimeError: If the Account ID is not found in environment variables.

    """
    account_id = CLOUDFLARE_ACCOUNT_ID
    if not account_id:
        raise RuntimeError(f"{ACCOUNT_ID_ENV} not found in environment or .env file")
    return account_id
