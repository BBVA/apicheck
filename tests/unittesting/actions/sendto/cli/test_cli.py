from click.testing import CliRunner
from apitest.actions.cli import cli


def test_sendto_cli_runs_ok():
    runner = CliRunner()
    result = runner.invoke(cli, ["sendto"])
    
    assert result.exit_code == 0
