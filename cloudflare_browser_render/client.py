"""HTTP client for Cloudflare Browser Rendering API."""
from typing import Dict, Any
import httpx
from .config import get_api_token

BASE_URL = "https://api.browser.render.workers.dev"


def call_api(endpoint: str, payload: Dict[str, Any]) -> httpx.Response:
    """Send POST request to a Browser Rendering API endpoint."""
    token = get_api_token()
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response
