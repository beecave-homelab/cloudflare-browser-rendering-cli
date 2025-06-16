from cloudflare_browser_render import cli

def test_cli_exists():
    assert callable(cli)
