"""Markdown endpoint renderer."""

from ..client import call_api


def render_markdown(url: str) -> str:
    resp = call_api("/markdown", {"url": url})
    return resp.text
