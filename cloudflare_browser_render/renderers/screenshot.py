"""Screenshot endpoint renderer.

Returns raw PNG bytes from the Browser Rendering API."""

from ..client import get_client
from ..config import get_account_id
from ..utils import call_with_retry

_cf = get_client()

# NOTE: The SDK's .with_raw_response returns an APIResponse whose underlying
# httpx.Response provides access to the binary content via `.content`.
_account_id = get_account_id()


def render_screenshot(url: str) -> bytes:
    raw = call_with_retry(
        lambda: _cf.browser_rendering.screenshot.with_raw_response.create(
            account_id=_account_id, url=url
        )
    )
    return raw.read()
