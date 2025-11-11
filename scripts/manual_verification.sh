#!/usr/bin/env bash
# scripts/manual_verification.sh
#
# Automated wrapper for manual CLI verification of cloudflare-render commands.
# Requires CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID to be set in the environment.
#
# Usage:
#   scripts/manual_verification.sh [URL] [CSS_SELECTOR]
#
#   URL           - The target webpage to render (default: https://example.com)
#   CSS_SELECTOR  - Selector for scrape endpoint (default: h1)
#
# Example:
#   export CLOUDFLARE_API_TOKEN="..."
#   export CLOUDFLARE_ACCOUNT_ID="..."
#   pdm install
#   ./scripts/manual_verification.sh https://example.com "h1.title"

set -euo pipefail

URL="${1:-https://example.com}"
CSS_SELECTOR="${2:-h1}"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]] || [[ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
  echo "[ERROR] CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be exported before running this script." >&2
  exit 1
fi

echo "[INFO] Running cloudflare-render manual verification against: $URL"

# content (text to stdout)
printf "\n[content]---------------------------------------------\n"
pdm run cloudflare-render content "$URL"

# screenshot (PNG output)
printf "\n[screenshot]------------------------------------------\n"
pdm run cloudflare-render screenshot "$URL" -o screenshot.png

echo "[INFO] screenshot.png saved."

# pdf (PDF output)
printf "\n[pdf]-------------------------------------------------\n"
pdm run cloudflare-render pdf "$URL" -o page.pdf

echo "[INFO] page.pdf saved."

# snapshot (JSON metadata)
printf "\n[snapshot]-------------------------------------------\n"
pdm run cloudflare-render snapshot "$URL"

# scrape (selector)
printf "\n[scrape]---------------------------------------------\n"
pdm run cloudflare-render scrape "$URL" "$CSS_SELECTOR" -o heading.json

echo "[INFO] heading.json saved."

# json (structured page)
printf "\n[json]-----------------------------------------------\n"
pdm run cloudflare-render json "$URL" -o page.json

echo "[INFO] page.json saved."

# links (extract links)
printf "\n[links]----------------------------------------------\n"
pdm run cloudflare-render links "$URL" -o links.json

echo "[INFO] links.json saved."

# markdown (Markdown content)
printf "\n[markdown]-------------------------------------------\n"
pdm run cloudflare-render markdown "$URL" -o page.md

echo "[INFO] page.md saved."

echo "\n[INFO] Manual verification script completed successfully." 