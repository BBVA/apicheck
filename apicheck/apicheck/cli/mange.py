import logging
import argparse

from apicheck.db import setup_db_engine
from apicheck.core.cli import cli_global_args
from apicheck.core.logging import setup_console_log
from apicheck.core.plugin_loader import load_plugins

logger = logging.getLogger("apicheck")


def cli():
    parser = argparse.ArgumentParser(
        description="API-Check manage commands"
    )

    # Add global options
    cli_global_args(parser)

    subparsers = parser.add_subparsers(dest="option",
                                       description="Valid options",
                                       help='Actions')

    #
    # Add subparsers
    #
    plugins = load_plugins("manage")

    already_loaded = set(subparsers.choices.keys())
    actions = {}
    for plugin_name, (cli_args, conf, fn) in plugins.items():
        cli_args(subparsers)

        #
        # Induce the new command added to the cli command line and add new
        # actions to them. Yes, It's not so elegant. Ideas are welcome.
        #
        # TODO: Improve that
        #
        plugin_action_name = "".join(set(subparsers.choices.keys()).difference(
            already_loaded
        ))
        already_loaded.add("".join(plugin_action_name))

        actions[plugin_action_name] = [conf, fn]

    #
    # Parse cli
    #
    args = parser.parse_args()

    #
    # Choice correct config object
    try:
        config, function = actions[args.option]
    except KeyError as e:
        print(f"[!] Invalid importer: '{e}'")
        exit(1)

    #
    # Delete 'importer_type' key. Used only for aux keyword in the Cli.
    #
    running_config = args.__dict__
    del running_config["option"]

    #
    # Setup log for console
    #
    setup_console_log(logger, log_level=args.log_level)

    #
    # Build config
    #
    obj_config = config(**running_config)

    #
    # Setup db
    #
    setup_db_engine(obj_config.db_connection_string)

    #
    # Launch API Check
    #
    function(obj_config)
    #
    # Launch API Check
    #
    function(config(**running_config))


if __name__ == '__main__':
    cli()
