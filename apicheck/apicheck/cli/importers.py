import logging
import argparse

from apicheck.core.cli import cli_global_args
from apicheck.core.logging import setup_console_log
from apicheck.core.plugin_loader import load_plugins

logger = logging.getLogger("apicheck")


def cli():
    parser = argparse.ArgumentParser(
        description="API-Check importer commands"
    )

    # Add global options
    cli_global_args(parser)

    subparsers = parser.add_subparsers(dest="importer_type",
                                       description="Valid actions",
                                       help='Actions')

    #
    # Add subparsers
    #
    plugins = load_plugins("sources")

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
        importer_config, importer_function = actions[args.importer_type]
    except KeyError as e:
        print(f"[!] Invalid importer: '{e}'")
        exit(1)

    #
    # Delete 'importer_type' key. Used only for aux keyword in the Cli.
    #
    running_config = args.__dict__
    del running_config["importer_type"]

    #
    # Setup log for console
    #
    setup_console_log(logger, log_level=args.log_level)

    #
    # Launch API Check
    #
    importer_function(importer_config(**running_config))


if __name__ == '__main__':
    cli()
