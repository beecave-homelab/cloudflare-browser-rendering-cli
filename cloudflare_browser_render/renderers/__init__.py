"""Renderer modules mapping."""
from .content import render_content
from .screenshot import render_screenshot
from .pdf import render_pdf
from .snapshot import render_snapshot
from .scrape import render_scrape
from .json import render_json
from .links import render_links
from .markdown import render_markdown

__all__ = [
    "render_content",
    "render_screenshot",
    "render_pdf",
    "render_snapshot",
    "render_scrape",
    "render_json",
    "render_links",
    "render_markdown",
]
