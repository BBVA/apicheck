"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""
import json
import aiohttp
import asyncio
import logging

from sqlalchemy import and_
from apicheck.db import ProxyLogs, get_engine, APIMetadata

from .config import RunningConfig

logger = logging.getLogger("apicheck")


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
                proxy=f"http://{running_config.proxy_ip}:{running_config.proxy_port}"
            )
            if http_content:
                fn_params["data"] = http_content

            async with fn_method(**fn_params) as response:
                try:
                    logger.info(f"Sending query to: '{url}'")
                    resp = await response.text()
                except Exception as e:
                    print(e)


async def send_to_proxy_from_definition():
    pass


async def _run(running_config: RunningConfig):
    if running_config.source == "proxy":
        return await send_to_proxy_from_proxy(running_config)
    elif running_config.source == "definition":
        return await send_to_proxy_from_definition(running_config)


def run(running_config: RunningConfig):
    logger.info(f"Send API '{running_config.api_id}' to proxy")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run(running_config))
