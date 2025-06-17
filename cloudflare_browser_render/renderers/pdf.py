"""PDF endpoint renderer."""

from ..client import call_api


def render_pdf(url: str) -> bytes:
    resp = call_api("/pdf", {"url": url})
    return resp.content
