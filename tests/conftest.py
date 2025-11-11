import os

# Ensure CI/test environment has the required variables without a .env file.
os.environ.setdefault("CLOUDFLARE_API_TOKEN", "test-token")
os.environ.setdefault("CLOUDFLARE_ACCOUNT_ID", "test-account")
