"""Configuration for Cloudflare Browser Rendering CLI."""

import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN_ENV = "CLOUDFLARE_API_TOKEN"


def get_api_token() -> str:
    """Retrieve API token from environment variables."""
    token = os.getenv(API_TOKEN_ENV)
    if not token:
        raise RuntimeError(f"{API_TOKEN_ENV} not found in environment or .env file")
    return token
