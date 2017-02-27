from click.testing import CliRunner
from apitest.actions.parser.postman.cli import cli_parser


def test_parser_cli_runs_ok():
    runner = CliRunner()
    result = runner.invoke(cli_parser, ["-h"])
    
    assert result.exit_code == 0
