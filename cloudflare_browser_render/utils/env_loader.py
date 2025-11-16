"""Environment loading utilities for the CLI."""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv


@lru_cache(maxsize=1)
def load_project_env() -> dict[str, str]:
    """Load environment variables once for the entire application."""
    load_dotenv()
    return dict(os.environ)
