import click

from click.testing import CliRunner

from apitest.actions.cli import cli

import apitest.actions.compare.console


def _launch_apitest_comparer_console(blah, **kwargs):
    click.echo("ok")
    

def test_cli_compare_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["compare"])
    
    assert 'compare [OPTIONS] API_OLD_CONNECTION_STRING\n                   API_CURRENT_CONNECTION_STRING'\
           in result.output
    assert 'Usage:' in result.output


def test_cli_compare_runs_ok():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.compare.cli.launch_apitest_comparer_console = _launch_apitest_comparer_console
    
    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "old_connection_string", "new_connection_string"])
    
    assert 'ok' in result.output
