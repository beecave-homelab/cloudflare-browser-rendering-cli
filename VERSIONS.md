# Versions

## **v0.2.1** (Current) - *October 2025*

🐛 **Bug Fix Release**

### 🔧 **Improvements in v0.2.1**

- **Improved**: Comprehensive docstring coverage with Google-style format for all public functions, classes, and modules
- **Enhanced**: Error handling documentation with proper `Raises:` sections across all CLI commands
- **Updated**: All renderer modules with detailed `Returns:` documentation
- **Refactored**: Import statements from relative to absolute imports (TID252 compliance)
- **Fixed**: Line length violations (E501) throughout codebase
- **Added**: Ruff preview mode with DOC rules (pydoclint) for enhanced docstring validation
- **Updated**: Configuration management with proper exception documentation
- **Improved**: Code quality with consistent PEP 257 and PEP 8 compliance

### 📝 **Documentation Updates**

- **Added**: Comprehensive docstring rules documentation in `project-overview.md`
- **Updated**: CLI aliases documentation (`cbr`, `cloudflare-browser-render`, `cloudflare-browser-rendering`)
- **Enhanced**: Code quality section with docstring rules table
- **Removed**: Deprecated `boilerplate-example.py` from docs

### 🔧 **Configuration**

- **Updated**: `.gitignore` to properly handle output directory with `.gitkeep`
- **Enhanced**: `pyproject.toml` with Ruff preview mode enabled
- **Added**: AGENTS.md with comprehensive coding rules and standards

### 📝 **Key Commits in v0.2.1**

`96fbfa2`, `7b2a0aa`, `794c729`, `e5acc25`, `deb694f`

---

## **v0.1.0** - *June 2025*

🎉 **Initial Release**

### ✨ **New Features**

- **Added**: Interactive CLI (`cloudflare-render`) and Python client for the Cloudflare Browser Rendering API.
- **Added**: Renderer modules for `content`, `screenshot`, `pdf`, `snapshot`, `scrape`, `json`, `links`, and `markdown` endpoints.

### 📝 **Commits**: `740de82`

---

## **v0.2.0** - *June 2025*

✨ **Feature Release**

### ✨ **New Features in v0.2.0**

- **Added**: Cloudflare SDK integration replacing manual HTTP calls.
- **Enhanced**: CLI with global `--debug` flag and improved error handling.
- **Added**: Verification scripts and comprehensive smoke & error tests.

### 🔧 **Improvements in v0.2.0**

- **Updated**: Configuration files (`.env.example`, `.gitignore`, `pyproject.toml`).

### 📝 **Commits**: `203ac3f`, `6e44e2c`, `458a75d`, `315f5b5`, `1205d21`, `9138a89`

---
