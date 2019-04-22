import logging
import argparse

from apicheck.db import setup_db_engine
from apicheck.core.cli import cli_db, cli_log_level
from apicheck.core.logging import setup_console_log

from .apis.cli import cli as cli_apis
from .create_plugin.cli import cli as cli_create_plugin
from .api_definition_formats.cli import cli as cli_definitions

from .apis.run import run as run_apis
from .create_plugin.run import run as run_create_plugin
from .api_definition_formats.run import run as run_definitions

from .apis.config import RunningConfig as ConfigAPIs
from .create_plugin.config import RunningConfig as ConfigCreatePlugin
from .api_definition_formats.config import RunningConfig as ConfigDefinition

logger = logging.getLogger("apicheck")

ACTION_MAP = {
    'api': (run_apis, ConfigAPIs),
    'create-plugin': (run_create_plugin, ConfigCreatePlugin),
    'definition': (run_definitions, ConfigDefinition)
}


def cli():
    parser = argparse.ArgumentParser(
        description="API-Check manage commands"
    )

    # Add global options
    cli_db(parser)
    cli_log_level(parser)

    subparsers = parser.add_subparsers(dest="option",
                                       description="Valid options",
                                       help='Actions')

    #
    # Add subparsers
    #
    cli_apis(subparsers)
    cli_create_plugin(subparsers)
    cli_definitions(subparsers)

    #
    # Parse cli
    #
    args = parser.parse_args()

    #
    # Choice correct config object
    try:
        config, run_function = ACTION_MAP[args.option]
    except KeyError as e:
        print(f"[!] Invalid importer: '{e}'")
        exit(1)

    #
    # Delete 'importer_type' key. Used only for aux keyword in the Cli.
    #
    cli_config = args.__dict__
    del cli_config["option"]

    #
    # Build config
    #
    running_config = config(**cli_config)

    #
    # Setup log for console
    #
    setup_console_log(logger, log_level=args.log_level)

    #
    # Setup db
    #
    if ":" in running_config.db_connection_string:
        setup_db_engine(running_config.db_connection_string)

    #
    # Launch API Check
    #
    run_function(running_config)


if __name__ == '__main__':
    cli()
