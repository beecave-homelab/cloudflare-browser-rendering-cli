"""Content endpoint renderer."""
from ..client import call_api


def render_content(url: str) -> str:
    resp = call_api("/content", {"url": url})
    return resp.text
