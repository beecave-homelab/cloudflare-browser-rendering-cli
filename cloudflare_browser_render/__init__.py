"""Cloudflare Browser Rendering CLI package."""

__all__ = ["cli"]


def cli(*args, **kwargs):
    """Deferred CLI entry point.

    Importing heavy dependencies is delayed until runtime so that the package
    can be imported without having all optional third-party modules installed.
    """

    from .cli import cli as real_cli

    return real_cli(*args, **kwargs)
