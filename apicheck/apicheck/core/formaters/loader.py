from exceptions import APICheckException
from apicheck.db import APIDefinitions, APIDefinitionsCache, get_engine

from .model import OpenAPI3
from .openapi3 import load_openapi3

CONVERTERS = {
    "openapi_3": load_openapi3
}


async def load_from_db(api_id: str) -> OpenAPI3:
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
        parsed_content, openapi_obj = CONVERTERS[api_format](
            content,
            bool(cached)
        )

        #
        # Save into cache
        #
        if not cached:
            await connection.execute(
                APIDefinitionsCache.insert().values(
                    api_id=api_id,
                    format=api_format,
                    content=parsed_content
                ))
    except KeyError:
        raise APICheckException(f"Format '{api_format}' not supported")


