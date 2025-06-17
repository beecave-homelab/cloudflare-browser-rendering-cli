# To-Do: Add OAuth 2.1 Browser-Based Authentication

This plan outlines the steps to implement a browser-based OAuth 2.1 authentication flow as an alternative to the existing API token method.

## Tasks

- [ ] **Analysis Phase:**
  - [ ] **Research OAuth Libraries:**
    - Path: `pyproject.toml`
    - Action: Evaluate suitable Python libraries for handling the OAuth 2.1 Authorization Code Flow with PKCE (e.g., `authlib`, `requests-oauthlib`).
    - Analysis Results:
      - [ ] `authlib`: Pros/Cons
      - [ ] `requests-oauthlib`: Pros/Cons
    - Accept Criteria: A library is selected and added to the project dependencies.
  - [ ] **Define OAuth Endpoints and Configuration:**
    - Path: `cloudflare_browser_render/config.py`
    - Action: Define the necessary configuration variables for the OAuth flow, such as `AUTHORIZATION_URL`, `TOKEN_URL`, `CLIENT_ID`, `REDIRECT_URI`, and `SCOPES`.
    - Accept Criteria: All required OAuth configuration variables are defined.

- [ ] **Implementation Phase:**
  - [ ] **Implement Core OAuth Flow Logic:**
    - Path: `cloudflare_browser_render/auth.py` (new file)
    - Action: Create a new module to manage the authentication flow. This includes:
      - Generating the authorization URL with PKCE code challenge.
      - Starting a temporary local web server to handle the redirect and capture the authorization code.
      - Exchanging the authorization code for an access token and a refresh token.
    - Status: Pending
  - [ ] **Implement Secure Token Storage:**
    - Path: `cloudflare_browser_render/auth.py`
    - Action: Implement a mechanism to securely store the access and refresh tokens on the user's machine (e.g., using the `keyring` library or a local file with restricted permissions). Implement token refresh logic.
    - Status: Pending
  - [ ] **Integrate OAuth Flow into Configuration:**
    - Path: `cloudflare_browser_render/config.py`
    - Action: Modify `get_api_token()` to first check for the environment variable, and if not found, initiate the new browser-based OAuth flow. The function should retrieve a stored token or start the flow if no valid token exists.
    - Status: Pending
  - [ ] **Update Client to Use New Auth Flow:**
    - Path: `cloudflare_browser_render/client.py`
    - Action: Ensure the `call_api` function transparently uses the token obtained from the updated `get_api_token()` function. No major changes should be needed here if `config.py` is updated correctly.
    - Status: Pending
  - [ ] **Update CLI for Interactive Login:**
    - Path: `cloudflare_browser_render/cli.py`
    - Action: Add logic to inform the user that a browser window is being opened for authentication and handle any potential errors during the process.
    - Status: Pending

- [ ] **Testing Phase:**
  - [ ] **Unit Tests for OAuth Flow:**
    - Path: `tests/test_auth.py` (new file)
    - Action: Write unit tests to mock the OAuth provider and verify the a) authorization URL generation, b) token exchange, and c) secure token storage.
    - Accept Criteria: The OAuth logic is well-tested.
  - [ ] **Integration Test for CLI:**
    - Path: `tests/test_cli.py` (new file or extend existing)
    - Action: Create an integration test that simulates a user running the CLI without an API token, triggering the browser auth flow (mocked), and successfully making an API call.
    - Accept Criteria: The end-to-end flow works as expected from the CLI.

- [ ] **Documentation Phase:**
  - [ ] **Update `README.md`:**
    - Path: `README.md`
    - Action: Document the new browser-based authentication method, explaining how it works and how it differs from the API token method.
    - Accept Criteria: The documentation is clear and accurate.
  - [ ] **Update Project Overview:**
    - Path: `project-overview.md` (or create if not present)
    - Action: Reflect the new authentication architecture in the project overview.
    - Accept Criteria: The overview is up-to-date.

## Related Files

- `cloudflare_browser_render/auth.py` (new)
- `cloudflare_browser_render/config.py`
- `cloudflare_browser_render/client.py`
- `cloudflare_browser_render/cli.py`
- `README.md`
- `pyproject.toml`
- `tests/test_auth.py` (new)
- `tests/test_cli.py`

## Future Enhancements

- [ ] Add a `logout` command to clear stored credentials.
- [ ] Explore using a different local server approach if the temporary one proves problematic on some systems.
