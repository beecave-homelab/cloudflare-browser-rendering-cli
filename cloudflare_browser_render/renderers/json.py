"""JSON endpoint renderer."""

from ..client import get_client
from ..config import get_account_id
from ..utils import call_with_retry

_cf = get_client()
_account_id = get_account_id()


def render_json(url: str) -> dict:
    """Render *url* into structured JSON data."""
    # The JSON endpoint requires either a `prompt` or a `response_format`.
    # We use an extremely permissive JSON schema as a sensible default so
    # that users can still fetch structured data without having to supply
    # extra arguments.

    default_schema = {"type": "json_schema", "json_schema": {"type": "object"}}

    raw = call_with_retry(
        lambda: _cf.browser_rendering.json.with_raw_response.create(
            account_id=_account_id,
            url=url,
            response_format=default_schema,
        )
    )
    return raw.json()
