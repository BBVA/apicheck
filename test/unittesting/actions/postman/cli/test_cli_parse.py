import click

from click.testing import CliRunner

from apitest.actions.cli import cli

import apitest.actions.parser.postman.parse.console


def _launch_apitest_postman_parse_in_console(blah, **kwargs):
    click.echo("ok")


def test_cli_analyze_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["parse", "postman", "analyze"])
    
    assert 'postman analyze [OPTIONS] FILE_PATH' in result.output
    assert 'Usage:' in result.output


def test_cli_postman_analyze_runs_ok():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.parser.postman.cli.launch_apitest_postman_parse_in_console = _launch_apitest_postman_parse_in_console
    
    runner = CliRunner()
    result = runner.invoke(cli, ["parse", "postman", "analyze", "asdf"])
    
    assert 'ok' in result.output
