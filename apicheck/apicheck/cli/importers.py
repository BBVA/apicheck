import argparse

from apicheck.sources.proxy import cli_args_proxy
from apicheck.sources.api_definition_formats import cli_args_api_definitions
from apicheck.sources.manage_apis import cli_args_api_manage

from apicheck.sources.proxy import ProxyConfig, launch_apicheck_proxy
from apicheck.sources.api_definition_formats import APIDefinitionsConfig, \
    run_load_api_definitions
from apicheck.sources.manage_apis import APIManageConfig, run_manage_apis

IMPORTERS = {
    "proxy": (ProxyConfig, launch_apicheck_proxy),
    "definition": (APIDefinitionsConfig, run_load_api_definitions),
    "manage": (APIManageConfig, run_manage_apis)
}


def cli():
    parser = argparse.ArgumentParser(
        description="API-Check importer commands"
    )
    parser.add_argument('-C', '--connection-string',
                        dest="db_connection_string",
                        required=True,
                        help="database connection string")
    subparsers = parser.add_subparsers(dest="importer_type",
                                       description="Valid actions",
                                       help='Actions')

    #
    # Add subparsers
    #
    cli_args_proxy(subparsers)
    cli_args_api_definitions(subparsers)
    cli_args_api_manage(subparsers)

    #
    # Parse cli
    #
    args = parser.parse_args()

    #
    # Choice correct config object
    #
    try:
        importer_config, importer_function = IMPORTERS[args.importer_type]
    except KeyError as e:
        print(f"[!] Invalid importer: '{e}'")
        exit(1)

    running_config = args.__dict__
    running_config.pop("importer_type")

    #
    # Launch API Check
    #
    importer_function(importer_config(**running_config))


if __name__ == '__main__':
    cli()
