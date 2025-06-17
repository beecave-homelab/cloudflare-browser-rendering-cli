---
repo: https://github.com/beecave-homelab/cloudflare-browser-rendering-cli.git
commit: 740de826088820d6575e511fb686a33b5f0db4b9
generated: 2025-06-17T21:05:00Z
---
<!-- SECTIONS:API,CLI,CODE-QUALITY,TESTS -->

# Project Overview | cloudflare-render

This project provides an interactive Command Line Interface (CLI) and a Python client for interacting with the Cloudflare Browser Rendering API.

[![Language](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org)
[![Version](https://img.shields.io/badge/Version-0.1.0-brightgreen)](#version-summary)
[![Dependencies](https://img.shields.io/badge/Dependencies-click%2C%20questionary%2C%20rich%2C%20httpx%2C%20python--dotenv-orange)](pyproject.toml)

## Table of Contents

- [Quickstart for Developers](#quickstart-for-developers)
- [Version Summary](#version-summary)
- [Project Features](#project-features)
- [Project Structure](#project-structure)
- [Architecture Highlights](#architecture-highlights)
- [API](#api)
- [CLI](#cli)
- [Code Quality](#code-quality)
- [Tests](#tests)

## Quickstart for Developers

```bash
git clone https://github.com/beecave-homelab/cloudflare-browser-rendering-cli.git
cd cloudflare-browser-rendering-cli
# Install dependencies (PDM recommended)
pdm install -G dev
# Set your Cloudflare API token in a .env file or as an environment variable
export CLOUDFLARE_API_TOKEN="your-api-token"
# Run the interactive CLI
pdm run cloudflare-render
```

> *Prefer PDM; alternatively, use `pip install .` then run `cloudflare-render`.*

## Version Summary

| Version | Date       | Type | Key Changes                |
|---|---|---|----|
| v0.1.0  | 2025-06-17 | feat ✨   | Initial release of the CLI and API client. |

## Project Features

The CLI and client support the following rendering operations:

- **`content`**: Renders the raw text content of a URL.
- **`screenshot`**: Captures a PNG screenshot of a URL.
- **`pdf`**: Generates a PDF document from a URL.
- **`snapshot`**: Creates a durable snapshot of a page.
- **`scrape`**: Extracts data from a page using a CSS selector.
- **`json`**: Renders a page and returns structured JSON data.
- **`links`**: Extracts all links from a page.
- **`markdown`**: Converts page content to Markdown format.

## Project Structure

<details><summary>Show tree</summary>

```text
.
├── cloudflare_browser_render/ # Main Python package
│   ├── __init__.py
│   ├── cli.py                 # Interactive CLI (Click)
│   ├── client.py              # HTTP client for the API (httpx)
│   ├── config.py              # Configuration loader (dotenv)
│   ├── renderers/             # Modules for each API endpoint
│   │   ├── __init__.py
│   │   ├── content.py
│   │   ├── json.py
│   │   ├── links.py
│   │   ├── markdown.py
│   │   ├── pdf.py
│   │   ├── scrape.py
│   │   ├── screenshot.py
│   │   └── snapshot.py
│   └── utils.py               # Utility functions
├── docs/                      # Project documentation
├── LICENSE
├── pyproject.toml             # Project metadata and dependencies (PDM)
├── README.md
├── requirements.txt           # Pip-formatted dependencies
└── tests/                     # Test suite
    ├── __init__.py
    └── test_imports.py
```

</details>

## Architecture Highlights

- **Layered Structure**: The application is split into a CLI layer (`cli.py`), a business logic layer (`renderers/`), and an API communication layer (`client.py`).
- **Configuration**: Application configuration, like the API token, is loaded from environment variables or a `.env` file via `config.py`.
- **Extensibility**: Each API endpoint is handled by its own module in the `renderers` directory, making it easy to add or modify endpoints.
- **HTTP Client**: Uses `httpx` for sending synchronous POST requests to the Cloudflare API.

## API

The core API interaction is handled by the `call_api` function in `cloudflare_browser_render/client.py`.

- `call_api(endpoint: str, payload: Dict[str, Any]) -> httpx.Response`: Sends a signed POST request to the specified API `endpoint` with the given `payload`. It automatically handles adding the `Authorization` header.

## CLI

The project includes an interactive CLI, accessible via the `cloudflare-render` command.

- **Interactive Mode**: It prompts the user to select an API endpoint and provide a target URL.
- **Endpoint Coverage**: All available renderers are exposed as choices.
- **Output Handling**: Can print results directly to the console or save them to a file, depending on the content type (text vs. bytes).

## Code Quality

Maintain code consistency and catch issues early using the configured linting and formatting tools.

| Tool | Purpose | Typical Command |
|------|---------|-----------------|
| **black** | Opinionated auto-formatter | `pdm run black .` |
| **ruff** | Fast linter & fixer (replaces flake8 + isort) | `pdm run ruff check .` |
| **ruff format** | Ruff's formatter (alternate to black) | `pdm run ruff format .` |

Install the dev extras group first:

```bash
pdm install -G dev
```

Run all checks at once:

```bash
# format and then lint
pdm run black . && pdm run ruff check .
```

> **Tip:** Use `ruff --fix` to auto-apply safe fixes, and configure editors to run `black` on save.

## CI/CD
>
> No CI/CD pipelines are configured for this project.

## Docker
>
> No Docker configuration is present in this project.

## Tests

The test suite is located in the `tests/` directory and uses `pytest`.

- **Current Coverage**: Includes a basic import test (`tests/test_imports.py`) to ensure the CLI command is callable.
- **Installing Test Deps**: `pdm install -G test` (or `pip install pytest pytest-cov`).
- **Running Tests**: Execute `pytest` from the project root.

**Always update this file when code or configuration changes.**
