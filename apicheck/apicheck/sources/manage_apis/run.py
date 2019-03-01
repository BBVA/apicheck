"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""

import asyncio

from terminaltables import AsciiTable, DoubleTable, SingleTable

from apicheck.db import get_engine, setup_db_engine, APIMetadata
from apicheck.exceptions import APICheckException

from .model import RunningConfig


# -------------------------------------------------------------------------
# Main saving methods
# -------------------------------------------------------------------------
async def list_apis(running_config: RunningConfig) -> APICheckException:
    """Save definition into database"""

    try:
        connection = await get_engine().connect()

        results = await connection.execute(APIMetadata.select())
        apis: list = await results.fetchall()

    except Exception as e:
        raise APICheckException(f"Error accessing to database: {e}")

    #
    # Adding Title
    #
    apis.insert(0, ("ID", "API Name", "Version"))

    # -------------------------------------------------------------------------
    # Printing results
    # -------------------------------------------------------------------------
    table_instance = AsciiTable(apis, "- API Info --")
    table_instance.justify_columns[0] = 'center'
    table_instance.justify_columns[1] = 'center'
    table_instance.justify_columns[2] = 'center'

    print()
    print(table_instance.table)
    print()


def run(running_config: RunningConfig):

    # -------------------------------------------------------------------------
    # Setup database
    # -------------------------------------------------------------------------
    setup_db_engine(running_config.db_connection_string)

    # -------------------------------------------------------------------------
    # Select action
    # -------------------------------------------------------------------------
    if running_config.api_action == "list":
        action = list_apis
    else:
        raise ValueError("Invalid action selected")

    # -------------------------------------------------------------------------
    # Run action
    # -------------------------------------------------------------------------
    loop = asyncio.get_event_loop()
    loop.run_until_complete(action(
        running_config
    ))
