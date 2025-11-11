"""Renderer modules mapping."""

from cloudflare_browser_render.renderers.content import render_content
from cloudflare_browser_render.renderers.json import render_json
from cloudflare_browser_render.renderers.links import render_links
from cloudflare_browser_render.renderers.markdown import render_markdown
from cloudflare_browser_render.renderers.pdf import render_pdf
from cloudflare_browser_render.renderers.scrape import render_scrape
from cloudflare_browser_render.renderers.screenshot import render_screenshot
from cloudflare_browser_render.renderers.snapshot import render_snapshot

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
