"""Environment loading utilities for the CLI.

Discovers and loads a ``.env`` file from the first matching location in a
deterministic order, then returns a snapshot of the process environment.

Discovery order (first existing file wins):

1. ``~/.config/cloudflare-browser-rendering-cli/.env``
2. ``~/.config/cbr/.env``
3. ``${PWD}/.env``

By default already-exported process environment variables are preserved
(``override=False``).  Pass ``override=True`` to let ``.env`` values replace
existing variables.

Diagnostics expose only safe metadata (loaded/not loaded, path, key count).
No environment values are ever returned in diagnostics or in the repr.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Deterministic discovery order: first existing file wins.
_ENV_SEARCH_PATHS: tuple[str, ...] = (
    "~/.config/cloudflare-browser-rendering-cli/.env",
    "~/.config/cbr/.env",
    ".env",  # resolved against PWD at call time
)


def _find_env_file() -> Path | None:
    """Return the first existing ``.env`` path from the discovery order.

    Returns:
        The first matching ``Path`` or ``None`` when no candidate exists.
    """
    for candidate in _ENV_SEARCH_PATHS:
        resolved = Path(candidate).expanduser()
        if resolved.is_file():
            return resolved.resolve()
    return None


@dataclass(frozen=True, repr=False)
class EnvLoadResult:
    """Immutable result of a ``load_project_env`` call.

    The ``env`` dict holds the environment snapshot needed by callers.
    The remaining fields and ``diagnostics`` property expose only safe
    metadata, never values.

    Attributes:
        env: Snapshot of the process environment after loading.
        loaded: Whether a ``.env`` file was found and loaded.
        path: Path of the loaded file, or ``None`` when no file was found.
        key_count: Number of keys in ``env``.
    """

    env: dict[str, str] = field(default_factory=dict)
    loaded: bool = False
    path: Path | None = None
    key_count: int = 0

    @property
    def diagnostics(self) -> dict[str, str | int | bool | None]:
        """Safe diagnostic metadata without environment values.

        Returns:
            A dict with ``loaded``, ``path``, and ``key_count`` keys.
            No environment values are included.
        """
        return {
            "loaded": self.loaded,
            "path": str(self.path) if self.path else None,
            "key_count": self.key_count,
        }

    def __repr__(self) -> str:
        """Return a safe repr without environment values."""
        return (
            f"EnvLoadResult(loaded={self.loaded}, "
            f"path={self.path!r}, key_count={self.key_count})"
        )


@lru_cache(maxsize=2)
def load_project_env(override: bool = False) -> EnvLoadResult:
    """Load environment variables once for the entire application.

    Searches for a ``.env`` file in a deterministic order and loads it via
    ``python-dotenv``.  By default already-exported process variables are
    preserved; pass ``override=True`` to replace them with file values.

    The result is cached per ``override`` value so that a non-override call
    can never be reused for an override call (and vice versa).

    Args:
        override: When ``True``, ``.env`` values overwrite existing process
            environment variables.  Defaults to ``False``.

    Returns:
        An ``EnvLoadResult`` with the environment snapshot and safe
        diagnostics.  No values are exposed in the diagnostics or repr.
    """
    path = _find_env_file()
    if path is not None:
        load_dotenv(dotenv_path=path, override=override)
    env_snapshot = dict(os.environ)
    return EnvLoadResult(
        env=env_snapshot,
        loaded=path is not None,
        path=path,
        key_count=len(env_snapshot),
    )
