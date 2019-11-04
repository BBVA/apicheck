import logging
import argparse

from apicheck.db import setup_db_engine
from apicheck.core.cli import cli_db, cli_log_level
from apicheck.core.logging import setup_console_log

from .run import run
from .config import RunningConfig

logger = logging.getLogger("apicheck")


def cli():
    parser = argparse.ArgumentParser(
        description="Send API definition to proxy"
    )

    # Add global options
    cli_db(parser)
    cli_log_level(parser)

    parser.add_argument('api_id',
                        help="api definition ID to send")
    parser.add_argument('--source',
                        dest="source",
                        default="definition",
                        choices=RunningConfig.OPERATION_MODES,
                        help="origin of data. Default: definition")
    parser.add_argument('--proxy',
                        dest="proxy_destination",
                        required=True,

                        help="proxy destination. IP:PORT")

    c = parser.add_argument_group("API Definitions")
    c.add_argument("--api-url",
                   dest="api_url",
                   help="api base url used for requests")

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
