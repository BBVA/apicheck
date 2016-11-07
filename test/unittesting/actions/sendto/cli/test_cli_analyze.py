import click
import pytest

from click.testing import CliRunner

from apitest.actions.unittest.cli import analyze

import apitest.actions.unittest.analyze.console


def _launch_apitest_generate_load_in_console(blah, **kwargs):
    click.echo("ok")
    

def test_cli_analyze_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(analyze)
    
    assert 'Missing argument "file_path"' in result.output


def test_sendto_cli_analyze_runs_ok():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.unittest.cli.launch_apitest_generate_load_in_console = _launch_apitest_generate_load_in_console
    
    runner = CliRunner()
    result = runner.invoke(analyze, ["sssss"])
    
    assert result.output == "ok\n"
