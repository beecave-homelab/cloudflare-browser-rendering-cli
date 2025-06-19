"""Content endpoint renderer."""

from ..client import get_client
from ..config import get_account_id
from ..utils import call_with_retry

_cf = get_client()
_account_id = get_account_id()


def render_content(url: str) -> str:
    """Return the raw text content of *url*."""
    raw = call_with_retry(
        lambda: _cf.browser_rendering.content.with_raw_response.create(
            account_id=_account_id, url=url
        )
    )
    # SDK returns an httpx.Response; use .text() to get decoded body
    return raw.text()
