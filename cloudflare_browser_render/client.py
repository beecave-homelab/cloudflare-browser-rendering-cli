"""HTTP client for Cloudflare Browser Rendering API."""

from cloudflare import Cloudflare  # type: ignore

from cloudflare_browser_render.config import get_api_token

# ---------------------------------------------------------------------------
# New SDK-based Client (preferred)
# ---------------------------------------------------------------------------


# Internal singleton instance – created lazily.
_cf_client: Cloudflare | None = None


def get_client() -> Cloudflare:
    """Return a lazily-instantiated singleton Cloudflare SDK client.

    The instance is created on first call using the API token loaded from the
    environment (via :func:`config.get_api_token`). The Cloudflare SDK handles
    TLS verification, retries, and other concerns internally, so no extra
    configuration is necessary here.
    """
    global _cf_client
    if _cf_client is None:
        _cf_client = Cloudflare(api_token=get_api_token())
    return _cf_client
