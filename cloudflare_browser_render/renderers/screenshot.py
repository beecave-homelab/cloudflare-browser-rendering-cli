"""Screenshot endpoint renderer."""
from ..client import call_api


def render_screenshot(url: str) -> bytes:
    resp = call_api("/screenshot", {"url": url})
    return resp.content
