from click.testing import CliRunner
from apitest.actions.cli import cli


def test_unittest_cli_runs_ok():
    runner = CliRunner()
    result = runner.invoke(cli, ["unittest"])
    
    assert result.exit_code == 0
