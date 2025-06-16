"""Scrape endpoint renderer."""
from ..client import call_api


def render_scrape(url: str, selector: str) -> dict:
    resp = call_api("/scrape", {"url": url, "selector": selector})
    return resp.json()
