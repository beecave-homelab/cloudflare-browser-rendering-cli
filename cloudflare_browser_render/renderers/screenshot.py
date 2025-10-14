"""Screenshot endpoint renderer.

Returns raw PNG bytes from the Browser Rendering API.
"""

from cloudflare_browser_render.client import get_client
from cloudflare_browser_render.config import get_account_id
from cloudflare_browser_render.utils import call_with_retry

_cf = get_client()

# NOTE: The SDK's .with_raw_response returns an APIResponse whose underlying
# httpx.Response provides access to the binary content via `.content`.
_account_id = get_account_id()


def render_screenshot(url: str) -> bytes:
    """Capture a PNG screenshot of *url* and return its bytes.

    Returns:
        The PNG screenshot as raw bytes.

    """
    raw = call_with_retry(
        lambda: _cf.browser_rendering.screenshot.with_raw_response.create(
            account_id=_account_id, url=url
        )
    )
    return raw.read()
