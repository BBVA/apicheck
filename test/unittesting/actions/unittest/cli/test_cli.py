from click.testing import CliRunner
from apitest.actions.sendto.cli import sendto


def test_unittest_cli_runs_ok():
    runner = CliRunner()
    result = runner.invoke(sendto, ["-h"])
    
    assert result.exit_code == 0
