# 📦 Cloudflare Browser Rendering CLI

A fast, friendly command-line tool for Cloudflare's Browser Rendering API. Capture screenshots, PDFs, raw text, links, JSON, Markdown and more straight from your terminal.

## Versions

**Current version**: 0.2.1 – Code quality improvements, comprehensive docstring coverage, linting enhancements.

## Table of Contents

- [Versions](#versions)
- [Badges](#badges)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)

## Badges

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org)
[![Version](https://img.shields.io/badge/Version-0.2.1-brightgreen)](#versions)
[![License](https://img.shields.io/badge/License-MIT-yellow)](#license)

## Installation

1. Install with pip (requires Python 3.11+):

   ```bash
   pip install cloudflare-browser-rendering-cli
   ```

2. Export your Cloudflare Browser Rendering API token (or create a `.env` file):

   ```bash
   export CLOUDFLARE_API_TOKEN="your-browser-render-api-token"
   ```

That's it! You're ready to render.

> Prefer an isolated environment? Feel free to use `pdm`, `poetry`, or a virtualenv – the CLI works the same.

## Usage

Run the interactive menu:

```bash
cloudflare-render
```

Or call a sub-command directly:

```bash
# Grab raw text content
cloudflare-render content https://example.com

# Capture a PNG screenshot
cloudflare-render screenshot https://example.com -o screenshot.png

# Generate a PDF
cloudflare-render pdf https://example.com -o page.pdf
```

Short on keystrokes? Use the alias `cbr` instead of `cloudflare-render`.

Each command accepts `-o/--output` to save the response to file. Without it, text and JSON print to the terminal; binary data prompts you to choose where to save.

Need more detail? Pass `--debug` to show full tracebacks.

## License

This project is licensed under the MIT license. See [LICENSE](LICENSE) for full details.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to improve. Thank you for helping make the CLI even better.
