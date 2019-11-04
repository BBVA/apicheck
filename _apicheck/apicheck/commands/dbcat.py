import sys
import asyncio
import argparse

from apicheck.core.cli import cli_db
from apicheck.db import setup_db_engine
from apicheck.core.db_utils import get_proxy_logs


def main():
    parser = argparse.ArgumentParser(
        description="concatenate and print APIs from database"
    )
    parser.add_argument('API_AND_VERSION',
                        nargs="?",
                        help="API name and version in format: Name:Version")
    parser.add_argument('-P',
                        action="store_true",
                        default=False,
                        dest="indent",
                        help="indent json result file")

    #
    # Add database options
    #
    cli_db(parser)

    parsed = parser.parse_args()

    # -------------------------------------------------------------------------
    # Configure database
    # -------------------------------------------------------------------------
    setup_db_engine(parsed.db_connection_string)

    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(get_proxy_logs(1))

    print(x)

    if parsed.YAML_FILE:

        with open(parsed.YAML_FILE, "r") as f:
            input_content = f.read()
    else:
        input_content = sys.stdin.read()


if __name__ == '__main__':
    main()
