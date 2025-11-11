#!/usr/bin/env bash
# manual_verify_all.sh
# Run every sub-command against a real URL, capture output & exit codes.

URL="https://example.com"
CSS_SELECTOR="h1.title"
LOG="manual_verification_results.log"

echo "=== $(date) ===" >> "$LOG"

run() {
  echo -e "\n▶️  Running: cloudflare-render $*"
  echo "\n--- $* ---"            >> "$LOG"
  pdm run cloudflare-render "$@" | tee -a "$LOG"
  exit_code=${PIPESTATUS[0]}
  echo "exit_code=$exit_code"      >> "$LOG"
  echo "↪️  Completed (exit $exit_code)"
  sleep 5
}

# text / JSON endpoints (stdout only)
run content   "$URL"
run json      "$URL"
run links     "$URL"
run markdown  "$URL"
run scrape    "$URL" "$CSS_SELECTOR"
run snapshot  "$URL"

# binary endpoints – save to disk, log name+size
run screenshot "$URL" -o screenshot.png
echo "Saved screenshot.png ($(du -h screenshot.png | cut -f1))" | tee -a "$LOG"

run pdf "$URL" -o page.pdf
echo "Saved page.pdf ($(du -h page.pdf | cut -f1))"    | tee -a "$LOG"

echo "=== end ===" >> "$LOG"
echo "Wrote consolidated results to $LOG"
