#!/usr/bin/env python3
"""Fetch og:description meta tags from URLs.

This script fetches the `og:description` meta tag from a list of URLs
provided in a text file. It uses the `cbr` CLI via `pdm` to scrape
the `content` attribute from the meta tag.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

# --- Configuration ---

# Default input file with the list of URLs
DEFAULT_INPUT_FILE = "all-nedap-links-20250620131514.md"
# Default output file for the collected descriptions
DEFAULT_OUTPUT_FILE = "all-nedap-descriptions.json"


def run_command(url: str) -> str | None:
    """Runs `cbr scrape` command and returns the `og:description` content.

    Returns:
        The og:description content if found, None otherwise.

    """
    selector = "meta[property='og:description']"
    expression = "el => el.getAttribute('content')"

    command = ["pdm", "run", "cbr", "scrape", url, selector, "-e", expression]

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(process.stdout)

        # The API returns a `result` list where each item corresponds to a
        # requested selector. Since we only request one, we take the first item.
        result_list = data.get("result", [])
        if not result_list:
            print(f"Warning: 'result' list is empty for URL {url}.", file=sys.stderr)
            return None

        # The actual value is nested inside the first result item.
        description = result_list[0].get("result", {}).get("value")

        return description

    except FileNotFoundError:
        print("Error: 'pdm' command not found.", file=sys.stderr)
        print(
            "Please install pdm: https://pdm-project.org/latest/getting-started/installation/",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error processing URL {url}:", file=sys.stderr)
        # Attempt to parse the JSON error from Cloudflare if possible
        try:
            error_json = json.loads(e.stdout)
            print(json.dumps(error_json, indent=2), file=sys.stderr)
        except json.JSONDecodeError:
            print(e.stderr, file=sys.stderr)
        return None
    except (json.JSONDecodeError, IndexError, KeyError, TypeError) as e:
        print(
            f"Error: Could not parse or find description for URL {url}.",
            file=sys.stderr,
        )
        print(f"Details: {e}", file=sys.stderr)
        # Also print the raw data that caused the error
        if "process" in locals() and hasattr(process, "stdout"):
            print("--- RAW DATA ---", file=sys.stderr)
            print(process.stdout, file=sys.stderr)
            print("----------------", file=sys.stderr)
        return None


def main():
    """Main script execution."""
    examples = """
Examples:
  # Basic usage with the default input file
  python3 scripts/get_all_nedap_descriptions.py

  # Specify a different input file
  python3 scripts/get_all_nedap_descriptions.py -i another-file.md

  # Perform a dry run without writing any files
  python3 scripts/get_all_nedap_descriptions.py --dry-run
"""

    parser = argparse.ArgumentParser(
        description="Fetch 'og:description' from a list of URLs and save to JSON.",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f"Path to the input file containing URLs (default: {DEFAULT_INPUT_FILE}).",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Fetch descriptions and print to console instead of writing to file.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found at '{args.input}'", file=sys.stderr)
        sys.exit(1)

    with open(args.input, encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    all_docs: list[dict[str, str]] = []

    print(f"Collecting descriptions from {len(urls)} URLs found in '{args.input}'...")
    for i, url in enumerate(urls):
        print(f"-> Processing ({i + 1}/{len(urls)}): {url}")

        description = run_command(url)

        if description:
            all_docs.append({"doc_url": url, "doc_description": description})
            print("   Extracted description successfully.")
        else:
            print("   Failed to extract description.")

        if i < len(urls) - 1:
            print("   Waiting 5 seconds before next request...")
            time.sleep(5)

    print("\nCollection complete.")

    summary = (
        f"Successfully extracted descriptions for {len(all_docs)} "
        f"out of {len(urls)} URLs."
    )

    if args.dry_run:
        print(f"\nDRY RUN: {summary}")
        print("The following JSON data would be saved:")
        print("----------------------------------------------------")
        print(json.dumps(all_docs, indent=2))
        print("----------------------------------------------------")
        print("✅ Dry run complete. No files were written.")
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
            print(msg)

        print(f"\n{summary} Saving to {output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_docs, f, indent=2)

        print(f"✅ Done. Saved {len(all_docs)} descriptions to {output_path}")


if __name__ == "__main__":
    main()
