#!/bin/bash
#
# This script fetches all unique links from a predefined list of Nedap Support URLs.
# It uses the `cbr` CLI via `pdm` to extract links from each page and
# compiles them into a single Markdown file, avoiding duplicates.
#
# Usage:
#   ./get_all_nedap_links.sh [options]
#
# Options:
#   --dry-run      - Fetches links and prints to console only.
#   --no-list      - Save the extracted URLs in plain text.
#   --filter SLUG  - Only include URLs containing the specified SLUG.
#   -h, --help     - Show this help message.
#
# Dependencies:
#   - pdm
#   - cbr-rendering-cli (installed via pdm)
#   - jq (https://stedolan.github.io/jq/)
#

# --- Function to display help ---
show_help() {
    echo "Usage: $(basename "$0") [options]"
    echo ""
    echo "This script fetches all unique links from a predefined list of URLs."
    echo ""
    echo "Options:"
    echo "  --dry-run      - Fetches links and prints to console only."
    echo "  --no-list      - Save the extracted URLs in plain text."
    echo "  --filter SLUG  - Only include URLs containing the specified SLUG."
    echo "  -h, --help     - Show this help message."
    echo ""
    echo "Examples:"
    echo "  # Basic usage to fetch all links and save to a Markdown file"
    echo "  ./scripts/get_all_nedap_links.sh"
    echo ""
    echo "  # Perform a dry run without writing any files"
    echo "  ./scripts/get_all_nedap_links.sh --dry-run"
    echo ""
    echo "  # Fetch links containing 'solutions' and save as a plain text file"
    echo "  ./scripts/get_all_nedap_links.sh --filter solutions --no-list"
}

set -e
# --- Configuration ---

# Output file for the collected links
OUTPUT_FILE="all-nedap-links.md"

# --- Argument Parsing ---
DRY_RUN=false
NO_LIST=false
URL_FILTER=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-list)
            NO_LIST=true
            shift
            ;;
        --filter)
            URL_FILTER="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Array of URLs to process
URLS=(
    "https://support.nedap-ons.nl/support/solutions/103000204591"
    "https://support.nedap-ons.nl/support/solutions/103000258767"
    "https://support.nedap-ons.nl/support/solutions/103000248883"
    "https://support.nedap-ons.nl/support/solutions/103000255344"
    "https://support.nedap-ons.nl/support/solutions/103000257649"
    "https://support.nedap-ons.nl/support/solutions/103000248882"
    "https://support.nedap-ons.nl/support/solutions/103000204608"
    "https://support.nedap-ons.nl/support/solutions/103000204609"
    "https://support.nedap-ons.nl/support/solutions/103000204592"
    "https://support.nedap-ons.nl/support/solutions/103000204595"
    "https://support.nedap-ons.nl/support/solutions/103000204600"
    "https://support.nedap-ons.nl/support/solutions/103000206492"
    "https://support.nedap-ons.nl/support/solutions/103000204602"
    "https://support.nedap-ons.nl/support/solutions/103000206488"
    "https://support.nedap-ons.nl/support/solutions/103000204610"
    "https://support.nedap-ons.nl/support/solutions/103000204599"
    "https://support.nedap-ons.nl/support/solutions/103000204598"
    "https://support.nedap-ons.nl/support/solutions/103000206496"
    "https://support.nedap-ons.nl/support/solutions/103000204596"
    "https://support.nedap-ons.nl/support/solutions/103000248881"
    "https://support.nedap-ons.nl/support/solutions/103000204601"
    "https://support.nedap-ons.nl/support/solutions/103000206497"
    "https://support.nedap-ons.nl/support/solutions/103000204597"
    "https://support.nedap-ons.nl/support/solutions/103000204593"
    "https://support.nedap-ons.nl/support/solutions/103000204603"
    "https://support.nedap-ons.nl/support/solutions/103000204604"
    "https://support.nedap-ons.nl/support/solutions/103000206499"
    "https://support.nedap-ons.nl/support/solutions/103000258008"
    "https://support.nedap-ons.nl/support/solutions/103000204594"
    "https://support.nedap-ons.nl/support/solutions/103000206500"
    "https://support.nedap-ons.nl/support/solutions/103000206503"
    "https://support.nedap-ons.nl/support/solutions/103000206504"
    "https://support.nedap-ons.nl/support/solutions/103000248878"
    "https://support.nedap-ons.nl/support/solutions/103000248880"
    "https://support.nedap-ons.nl/support/solutions/103000251077"
    "https://support.nedap-ons.nl/support/solutions/103000258048"
    "https://support.nedap-ons.nl/support/solutions/103000206487"
    "https://support.nedap-ons.nl/support/solutions/folders/103000507225"
    "https://support.nedap-ons.nl/support/solutions/folders/103000507546"
    "https://support.nedap-ons.nl/support/discussions/103000099007"
    "https://support.nedap-ons.nl/support/solutions/folders/103000516727"
    "https://support.nedap-ons.nl/support/solutions/articles/103000165305-organisatorische-en-praktische-informatie"
    "https://support.nedap-ons.nl/support/solutions/folders/103000640270"
    "https://support.nedap-ons.nl/support/solutions/articles/103000165414-ontwikkelplanning"
    "https://support.nedap-ons.nl/support/solutions/folders/103000640272"
)

