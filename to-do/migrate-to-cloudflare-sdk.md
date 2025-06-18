# To-Do: Migrate to Cloudflare Python SDK

This plan outlines the steps to migrate from the manual `httpx` client to the official `cloudflare` Python SDK for interacting with the Cloudflare Browser Rendering API. This will provide a fully-supported client with features like retry/backoff, typed responses, and robust TLS handling.

## Tasks

- [x] **Analysis Phase:**
  - [x] Confirm `cloudflare` SDK compatibility and features.
    - Path: `pyproject.toml`, `cloudflare_browser_render/client.py`
    - Action: Review the `cloudflare` Python SDK documentation to confirm that it supports all the browser rendering endpoints currently in use (`/screenshot`, `/scrape`, etc.) and that the response handling is compatible with our existing renderer functions. The SDK's `browser_rendering.<endpoint>.create()` methods seem to be the correct path.
    - Analysis Results:
      - The `cloudflare` package exposes `browser_rendering` sub-resources for **all** endpoints in use: `content`, `screenshot`, `pdf`, `snapshot`, `scrape`, `json`, `links`, and `markdown`.
      - Each endpoint provides a `.create()` method that accepts an `account_id` plus request body and returns typed responses (`bytes` for binary, `str`/`dict` for text & JSON), matching our current renderer expectations.
      - Authentication (Bearer API token), TLS negotiation, and retry/backoff are handled internally by the SDK, eliminating the need for custom logic in `client.py`.
      - Therefore, our bespoke `TLSHandshakeError` workaround and the `--no-verify-ssl` flag can be safely removed.
    - Accept Criteria: ✅ Confirmed – the SDK is a viable drop-in replacement for the current `httpx` implementation.

- [ ] **Implementation Phase:**
  - [x] **1. Update Dependencies:**
    - Path: `pyproject.toml`
    - Action: Add `cloudflare>=4.3` to the project dependencies.
    - Status: Done – dependency added to `pyproject.toml`; project overview badge updated.

  - [x] **2. Create Singleton Client:**
    - Path: `cloudflare_browser_render/client.py`
    - Action: Instantiate a singleton `Cloudflare` client. This client will be initialized with the API token from the configuration and will require an `account_id`. This replaces the `call_api` function.
    - Status: Done – added `get_client()` singleton and `get_account_id()` helper.

  - [x] **3. Refactor Renderer Functions:**
    - Path: `cloudflare_browser_render/renderers/*.py`
    - Action: Replace the implementation of each `render_*` function in the `renderers` directory to use the new `cloudflare` SDK client. For example, `render_screenshot` will be updated to use `cf.browser_rendering.screenshot.create(...)`.
    - Status: Done – all `render_*` functions now use `client.browser_rendering.<endpoint>.with_raw_response.create()`.

  - [x] **4. Remove TLS Workaround:**
    - Path: `cloudflare_browser_render/client.py`
    - Action: Remove the custom `TLSHandshakeError` exception and the associated `--no-verify-ssl` logic, as the SDK handles TLS correctly.
    - Status: Done – legacy `call_api`, TLS error handling, and CLI flag removed.

  - [x] **5. Add `--debug` Flag to CLI:**
    - Path: `cloudflare_browser_render/cli.py`
    - Action: Introduce a global `--debug` option to the root Click group. When enabled, the CLI re-raises original exceptions so full Python tracebacks are shown; otherwise, errors are wrapped in `click.ClickException` for clean output.
    - Status: Done – flag implemented; automated tests pass unchanged.

