import logging
import argparse

from apicheck.db import setup_db_engine
from apicheck.core.logging import setup_console_log
from apicheck.core.cli import cli_db, cli_log_level

from .run import run
from .config import RunningConfig

logger = logging.getLogger("apicheck")


def cli():
    parser = argparse.ArgumentParser(
        description="Generate a dataset from proxy traffic"
    )
    parser.add_argument('fout',
                        help="output file to store results")

    # Add global options
    cli_db(parser)
    cli_log_level(parser)

    #
    # Parse cli
    #
    args = parser.parse_args()

    #
    # Build config from CLI args
    #
    running_config = RunningConfig(args.__dict__)

    #
    # Setup log for console
    #
    setup_console_log(logger, log_level=running_config.log_level)

    #
    # Setup db
    #
    setup_db_engine(running_config.db_connection_string)

    #
    # Launch
    #
    run(running_config)
