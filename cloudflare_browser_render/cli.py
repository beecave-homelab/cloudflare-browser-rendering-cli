"""Command line interface for Cloudflare Browser Rendering API."""
import click
import questionary
from rich.console import Console
from .utils import save_bytes, save_text, print_json
from .renderers import (
    render_content,
    render_screenshot,
    render_pdf,
    render_snapshot,
    render_scrape,
    render_json,
    render_links,
    render_markdown,
)

console = Console()


@click.command()
def cli() -> None:
    """Interactively call Cloudflare Browser Rendering endpoints."""
    endpoint = questionary.select(
        "Which endpoint do you want to use?",
        choices=[
            "content",
            "screenshot",
            "pdf",
            "snapshot",
            "scrape",
            "json",
            "links",
            "markdown",
        ],
    ).ask()
    if not endpoint:
        return
    url = questionary.text("Enter the target URL:").ask()
    if not url:
        return

    if endpoint == "scrape":
        selector = questionary.text("CSS selector:").ask()
        result = render_scrape(url, selector)
        print_json(result)
        return
    renderer_map = {
        "content": render_content,
        "screenshot": render_screenshot,
        "pdf": render_pdf,
        "snapshot": render_snapshot,
        "json": render_json,
        "links": render_links,
        "markdown": render_markdown,
    }
    renderer = renderer_map[endpoint]
    result = renderer(url)

    if isinstance(result, bytes):
        default = f"output.{ 'png' if endpoint == 'screenshot' else 'pdf'}"
        save = questionary.confirm("Save result to file?", default=True).ask()
        if save:
            filename = questionary.text("Filename", default=default).ask()
            save_bytes(result, filename)
    elif isinstance(result, str):
        save = questionary.confirm("Save result to file?", default=False).ask()
        if save:
            filename = questionary.text("Filename", default="output.txt").ask()
            save_text(result, filename)
        else:
            console.print(result)
    else:
        print_json(result)
