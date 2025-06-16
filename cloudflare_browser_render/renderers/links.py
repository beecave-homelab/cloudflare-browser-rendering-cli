"""Links endpoint renderer."""
from ..client import call_api


def render_links(url: str) -> dict:
    resp = call_api("/links", {"url": url})
    return resp.json()
