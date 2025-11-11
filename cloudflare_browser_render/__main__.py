"""Package entry-point: ``python -m cloudflare_browser_render``.

This thin shim simply forwards control to the Click-based CLI so that the
package can be executed with the ``-m`` flag *and* via the installed
``cloudflare-render`` console script.
"""

from .cli import cli

if __name__ == "__main__":
    # Click's `Command.main` handles argument parsing and will exit
    # appropriately. Using `.main()` avoids the static-analysis complaint
    # about the `ctx` parameter that Click injects at runtime.
    cli.main(prog_name="cloudflare-render")
