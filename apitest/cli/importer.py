from ..actions import run
from .common_args import common_cli_args
from ..running_config import build_config_from_argparser


def cli_add_importers(subparsers):

    #
    # Import from OpenAPI
    #
    open_api = subparsers.add_parser('openapi', help='import from OpenAPI 3')
    open_api.add_argument('yaml_file', help="YAML file path")


def cli():
    parser = common_cli_args("Importer APITest commands")
    subparsers = parser.add_subparsers(dest="importer_type",
                                       description="Valid actions",
                                       help='Actions')
    cli_add_importers(subparsers)

    #
    # Parse cli
    #
    args = parser.parse_args()

    #
    # Choice correct config object
    #
    config = build_config_from_argparser(args)

    #
    # Launch API Test
    #
    run(config)


if __name__ == '__main__':
    cli()
