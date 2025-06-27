"""Scrape endpoint renderer."""

from typing import Optional
from ..client import get_client
from ..config import get_account_id
from ..utils import call_with_retry

_cf = get_client()
_account_id = get_account_id()


def render_scrape(url: str, selector: str, expression: Optional[str] = None) -> dict:
    """Scrape elements matching *selector* from *url*.

    Optionally, run a Javascript *expression* on the matched elements.
    """
    element = {"selector": selector}
    if expression:
        element["expression"] = expression

    raw = call_with_retry(
        lambda: _cf.browser_rendering.scrape.with_raw_response.create(
            account_id=_account_id,
            elements=[element],
            url=url,
        )
    )
    return raw.json()