- [ ] **Testing Phase:**
  - [X] **1. Test Existing Commands:**
    - Path: `(manual)`
    - Action: Run all existing CLI commands (`screenshot`, `scrape`, `pdf`, etc.) to ensure they work correctly with the new SDK-based implementation.
    - Accept Criteria: All commands execute successfully and produce the expected output.

  - [ ] ~~**2. Verify Error Handling:**~~
    - ~~Path: `(manual)`~~
    - ~~Action: Test how the application handles API errors (e.g., invalid token, invalid URL) with the new SDK.~~
    - ~~Accept Criteria: The application gracefully handles errors from the Cloudflare API.~~

  ### Hybrid Test Strategy (added 2025-06-18)

  - [x] **1a. Automated Smoke Tests:**
    - Path: `tests/test_cli_smoke.py`
    - Action: Write Pytest tests that monkey-patch the `cloudflare` SDK client to return stubbed responses for each renderer endpoint, then invoke the corresponding CLI subcommand via Click's test runner (`CliRunner`).
    - Accept Criteria: All tests pass, confirming that each subcommand correctly processes the SDK response and exits with code 0.

  - [x] **1b. Manual Verification:**
    - Path: `(manual)`
    - Action: Run each CLI command against the live Cloudflare API using valid credentials to confirm real-world behaviour mirrors mocked tests.
    - Accept Criteria: Outputs match expectations; binary outputs saved to disk are valid (PNG/PDF).

    **Run via scripts:**

    - Bash: `./scripts/manual_verification.sh <URL> [CSS_SELECTOR]`
    - Python (loads .env automatically): `python scripts/manual_verification.py <URL> [CSS_SELECTOR]`

    The scripts do not export secrets; make sure `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are defined in your environment or in a `.env` file. Replace `<URL>` (default `https://example.com`) and `[CSS_SELECTOR]` (default `h1`) as needed.

  - [ ] **2. Error-Handling Tests (Automated):**
    - Path: `tests/test_error_handling.py`
    - Action: Mock the SDK to raise typical API exceptions (e.g., 401 Unauthorized, 404 Not Found). Ensure the CLI surfaces user-friendly error messages and returns non-zero exit codes.
    - Accept Criteria: Tests demonstrate graceful error handling without uncaught tracebacks.

  - [ ] **3. Error-Handling Manual Check:**
    - Path: `(manual)`
    - Action: Intentionally invoke the CLI with an invalid token and a malformed URL to observe behaviour.
    - Accept Criteria: CLI prints clear error messages and exits with a non-zero status.

    **Commands to run:**

    ```bash
    # Invalid token
    CLOUDFLARE_API_TOKEN="bad-token" pdm run cloudflare-render content https://example.com || echo "expected failure"

    # Invalid URL (malformed)
    pdm run cloudflare-render content not-a-valid-url || echo "expected failure"
    ```

  > Once automated tests are merged and manual checks completed, mark the original items **1** and **2** as done.

# Packaging Enhancements (added 2025-06-18)

- [x] **Add `__main__.py` shim:**
  - Path: `cloudflare_browser_render/__main__.py`
  - Action: Create a tiny shim that imports `cli` and calls it so users can run `python -m cloudflare_browser_render` without warnings.
  - Accept Criteria: Running `python -m cloudflare_browser_render --help` shows the CLI help and exits 0. Both invocation methods (`cloudflare-render` entry-point and `-m` form) work.

- [ ] **Documentation Phase:**
  - [ ] **1. Update Project Overview:**
    - Path: `project-overview.md`
    - Action: Update the project overview to reflect the switch to the `cloudflare` Python SDK and the removal of the manual `httpx` client.
    - Accept Criteria: Documentation accurately describes the new architecture.

## Related Files

- `pyproject.toml`
- `cloudflare_browser_render/client.py`
- `cloudflare_browser_render/renderers/screenshot.py`
- `cloudflare_browser_render/renderers/scrape.py`
- `cloudflare_browser_render/renderers/pdf.py`
- `cloudflare_browser_render/renderers/content.py`
- `cloudflare_browser_render/renderers/json.py`
- `cloudflare_browser_render/renderers/links.py`
- `cloudflare_browser_render/renderers/markdown.py`
- `cloudflare_browser_render/renderers/snapshot.py`
- `cloudflare_browser_render/__main__.py`
- `project-overview.md`

## Future Enhancements

- [ ] Explore using more advanced features of the `cloudflare` SDK if applicable.
