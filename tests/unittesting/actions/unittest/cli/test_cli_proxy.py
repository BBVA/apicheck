import click
import pytest

from click.testing import CliRunner

from apitest.actions.sendto.cli import proxy

import apitest.actions.sendto.proxy.console


def _launch_apitest_sento_proxy_console(blah, **kwargs):
    click.echo("ok")
    

def test_unittest_cli_analyze_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(proxy)
    
    assert 'Usage: proxy [OPTIONS] APITEST_FILE' in result.output


def test_unittest_cli_analyze_runs_ok():
    # Patch the launch of: launch_apitest_sento_proxy_console
    apitest.actions.sendto.cli.launch_apitest_sento_proxy_console = _launch_apitest_sento_proxy_console
    
    runner = CliRunner()
    result = runner.invoke(proxy, ["sssss"])
    
    assert result.output == "ok\n"