# --- Sanity checks ---

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it to continue." >&2
    exit 1
fi

# Check if pdm is installed
if ! command -v pdm &> /dev/null; then
    echo "Error: pdm is not installed or not in your PATH." >&2
    echo "Please install pdm: https://pdm-project.org/latest/getting-started/installation/" >&2
    exit 1
fi


# --- Main script ---

# Create a temporary file to store all links before deduplication.
# Use trap to ensure it's cleaned up on script exit (even on errors).
TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"' EXIT

echo "Collecting links from ${#URLS[@]} URLs..."
for url in "${URLS[@]}"; do
    echo "-> Processing: $url"
    
    # Run the command, storing the formatted links in a variable to count them.
    # The `if` statement checks if the command pipeline was successful.
    if links_output=$(pdm run cbr links "$url" | jq -r '.result[]? | select(. != null and . != "")'); then
        # Filter links if a filter is provided
        if [[ -n "$URL_FILTER" ]]; then
            links_output=$(echo "$links_output" | grep "$URL_FILTER" || true)
        fi

        # Count the number of lines in the output to get the link count.
        if [[ -z "$links_output" ]]; then
            link_count=0
        else
            link_count=$(echo "$links_output" | grep -c .)
            # Append the extracted links to our main temp file.
            echo "$links_output" >> "$TEMP_FILE"
        fi
        echo "   Extracted $link_count links."
    else
        echo "   (warning) Failed to process URL, or it returned no links. Skipping." >&2
    fi

    echo "   Waiting 5 seconds before next request..."
    sleep 5
done
echo "Collection complete."
echo ""

# Count total and unique links for a summary.
TOTAL_LINKS=$(wc -l < "$TEMP_FILE" | tr -d ' ')
UNIQUE_LINKS=$(sort -u "$TEMP_FILE" | wc -l | tr -d ' ')

if $DRY_RUN; then
    echo "DRY RUN: Found $TOTAL_LINKS links in total, with $UNIQUE_LINKS unique links."
    echo "The following unique links would be saved:"
    echo "----------------------------------------------------"
    if $NO_LIST; then
        sort -u "$TEMP_FILE"
    else
        sort -u "$TEMP_FILE" | awk '{print "- ["$0"]("$0")"}'
    fi
    echo "----------------------------------------------------"
    echo "✅ Dry run complete. No files were written."
else
    FINAL_OUTPUT_FILE=$OUTPUT_FILE
    if [ -f "$FINAL_OUTPUT_FILE" ]; then
        TIMESTAMP=$(date +%Y%m%d%H%M%S)
        BASE_NAME="${FINAL_OUTPUT_FILE%.*}"
        EXTENSION="${FINAL_OUTPUT_FILE##*.}"
        FINAL_OUTPUT_FILE="${BASE_NAME}-${TIMESTAMP}.${EXTENSION}"
        echo "File '$OUTPUT_FILE' already exists. Saving to new file: '$FINAL_OUTPUT_FILE'"
    fi

    echo "Found $TOTAL_LINKS links in total, with $UNIQUE_LINKS unique links. Saving to $FINAL_OUTPUT_FILE..."
    
    # Write the header to the output file, unless --no-list is used
    if ! $NO_LIST; then
        echo "# Collected Links from Nedap Support Pages" > "$FINAL_OUTPUT_FILE"
        echo "" >> "$FINAL_OUTPUT_FILE"
    else
        # Clear the file if --no-list is active
        > "$FINAL_OUTPUT_FILE"
    fi
    
    # Append the unique, sorted links
    if $NO_LIST; then
        sort -u "$TEMP_FILE" >> "$FINAL_OUTPUT_FILE"
    else
        sort -u "$TEMP_FILE" | awk '{print "- ["$0"]("$0")"}' >> "$FINAL_OUTPUT_FILE"
    fi
    
    echo "✅ Done. Saved $UNIQUE_LINKS unique links to $FINAL_OUTPUT_FILE"
fi 