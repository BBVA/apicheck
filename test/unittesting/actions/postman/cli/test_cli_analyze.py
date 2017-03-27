import click

from click.testing import CliRunner

from apitest.actions.cli import cli

import apitest.actions.parser.postman.analyze.console


def _launch_apitest_postman_analyze_in_console(blah, **kwargs):
    click.echo("ok")
    

def test_cli_analyze_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["parser", "postman", "analyze"])
    
    assert 'Usage: ' in result.output


def test_cli_postman_analyze_runs_ok():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.parser.postman.cli.launch_apitest_postman_analyze_in_console = _launch_apitest_postman_analyze_in_console
    
    runner = CliRunner()
    result = runner.invoke(cli, ["parse", "postman", "analyze", "file_path"])
    
    assert 'ok' in result.output
