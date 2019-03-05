"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""

import re
import asyncio
import logging

from typing import Tuple
from urllib.parse import urlparse
from sqlalchemy import and_

from apicheck.db import get_engine, APIDefinitions, setup_db_engine, \
    APIMetadata
from apicheck.exceptions import APICheckFormatException, APICheckException

from .config import RunningConfig, DefinitionsFormats

logger = logging.getLogger("apicheck")


# -------------------------------------------------------------------------
# Detectors of file formats
# -------------------------------------------------------------------------
def detect_file_definition_format(content) -> str or ValueError:
    """This function try to detect the file definition format.

    This uses regex to avoid to load and parse the file content. Currently it
    supports:

    - OpenAPI 3
    - Swagger
    - RAML

    If it detect the format, return the string: FORMAT_NAME
    otherwise:
        raise ValueError

    """
    format_detectors = {
        DefinitionsFormats.OPENAPI_3.name: (
            r"""(openapi)(\:[\s]*)([\d\.]+)""", 1, 3
        ),
        DefinitionsFormats.SWAGGER.name: (
            r"""(\{\")(swagger)(\")([\s]*\:[\s]*)([\s]*\")([\d\.]+)(\")""",
            2, 6
        ),
        DefinitionsFormats.RAML.name: (
            r"""(#\%)(RAML)([\s]*)([\d\.]+)""", 2, 4
        ),
    }

    format_name = format_version = None
    for extractor_name, (regex, group_name, group_version) \
            in format_detectors.items():

        v = re.search(regex, content)

        if v:
            n = v.group(group_name)
            v = v.group(group_version)

            if n and v:
                format_name = extractor_name
                format_version = v
                break

    if not format_name or not format_version:
        raise ValueError("Can't detect file definition format")

    return format_name


# -------------------------------------------------------------------------
# Extractors of API name / version
# -------------------------------------------------------------------------
def _extract_api_info_from_openapi_3(content) -> Tuple[str, str]:
    regex_version = r"""(version\:)([\s]*)([\d\\.]+)"""
    regex_api_name = \
        r"""(servers\:[\n\r]+[\s]*-[\s]*)(url:[\s]*)([0-9\.\/\w\:]+)"""

    name = version = None

    v = re.search(regex_version, content)
    if v:
        version = v.group(3)
    n = re.search(regex_api_name, content)
    if n:
        name = urlparse(n.group(3)).hostname

    return name, version


def _extract_api_info_from_swagger(content) -> Tuple[str, str]:
    regex_version = \
        r"""(basePath)(\")([\s]*\:[\s]*\")([\/\d\w\.]+)"""
    regex_api_name = \
        r"""(host)(\")([\s]*\:[\s]*\")([\/\d\w\.]+)"""

    name = version = None

    v = re.search(regex_version, content)
    if v:
        _version = v.group(4)

        if _version.startswith("/"):
            version = _version[1:]

            if "/" in version:
                version = version.split("/")[0]

    n = re.search(regex_api_name, content)
    if n:
        name = n.group(4)

    return name, version


def _extract_api_info_from_raml(content) \
        -> Tuple[str, str] or APICheckFormatException:
    raise APICheckFormatException(
        "Can't determinate API name/version from RAML file"
    )


def extract_api_version(
        content: str,
        running_config: RunningConfig) \
        -> Tuple[str, str] or APICheckFormatException or APICheckException:
    """
    Extract API version / name from the definition file

    :return: return format: Tuple[NAME, VERSION]
    """
    if running_config.api_version and running_config.api_name:
        return running_config.api_name, running_config.api_version

    extractors = {
        DefinitionsFormats.OPENAPI_3.name: _extract_api_info_from_openapi_3,
        DefinitionsFormats.SWAGGER.name: _extract_api_info_from_swagger,
        DefinitionsFormats.RAML.name: _extract_api_info_from_raml,
    }

    input_format = running_config.format
    if input_format:
        input_format = input_format.upper()

    #
    # User selected specific extractor
    #
    api_name = api_version = None
    if input_format:
        try:
            api_name, api_version = extractors[input_format](
                content
            )
        except KeyError:
            raise APICheckFormatException("Invalid definition file type")
    #
    # try to detect file format
    #
    else:
        file_format = detect_file_definition_format(
            content
        )
        #
        # Choice extractor
        #
        try:
            api_name, api_version = extractors[file_format](
                content
            )
        except KeyError:
            raise APICheckFormatException("Invalid definition file type")

    if not api_name:
        raise APICheckException(
            "Can't determinate API name. Please provide an "
            "API name manually")
    if not api_version:
        raise APICheckException(
            "Can't determinate API version. Please provide an "
            "API version manually")

    return api_name, api_version


# -------------------------------------------------------------------------
# Main saving methods
# -------------------------------------------------------------------------
async def save_to_db(content: str, running_config: RunningConfig) \
        -> None or APICheckException:
    """Save definition into database"""

    try:
        connection = await get_engine().connect()
    except Exception as e:
        raise APICheckException(f"Can't connect to database. Error: {e}")

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
        raise APICheckException(f"Error storing API Definition to database. "
                                f"Error: {e}")


def run(running_config: RunningConfig):

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
    except Exception as e:
        print()
        print("[!] ", e)
        print()
