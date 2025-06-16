"""JSON endpoint renderer."""
from ..client import call_api


def render_json(url: str) -> dict:
    resp = call_api("/json", {"url": url})
    return resp.json()
