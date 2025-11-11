# To-Do: Add Missing Docstrings to Codebase

This plan outlines the steps to add missing docstrings to public modules, functions, and classes as identified by Ruff's pydocstyle checks.

## Tasks

- [x] **Analysis Phase:**
  - [x] Run Ruff to find all missing docstrings
    - Path: `cloudflare_browser_render/`, `tests/`
    - Action: `pdm run ruff check --select D .`
    - Analysis Results:
      - Ruff found 32 violations, of which 22 are missing docstrings (`D100`, `D103`, `D104`) and 10 are auto-fixable formatting issues.
    - Accept Criteria: A complete list of files and functions requiring docstrings is generated.

- [ ] **Implementation Phase:**
  - [x] **Step 1: Auto-fix formatting issues**
    - Path: `./`
    - Action: Run `pdm run ruff check --fix --select D .` to automatically correct formatting violations (D202, D209, D413).
    - Status: Completed

  - [x] **Step 2: Add docstrings to CLI functions**
    - Path: `cloudflare_browser_render/cli.py`
    - Action: Add missing `D103` docstrings to the public functions: `screenshot`, `pdf`, `snapshot`, `scrape`, `json_`, `links`, `markdown`.
    - Status: Completed

  - [x] **Step 3: Add docstrings to renderer functions**
    - Path: `cloudflare_browser_render/renderers/`
    - Action: Add missing `D103` docstrings to all `render_*` functions in the 8 renderer modules.
    - Status: Completed

  - [x] **Step 4: Add docstrings to utility functions**
    - Path: `cloudflare_browser_render/utils.py`
    - Action: Add missing `D103` docstrings to public functions: `save_bytes`, `save_text`, `print_json`.
    - Status: Completed

  - [x] **Step 5: Add docstrings to test files**
    - Path: `tests/`
    - Action: Add missing module/package/function docstrings (`D100`, `D104`, `D103`) to `tests/__init__.py`, `tests/test_imports.py`, and `tests/test_cli_smoke.py`.
    - Status: Completed
    - Note: Tests now pass docstring linting.

  - [x] **Step 6: Fix docstring style issues in docs & scripts**
    - Path: `docs/boilerplate-example.py`, `scripts/manual_verification.py`
    - Action: Address D400, D401, D415 and add missing docstrings so that `ruff check --select D .` reports zero errors.
    - Status: Completed

- [x] **Testing Phase:**
  - [x] **Verify all docstring issues are resolved**
    - Path: `./`
    - Action: Run `pdm run ruff check --select D .` again to confirm that no `D` violations remain.
    - Accept Criteria: The command exits with a success code and reports zero errors.
    - Status: Completed (verified on DATE)

- [x] **Documentation Phase:**
  - [x] **Update project overview**
    - Path: `project-overview.md`
    - Action: Updated 'Code Quality' section with details on docstring rules.
    - Accept Criteria: `project-overview.md` reflects docstring rule enhancements.
    - Status: Completed

## Related Files

- `cloudflare_browser_render/cli.py`
- `cloudflare_browser_render/client.py`
- `cloudflare_browser_render/utils.py`
- `cloudflare_browser_render/renderers/content.py`
- `cloudflare_browser_render/renderers/json.py`
- `cloudflare_browser_render/renderers/links.py`
- `cloudflare_browser_render/renderers/markdown.py`
- `cloudflare_browser_render/renderers/pdf.py`
- `cloudflare_browser_render/renderers/scrape.py`
- `cloudflare_browser_render/renderers/screenshot.py`
- `cloudflare_browser_render/renderers/snapshot.py`
- `tests/__init__.py`
- `tests/test_cli_smoke.py`
- `tests/test_imports.py`

## Future Enhancements

- [ ] Configure a pre-commit hook to run ruff checks automatically to prevent future regressions.
