import json
import logging

from typing import Tuple, List, Dict

from apicheck.core.helpers import slug, debugging
from apicheck.exceptions import APICheckException
from apicheck.db import APIDefinitions, APIDefinitionsCache, get_engine

from .helpers import yaml_loader
from .model import API, Request, Response
from .dict_helpers import search_all, search, ref_resolver, transform_tree

logger = logging.getLogger("apicheck")


def extract_requests(parsed_data: dict) -> List[Request]:
    pass


def extract_responses(method: str, content: dict) -> List[Response]:
    for http_code, response_content in search(content, "responses").items():
        model = search(response_content, "properties")

        pass


def extract_endpoints(parsed_data) -> List[str]:
    return search(parsed_data, "paths")


def extract_methods(end_point: dict) -> Dict[str, dict]:
    methods = ["get", "put", "post", "patch", "delete"]

    for k,v in end_point.items():
        if k in methods:
            yield k, v


def extract_metadata(parsed_data: dict) -> Tuple[str, str]:
    metadata = search(parsed_data, "info")

    try:
        api_name = slug(metadata["title"])
    except KeyError:
        raise APICheckException("Can't get API name. Be sure definition "
                                "file has the property 'title'")

    try:
        api_version = metadata["version"]
    except KeyError:
        raise APICheckException("Can't get API Version. Be sure definition "
                                "file has the property 'version'")

    return api_name, api_version


def build_api_model(str_data: str) -> API:

    end_points = []
    end_points_append = end_points.append
    debug_enabled = debugging()

    parsed_data = json.loads(str_data)
    resolver = ref_resolver(parsed_data)

    # -------------------------------------------------------------------------
    # We don't know why if debugger is enabled this code lock them. Then only
    # transform the complete tree when non-debug running mode
    # -------------------------------------------------------------------------
    if not debug_enabled:
        parsed_data = transform_tree(parsed_data, resolver)
    else:
        e = 0

    print("Extracting info")
    for end_point, end_point_info in extract_endpoints(parsed_data).items():

        for method, req_info in extract_methods(end_point_info):

            if debug_enabled:
                info = transform_tree(req_info, resolver)
            else:
                info = req_info

            req = Request(
                uri=end_point,
                method=method,
                headers={},
                responses=extract_responses(method, info)
            )

            end_points_append(req)

        if debug_enabled:
            e += 1

            if e > 10:
                break

    name, version = extract_metadata(parsed_data)

    return API(
        name=name,
        version=version,
        end_points=end_points
    )


async def openapi3_from_db(api_id: str) -> API:
    """
    This function get an API Id, detect the stored definition format and call
    the specific format loaded.

    Always returns an OpenAPI3 object
    """

    try:
        connection = await get_engine().connect()
    except Exception as e:
        raise APICheckException(f"Can't connect to database. Error: {e}")

    # -------------------------------------------------------------------------
    # Try to get the loaded content form cache
    # -------------------------------------------------------------------------
    _cached = await connection.execute(
        APIDefinitionsCache.select().where(
            APIDefinitionsCache.c.api_id == api_id
        )
    )

    try:
        _, api_format, cached = await _cached.fetchone()
    except TypeError:
        api_format = cached = None

    if not cached:
        # ---------------------------------------------------------------------
        # Getting content from original source
        # ---------------------------------------------------------------------
        c = await connection.execute(
            APIDefinitions.select().where(
                APIDefinitions.c.metadata_id == api_id
            ).order_by(APIDefinitions.c.id.desc())
        )

        try:
            _, api_format, _, content, _ = await c.fetchone()
        except TypeError:
            # API not found
            raise APICheckException(f"API '{api_id}' not found in database")

    else:
        content = cached

    try:

        logger.info("Parsing OpenAPI information")

        if bool(cached):
            parsed = json_content = content
        else:
            parsed = yaml_loader(content)
            json_content = json.dumps(parsed)

        #
        # Save into cache
        #
        if not cached:
            await connection.execute(
                APIDefinitionsCache.insert().values(
                    api_id=api_id,
                    format=api_format,
                    content=json_content
                ))

        return build_api_model(parsed)

    except KeyError:
        raise APICheckException(f"Format '{api_format}' not supported")


