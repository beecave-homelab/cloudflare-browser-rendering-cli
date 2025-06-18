"""Scrape endpoint renderer."""

from ..client import get_client
from ..config import get_account_id
from ..utils import call_with_retry

_cf = get_client()
_account_id = get_account_id()


def render_scrape(url: str, selector: str) -> dict:
    raw = call_with_retry(
        lambda: _cf.browser_rendering.scrape.with_raw_response.create(
            account_id=_account_id,
            elements=[{"selector": selector}],
            url=url,
        )
    )
    return raw.json()
