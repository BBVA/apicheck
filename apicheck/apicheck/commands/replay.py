from urllib.parse import urlunparse
import aiohttp
import argparse
import asyncio
import base64
import json
import sys
import traceback

from apicheck.core.cli import cli_db
from apicheck.core.db_utils import get_proxy_logs
from apicheck.db import setup_db_engine


REMAINING = 0
WAITER = asyncio.Condition()


async def response_to_json(response):
    data = dict()

    version = response.version
    data["http_version"] = f"HTTP/{version.major}.{version.minor}"

    data["status_code"] = response.status
    data["reason"] = response.reason
    data["content"] = base64.b64encode(await response.read()).decode("ascii")
    data["headers"] = dict()

    for raw_header in response.headers.keys():
        header = str(raw_header)
        value = str(response.headers[raw_header])
        data["headers"][header] = value

    return json.dumps(data)


async def make_request(request):
    global REMAINING
    try:
        async with aiohttp.ClientSession() as session:
            method = getattr(session, request["method"].lower())
            url = urlunparse((request["scheme"],
                              f'{request["host"]}:{request["port"]}',
                              request["path"],
                              None,
                              None,
                              None))
            async with method(url, headers=request["headers"]) as response:
                print(await response_to_json(response))
    except:
        traceback.print_exc(file=sys.stderr)
    finally:
        REMAINING -= 1
        async with WAITER:
            WAITER.notify()


async def replay_logs(logs, multiplier=1):
    global REMAINING
    initial = None
    loop = asyncio.get_event_loop()
    now = loop.time()
    requests = []

    async for log in logs():
        requests.append(json.loads(log["request"]))

    for idx, request in enumerate(requests):
        if initial is None:
            initial = request["timestamp_start"]

        when = now + (request["timestamp_start"] - initial) / multiplier

        loop.call_at(when, asyncio.create_task, make_request(request))
        REMAINING += 1


async def wait_for_requests():
    global REMAINING
    async with WAITER:
        await WAITER.wait_for(lambda: REMAINING == 0)


def main():
    global REMAINING
    parser = argparse.ArgumentParser(
        description="replay saved proxy logs to network"
    )
    parser.add_argument('-x',
                        '--multiplier',
                        action="store",
                        default=1.0,
                        type=float,
                        dest="multiplier",
                        help="Modify replay speed to a given multiple.")

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
    loop.run_until_complete(replay_logs(get_proxy_logs,
                                        multiplier=parsed.multiplier))
    loop.run_until_complete(wait_for_requests())


if __name__ == '__main__':
    main()
