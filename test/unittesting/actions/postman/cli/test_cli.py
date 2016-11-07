from click.testing import CliRunner
from apitest.actions.parser.postman.cli import cli_postman


def test_parser_cli_runs_ok():
    runner = CliRunner()
    result = runner.invoke(cli_postman, ["-h"])
    
    assert result.exit_code == 0
