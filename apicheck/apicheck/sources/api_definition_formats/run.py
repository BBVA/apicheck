"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""

import re
import asyncio

from typing import Tuple
from urllib.parse import urlparse
from sqlalchemy import and_

from apicheck.db import get_engine, APIDefinitions, setup_db_engine, \
    APIMetadata

from .model import APIDefinitionsConfig, DefinitionsFormats


def _extract_api_version_from_openapi_3(content) -> Tuple[str, str]:
    regex_openapi_3_version = r"""(version\:)([\s]*)([\d\\.]+)"""
    regex_openapi_3_api_name = \
        r"""(servers\:[\n\r]+[\s]*-[\s]*)(url:[\s]*)([0-9\.\/\w\:]+)"""

    name = version = None

    v = re.search(regex_openapi_3_version, content)
    if v:
        version = v.group(3)
    n = re.search(regex_openapi_3_api_name, content)
    if n:
        name = urlparse(n.group(3)).hostname

    return name, version


def extract_api_version(
        content: str,
        running_config: APIDefinitionsConfig) -> Tuple[str, str]:
    """
    Extract API version / name from the definition file

    :return: return format: Tuple[NAME, VERSION]
    """

    input_format = running_config.format.upper()

    if input_format == DefinitionsFormats.OPENAPI_3.name:
        name, version = _extract_api_version_from_openapi_3(content)
    else:
        raise ValueError("Invalid definition file type")

    if not name:
        raise ValueError("Can't determinate API name. Please provide an "
                         "API name manually")
    if not version:
        raise ValueError("Can't determinate API version. Please provide an "
                         "API version manually")

    return name, version


# -------------------------------------------------------------------------
# Main saving methods
# -------------------------------------------------------------------------
async def save_to_db(content: str, running_config: APIDefinitionsConfig):
    """Save definition into database"""

    try:
        connection = await get_engine().connect()
    except Exception as e:
        print("Can't connect to database. Error: ", e)
        return

    # -------------------------------------------------------------------------
    # Check if api name / version already exits
    # -------------------------------------------------------------------------
    api_name, api_version = extract_api_version(content, running_config)

    # -------------------------------------------------------------------------
    # Getting metadata
    # -------------------------------------------------------------------------
    r = await connection.execute(APIMetadata.select().where(and_(
        APIMetadata.c.api_name==api_name,
        APIMetadata.c.api_version==api_version
    )))

    res = await r.fetchone()

    #
    # Doesn't exits metadata info -> create it
    #
    if not res:
        _r = await connection.execute(APIMetadata.insert().values(
            api_name=api_name,
            api_version=api_version))

        metadata_id = _r.inserted_primary_key[0]
    else:
        metadata_id, *_ = res

    try:

        await connection.execute(APIDefinitions.insert().values(
            format=running_config.format,
            version=running_config.format,
            data=content,
            metadata_id=metadata_id))
    except Exception as e:
        print("!" * 20, "ERROR SAVING LOG: ", e)


def run_load_api_definitions(running_config: APIDefinitionsConfig):

    with open(running_config.file_path, "r") as f:
        definition_file_content = f.read()

    # -------------------------------------------------------------------------
    # Setup database
    # -------------------------------------------------------------------------
    setup_db_engine(running_config.db_connection_string)

    # -------------------------------------------------------------------------
    # Store process
    # -------------------------------------------------------------------------
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(save_to_db(
            definition_file_content,
            running_config
        ))
    except ValueError as e:
        print()
        print("[!] ", e)
        print()
