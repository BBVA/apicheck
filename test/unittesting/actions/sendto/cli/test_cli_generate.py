import click

from click.testing import CliRunner

from apitest.actions.unittest.cli import generate

import apitest.actions.unittest.analyze.console


def _launch_apitest_generate_unittest_in_console(blah, **kwargs):
    click.echo("ok")
    

def test_cli_analyze_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(generate)
    
    assert 'Missing argument "file_path"' in result.output


def test_sendto_cli_analyze_runs_missing_options():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.unittest.cli.launch_apitest_generate_unittest_in_console = _launch_apitest_generate_unittest_in_console
    
    runner = CliRunner()
    result = runner.invoke(generate, ["sssss"])
    
    assert 'Error: Missing option "-o" / "--output-dir"' in result.output


def test_sendto_cli_analyze_runs_ok_with_options():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.unittest.cli.launch_apitest_generate_unittest_in_console = _launch_apitest_generate_unittest_in_console
    
    runner = CliRunner()
    result = runner.invoke(generate, ["-o", "xxxx", "sssss"])
    
    assert result.output == "ok\n"
