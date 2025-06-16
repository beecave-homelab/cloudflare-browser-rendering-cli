"""Snapshot endpoint renderer."""
from ..client import call_api


def render_snapshot(url: str) -> dict:
    resp = call_api("/snapshot", {"url": url})
    return resp.json()
