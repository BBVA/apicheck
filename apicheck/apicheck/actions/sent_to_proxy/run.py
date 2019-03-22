"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""

import json
from typing import Tuple

import aiohttp
import asyncio
import logging

from sqlalchemy import and_
from urllib.parse import urlparse

from apicheck.db import ProxyLogs, get_engine
from apicheck.core.model import API
from apicheck.exceptions import APICheckException
from apicheck.core.openapi3 import openapi3_from_db

from .config import RunningConfig

logger = logging.getLogger("apicheck")


def _split_netloc(netloc: str) -> Tuple[str, str]:
    """From a netloc, my.hostname.com:9000, return a tuple with the hostname
    and port

    :return: tuple as (HOST, PORT)
    """
    if ":" in netloc:
        host, port = netloc.split(maxsplit=1)
    else:
        host = netloc
        port = "443" if netloc.startswith("https") else "80"

    return host, port


async def send_to_proxy_from_proxy(running_config: RunningConfig):
    connection = await get_engine().connect()

    _logs = await connection.execute(ProxyLogs.select().where(and_(
        ProxyLogs.c.id
    )))

    logs = await _logs.fetchall()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(
            verify_ssl=False)) as session:

        for log in logs:
            log_id, session_id, request_raw, response_raw = log

            request_json = json.loads(request_raw)

            http_method = request_json["method"].lower()
            http_scheme = request_json["scheme"]
            http_content = request_json["content"]
            http_headers = request_json["headers"]
            host = request_json["host"]
            port = request_json["port"]
            path = request_json["path"]

            url = f"{http_scheme}://{host}:{port}{path}"

            #
            # aiohttp has multiple method depending of HTTP method
            #
            fn_method = getattr(session, http_method)

            #
            # Fix accept encoding and removing "Brotli" support due
            # compatibility between browsers, servers and aiohttp
            #
            try:
                encoding = http_headers["accept-encoding"]
                if "br" in encoding:
                    http_headers["accept-encoding"] = ",".join(
                        x.strip() for x in encoding.split(",") if "br" not in x
                    )

            except KeyError:
                pass

            # If method is different form "get", has http_content:
            fn_params = dict(
                url=url,
                headers=http_headers,
                proxy=f"http://{running_config.proxy_ip}:"
                      f"{running_config.proxy_port}"
            )
            if http_content:
                fn_params["data"] = http_content

            async with fn_method(**fn_params) as response:
                try:
                    logger.info(f"Sending query to: '{url}'")
                    resp = await response.text()
                except Exception as e:
                    print(e)


async def send_to_proxy_from_definition(running_config: RunningConfig):
    api: API = await openapi3_from_db(running_config.api_id)

    print(api)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(
            verify_ssl=False)) as session:

        # Recover all end-points
        for end_point in api.end_points:

            # -----------------------------------------------------------------
            # Getting API connection parameters
            # -----------------------------------------------------------------
            if api.servers:

                if len(api.servers) > 1:
                    logger.warning("More than one server found in the "
                                   "definition file. Using the first one "
                                   "as target point")

                http_scheme = api.servers[0].scheme
                port = api.servers[0].port
                host = api.servers[0].hostname
                path = api.servers[0].path

            else:
                if not running_config.api_url:
                    raise APICheckException("API Base URL not provided")

                http_scheme, netloc, path, *_ = urlparse(
                    running_config.api_url
                )

                host, port = _split_netloc(netloc)

            url = f"{http_scheme}://{host}:{port}{path}{end_point.uri}"

            for end_point_method, end_point_obj in end_point.methods.items():
                #
                # aiohttp has multiple method depending of HTTP method
                #
                fn_method = getattr(session, end_point_method)

                print(end_point_obj.request)
                print(end_point_obj.request.headers.headers)
                print(end_point_obj.request.body)

                for resp in end_point_obj.request.responses:
                    print(resp)
                    print(resp.headers.headers)
                    print(resp.http_code)
                    print(resp.body)

                # Fix accept encoding and removing "Brotli" support due
                # compatibility between browsers, servers and aiohttp
                #
                # try:
                #     encoding = http_request_headers.headers["accept-encoding"]
                #     if "br" in encoding:
                #         http_request_headers["accept-encoding"] = ",".join(
                #             x.strip() for x in encoding.split(",") if "br" not in x
                #         )
                #
                # except KeyError:
                #     pass
            #
            #     # If method is different form "get", has http_content:
            #     fn_params = dict(
            #         url=url,
            #         headers=http_headers,
            #         proxy=f"http://{running_config.proxy_ip}:{
            #     running_config.proxy_port}"
            #     )
            #     if http_content:
            #         fn_params["data"] = http_content
            #
            #     async with fn_method(**fn_params) as response:
            #         try:
            #             logger.info(f"Sending query to: '{url}'")
            #             resp = await response.text()
            #         except Exception as e:
            #             print(e)


async def _run(running_config: RunningConfig):
    if running_config.source == "proxy":
        return await send_to_proxy_from_proxy(running_config)
    elif running_config.source == "definition":
        return await send_to_proxy_from_definition(running_config)


def run(running_config: RunningConfig):
    logger.info(f"Send API '{running_config.api_id}' to proxy")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run(running_config))
