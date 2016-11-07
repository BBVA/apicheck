import click

from click.testing import CliRunner

from apitest.actions.comparer.cli import compare

import apitest.actions.comparer.console


def _launch_apitest_comparer_console(blah, **kwargs):
    click.echo("ok")
    

def test_cli_analyze_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(compare)
    
    assert 'Usage: compare [OPTIONS] API_OLD_CONNECTION_STRING API_CURRENT_CONNECTION_STRING' in result.output


def test_cli_postman_analyze_runs_ok():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.comparer.cli.launch_apitest_comparer_console = _launch_apitest_comparer_console
    
    runner = CliRunner()
    result = runner.invoke(compare, ["old_connection_string", "new_connection_string"])
    
    assert 'ok' in result.output
