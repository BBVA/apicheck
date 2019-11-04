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
        description="Launches a local proxy to track API requests"
    )

    # Add global options
    cli_db(parser)
    cli_log_level(parser)

    parser.add_argument('domain',
                        metavar="domain",
                        nargs="*",
                        help="Domain to inspect using proxy")
    parser.add_argument('-l', '--listen',
                        dest="listen_addr",
                        default="127.0.0.1",
                        help="proxy listen address (default: 127.0.0.1)")
    parser.add_argument('-p', '--port',
                        dest="listen_port",
                        help="proxy listen port (default: 8080)")
    parser.add_argument('--store-assets',
                        action="store_true",
                        default=False,
                        dest="store_assets_content",
                        help="store assets content in database")
    parser.add_argument('-a', '--learning_mode',
                        action="store_true",
                        default=False,
                        dest="learning_mode",
                        help="enable learning mode to introspect the "
                             "REST API")
    parser.add_argument('--promiscuous',
                        action="store_true",
                        default=False,
                        dest="promiscuous",
                        help="save all requests that passthroughs "
                             "the proxy")

    #
    # Parse cli
    #
    args = parser.parse_args()

    #
    # Build config from CLI args
    #
    running_config = RunningConfig(**args.__dict__)

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


if __name__ == '__main__':
    cli()

