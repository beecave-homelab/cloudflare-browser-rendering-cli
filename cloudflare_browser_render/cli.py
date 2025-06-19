"""Command line interface for Cloudflare Browser Rendering API."""

import json

import click
import questionary
from rich.console import Console

from .renderers import (
    render_content,
    render_json,
    render_links,
    render_markdown,
    render_pdf,
    render_scrape,
    render_screenshot,
    render_snapshot,
)
from .utils import print_json, save_bytes, save_text

console = Console()


# ---------------------------------------------------------------------------
# Global debug flag
# ---------------------------------------------------------------------------

_DEBUG: bool = False  # toggled via --debug option


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _process_result(result, output: str | None) -> None:
    """Handle the output coming back from a renderer.

    If *output* is provided, the result is written to that file. Otherwise it
    will be printed to the terminal. Binary data will warn the user if no
    filename was provided.
    """
    if output:
        if isinstance(result, bytes):
            save_bytes(result, output)
        elif isinstance(result, str):
            save_text(result, output)
        else:  # JSON-serialisable
            save_text(json.dumps(result, indent=2), output)
        return

    # No output path provided — print to console.
    if isinstance(result, bytes):
        console.print(
            "[yellow]Binary data received ({} bytes). Use --output to save it.".format(
                len(result)
            )
        )
    elif isinstance(result, str):
        console.print(result)
    else:
        print_json(result)


# ---------------------------------------------------------------------------
# Click CLI definition
# ---------------------------------------------------------------------------


@click.group(invoke_without_command=True)
@click.option(
    "--debug",
    is_flag=True,
    help="Show full Python tracebacks instead of concise error messages.",
)
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
    """Cloudflare Browser Rendering CLI.

    Run with **--help** to see all available subcommands. If no subcommand is
    supplied, an interactive menu will be presented.
    """
    global _DEBUG
    _DEBUG = debug

    if ctx.invoked_subcommand is None:
        _interactive_flow()


# ---------------------------------------------------------------------------
# Subcommands (one per API endpoint)
# ---------------------------------------------------------------------------


@cli.command(
    help="Render raw text content from a page and print/save it.",
    short_help="Render page text.",
)
@click.argument("url")
@click.option(
    "-o", "--output", "output", type=click.Path(dir_okay=False, writable=True)
)
def content(url: str, output: str | None) -> None:  # noqa: D401
    """Render raw **content** for *URL*."""
    try:
        result = render_content(url)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output)


@cli.command(help="Capture a PNG screenshot of the page.")
@click.argument("url")
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    help="Save PNG to FILE.",
)
def screenshot(url: str, output: str | None) -> None:
    """Capture a PNG screenshot of *url*."""
    try:
        result = render_screenshot(url)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output or "screenshot.png")


@cli.command(help="Generate a PDF of the page.")
@click.argument("url")
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    help="Save PDF to FILE.",
)
def pdf(url: str, output: str | None) -> None:
    """Generate a PDF from *url*."""
    try:
        result = render_pdf(url)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output or "output.pdf")


@cli.command(help="Create a durable snapshot of the page and return metadata.")
@click.argument("url")
@click.option("-o", "--output", type=click.Path(dir_okay=False, writable=True))
def snapshot(url: str, output: str | None) -> None:
    """Create a durable snapshot of *url* and return its metadata."""
    try:
        result = render_snapshot(url)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output)


@cli.command(help="Scrape page data with a CSS selector and return structured JSON.")
@click.argument("url")
@click.argument("selector")
@click.option("-o", "--output", type=click.Path(dir_okay=False, writable=True))
def scrape(url: str, selector: str, output: str | None) -> None:
    """Scrape *selector* from *url* and return structured JSON."""
    try:
        result = render_scrape(url, selector)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output)


@cli.command(name="json", help="Render the page into browser-generated JSON.")
@click.argument("url")
@click.option("-o", "--output", type=click.Path(dir_okay=False, writable=True))
def json_(url: str, output: str | None) -> None:  # name json_ to avoid keyword clash
    """Render *url* into browser-generated JSON."""
    try:
        result = render_json(url)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output)


@cli.command(help="Extract all links from the page and return as JSON.")
@click.argument("url")
@click.option("-o", "--output", type=click.Path(dir_okay=False, writable=True))
def links(url: str, output: str | None) -> None:
    """Extract all links from *url*."""
    try:
        result = render_links(url)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output)


@cli.command(help="Convert page content to Markdown.")
@click.argument("url")
@click.option("-o", "--output", type=click.Path(dir_okay=False, writable=True))
def markdown(url: str, output: str | None) -> None:  # noqa: D401
    """Convert *url* content to Markdown."""
    try:
        result = render_markdown(url)
    except Exception as exc:
        if _DEBUG:
            raise
        raise click.ClickException(str(exc)) from None
    _process_result(result, output)


# ---------------------------------------------------------------------------
# Interactive flow (fallback when no subcommand supplied)
# ---------------------------------------------------------------------------


def _interactive_flow() -> None:
    """Replicates the original interactive Questionary workflow."""
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

    # Handle scrape separately because it needs an extra arg.
    if endpoint == "scrape":
        selector = questionary.text("CSS selector:").ask()
        result = render_scrape(url, selector)
        _process_result(result, None)
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
    _process_result(result, None)


if __name__ == "__main__":
    cli()
