#!/usr/bin/env python3
"""Fetch unique links from URLs and save to Markdown.

This script fetches all unique links from a predefined list of URLs.
It uses the `cbr` CLI via `pdm` to extract links from each page and
compiles them into a single Markdown file, avoiding duplicates.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

# --- Configuration ---

# Output file for the collected links
OUTPUT_FILE = "all-nedap-links.md"

# Array of URLs to process
URLS = [
    "https://support.nedap-ons.nl/support/solutions/103000204591",
    "https://support.nedap-ons.nl/support/solutions/103000258767",
    "https://support.nedap-ons.nl/support/solutions/103000248883",
    "https://support.nedap-ons.nl/support/solutions/103000255344",
    "https://support.nedap-ons.nl/support/solutions/103000257649",
    "https://support.nedap-ons.nl/support/solutions/103000248882",
    "https://support.nedap-ons.nl/support/solutions/103000204608",
    "https://support.nedap-ons.nl/support/solutions/103000204609",
    "https://support.nedap-ons.nl/support/solutions/103000204592",
    "https://support.nedap-ons.nl/support/solutions/103000204595",
    "https://support.nedap-ons.nl/support/solutions/103000204600",
    "https://support.nedap-ons.nl/support/solutions/103000206492",
    "https://support.nedap-ons.nl/support/solutions/103000204602",
    "https://support.nedap-ons.nl/support/solutions/103000206488",
    "https://support.nedap-ons.nl/support/solutions/103000204610",
    "https://support.nedap-ons.nl/support/solutions/103000204599",
    "https://support.nedap-ons.nl/support/solutions/103000204598",
    "https://support.nedap-ons.nl/support/solutions/103000206496",
    "https://support.nedap-ons.nl/support/solutions/103000204596",
    "https://support.nedap-ons.nl/support/solutions/103000248881",
    "https://support.nedap-ons.nl/support/solutions/103000204601",
    "https://support.nedap-ons.nl/support/solutions/103000206497",
    "https://support.nedap-ons.nl/support/solutions/103000204597",
    "https://support.nedap-ons.nl/support/solutions/103000204593",
    "https://support.nedap-ons.nl/support/solutions/103000204603",
    "https://support.nedap-ons.nl/support/solutions/103000204604",
    "https://support.nedap-ons.nl/support/solutions/103000206499",
    "https://support.nedap-ons.nl/support/solutions/103000258008",
    "https://support.nedap-ons.nl/support/solutions/103000204594",
    "https://support.nedap-ons.nl/support/solutions/103000206500",
    "https://support.nedap-ons.nl/support/solutions/103000206503",
    "https://support.nedap-ons.nl/support/solutions/103000206504",
    "https://support.nedap-ons.nl/support/solutions/103000248878",
    "https://support.nedap-ons.nl/support/solutions/103000248880",
    "https://support.nedap-ons.nl/support/solutions/103000251077",
    "https://support.nedap-ons.nl/support/solutions/103000258048",
    "https://support.nedap-ons.nl/support/solutions/103000206487",
    "https://support.nedap-ons.nl/support/solutions/folders/103000507225",
    "https://support.nedap-ons.nl/support/solutions/folders/103000507546",
    "https://support.nedap-ons.nl/support/discussions/103000099007",
    "https://support.nedap-ons.nl/support/solutions/folders/103000516727",
    "https://support.nedap-ons.nl/support/solutions/articles/103000165305-organisatorische-en-praktische-informatie",
    "https://support.nedap-ons.nl/support/solutions/folders/103000640270",
    "https://support.nedap-ons.nl/support/solutions/articles/103000165414-ontwikkelplanning",
    "https://support.nedap-ons.nl/support/solutions/folders/103000640272",
]


def run_command(url: str) -> list[str]:
    """Runs the `cbr links` command and returns a list of links.

    Returns:
        List of URLs found on the page.

    """
    command = ["pdm", "run", "cbr", "links", url]
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(process.stdout)
        links = data.get("result", [])
        # Filter out any None or empty string links
        return [link for link in links if link]
    except FileNotFoundError:
        print("Error: 'pdm' command not found.", file=sys.stderr)
        print(
            "Please install pdm: https://pdm-project.org/latest/getting-started/installation/",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error processing URL {url}:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return []  # Return empty list on error
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON for URL {url}.", file=sys.stderr)
        return []


def main():
    """Main script execution."""
    examples = """
Examples:
  # Basic usage to fetch all links and save to a Markdown file
  python3 scripts/get_all_nedap_links.py

  # Perform a dry run without writing any files
  python3 scripts/get_all_nedap_links.py --dry-run

  # Fetch links containing 'solutions' and save as a plain text file
  python3 scripts/get_all_nedap_links.py --filter solutions --no-list
"""

    parser = argparse.ArgumentParser(
        description=(
            "Fetch unique links from a list of URLs and save to a Markdown file."
        ),
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Fetch links and print to console instead of writing to file.",
    )
    parser.add_argument(
        "-n",
        "--no-list",
        action="store_true",
        help="Save the extracted URLs in plain text, one per line.",
    )
    parser.add_argument(
        "-f",
        "--filter",
        type=str,
        default=None,
        help="Only include URLs containing the specified string (slug).",
    )
    args = parser.parse_args()

    all_links: set[str] = set()
    total_links_processed = 0

    print(f"Collecting links from {len(URLS)} URLs...")
    for i, url in enumerate(URLS):
        print(f"-> Processing: {url}")

        extracted_links = run_command(url)

        # Apply the filter if provided
        if args.filter:
            extracted_links = [link for link in extracted_links if args.filter in link]

        link_count = len(extracted_links)
        total_links_processed += link_count
        all_links.update(extracted_links)

        print(f"   Extracted {link_count} links.")

        if i < len(URLS) - 1:
            print("   Waiting 5 seconds before next request...")
            time.sleep(5)

    print("\nCollection complete.")

    unique_links = sorted(list(all_links))

    summary = (
        f"Found {total_links_processed} links in total, "
        f"with {len(unique_links)} unique links."
    )

    if args.dry_run:
        print(f"\nDRY RUN: {summary}")
        print("The following unique links would be saved:")
        print("----------------------------------------------------")
        for link in unique_links:
            if args.no_list:
                print(link)
            else:
                print(f"- [{link}]({link})")
        print("----------------------------------------------------")
        print("✅ Dry run complete. No files were written.")
    else:
        output_path = OUTPUT_FILE
        if os.path.exists(output_path):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base, ext = os.path.splitext(output_path)
            output_path = f"{base}-{timestamp}{ext}"
            msg = (
                f"File '{OUTPUT_FILE}' already exists. "
                f"Saving to new file: '{output_path}'"
            )
            print(msg)

        print(f"\n{summary} Saving to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            if not args.no_list:
                f.write("# Collected Links from Nedap Support Pages\n\n")

            for link in unique_links:
                if args.no_list:
                    f.write(f"{link}\n")
                else:
                    f.write(f"- [{link}]({link})\n")
        print(f"✅ Done. Saved {len(unique_links)} unique links to {output_path}")


if __name__ == "__main__":
    main()
