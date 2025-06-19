# \U0001F4E6 Cloudflare Browser Rendering CLI

A fully interactive CLI wrapper around Cloudflare's Browser Rendering API. Built with Click, Questionary, and Rich. Supports screenshots, PDFs, HTML snapshots, scraping, structured JSON, and more — directly from your terminal.

## Usage

Install the package and run `cloudflare-render` to interactively choose an endpoint and provide a URL.
+You can also use the shorter alias `cbr` (defined in the project's console-scripts table).
Results can be saved to disk or printed in the terminal.

Ensure you provide your API token via a `.env` file:

```bash
CLOUDFLARE_API_TOKEN=your-browser-render-api-token
```
