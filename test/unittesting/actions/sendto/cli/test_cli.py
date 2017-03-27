from click.testing import CliRunner
from apitest.actions.unittest.cli import unittest


def test_sendto_cli_runs_ok():
    runner = CliRunner()
    result = runner.invoke(unittest, ["-h"])
    
    assert result.exit_code == 0
