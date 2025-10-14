"""Links endpoint renderer."""

from cloudflare_browser_render.client import get_client
from cloudflare_browser_render.config import get_account_id
from cloudflare_browser_render.utils import call_with_retry

_cf = get_client()
_account_id = get_account_id()


def render_links(url: str) -> dict:
    """Return all links extracted from *url*.

    Returns:
        Dictionary containing all links found on the webpage.

    """
    raw = call_with_retry(
        lambda: _cf.browser_rendering.links.with_raw_response.create(
            account_id=_account_id, url=url
        )
    )
    return raw.json()
