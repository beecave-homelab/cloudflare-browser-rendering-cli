"""Markdown endpoint renderer."""

from cloudflare_browser_render.client import get_client
from cloudflare_browser_render.config import get_account_id
from cloudflare_browser_render.utils import call_with_retry

_cf = get_client()
_account_id = get_account_id()


def render_markdown(url: str) -> str:
    """Convert *url* content to Markdown text.

    Returns:
        The webpage content converted to Markdown format.

    """
    raw = call_with_retry(
        lambda: _cf.browser_rendering.markdown.with_raw_response.create(
            account_id=_account_id, url=url
        )
    )
    return raw.text()
