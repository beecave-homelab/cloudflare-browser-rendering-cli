#!/usr/bin/env python3
"""Fetch og:description meta tags by parsing HTML directly.

This script fetches the `og:description` meta tag from a list of URLs
by directly downloading and parsing the HTML content of each page.
It uses the `requests` and `BeautifulSoup` libraries.
"""

import json
import os
import time
from datetime import datetime

import click
import requests
from bs4 import BeautifulSoup

# --- Configuration ---

DEFAULT_INPUT_FILE = "all-nedap-links-20250620131514.md"
DEFAULT_OUTPUT_FILE = "all-nedap-descriptions.json"

# Set a user-agent to mimic a browser and avoid blocking
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}


def get_description_and_title(
    url: str, debug: bool = False
) -> tuple[str | None, str | None, str, list[tuple[str, str]]]:
    """Fetch metadata from *url*.

    Returns:
        Tuple of (title, description, status_message, debug_lines).

    """
    debug_lines: list[tuple[str, str]] = []
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
        debug_lines.append((
            f"HTTP {response.status_code} – {len(response.content)} bytes",
            "blue",
        ))
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Description extraction
        desc_tag = soup.find("meta", property="og:description") or soup.find(
            "meta", attrs={"name": "description"}
        )
        description = desc_tag.get("content", "").strip() if desc_tag else None

        # Title extraction
        title_tag = (
            soup.find("meta", property="og:title")
            or soup.find("meta", attrs={"name": "title"})
            or soup.find("meta", property="title")
        )
        if title_tag and title_tag.has_attr("content"):
            title = title_tag["content"].strip()
        else:
            title_el = soup.find("title")
            title = title_el.text.strip() if title_el and title_el.text else None

        if debug:
            debug_lines.append((
                f"Extracted title length: {len(title) if title else 0}",
                "cyan",
            ))
            debug_lines.append((f"Extracted title: {title}", "green"))
            desc_len = len(description) if description else 0
            debug_lines.append((f"Extracted description length: {desc_len}", "cyan"))
            if description:
                excerpt = (
                    description
                    if len(description) <= 200
                    else description[:200] + "..."
                )
                debug_lines.append((f"Extracted description: {excerpt}", "white"))

        if description or title:
            return title, description, "Success", debug_lines
        return title, description, "No description or title found", debug_lines

    except requests.exceptions.RequestException as exc:
        debug_lines.append((str(exc), "red"))
        return None, None, f"Request failed: {exc}", debug_lines


@click.command(help="Fetch title and 'og:description' from URLs and save to JSON.")
@click.option(
    "-i",
    "--input",
    "input_file",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    default=DEFAULT_INPUT_FILE,
    show_default=True,
    help="Path to the input file containing URLs.",
)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Fetch descriptions and print to console instead of writing to file.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable verbose debug output for each URL.",
)
def cli(input_file: str, dry_run: bool, debug: bool):
    """Main script execution."""
    with open(input_file, encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    all_docs: list[dict[str, str]] = []

    click.echo(f"Collecting metadata from {len(urls)} URLs found in '{input_file}'...")

    with click.progressbar(length=len(urls), label="Overall Progress") as bar:
        for idx, url in enumerate(urls):
            click.echo(f"\n({idx + 1}/{len(urls)}) Processing: {url}", err=True)

            title, description, status, debug_lines = get_description_and_title(
                url, debug
            )

            if title or description:
                all_docs.append({
                    "doc_url": url,
                    "doc_title": title or "",
                    "doc_description": description or "",
                })
                click.secho(f"    -> ✅ {status}", fg="green", err=True)
            else:
                click.secho(f"    -> ❌ {status}", fg="red", err=True)

            if debug:
                for msg, color in debug_lines:
                    click.secho(f"       [debug] {msg}", fg=color, err=True)

            time.sleep(5)
            bar.update(1)

    click.echo("\nCollection complete.")

    summary = (
        f"Successfully extracted descriptions for {len(all_docs)} "
        f"out of {len(urls)} URLs."
    )

    if dry_run:
        click.echo(f"\nDRY RUN: {summary}")
        click.echo("The following JSON data would be saved:")
        click.echo("----------------------------------------------------")
        click.echo(json.dumps(all_docs, indent=2, ensure_ascii=False))
        click.echo("----------------------------------------------------")
        click.echo("✅ Dry run complete. No files were written.")
    else:
        output_path = DEFAULT_OUTPUT_FILE
        if os.path.exists(output_path):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base, ext = os.path.splitext(output_path)
            output_path = f"{base}-{timestamp}{ext}"
            msg = (
                f"File '{DEFAULT_OUTPUT_FILE}' already exists. "
                f"Saving to new file: '{output_path}'"
            )
            click.echo(msg)

        click.echo(f"\n{summary} Saving to {output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_docs, f, indent=2, ensure_ascii=False)

        click.echo(f"✅ Done. Saved {len(all_docs)} descriptions to {output_path}")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
