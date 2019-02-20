import json
import asyncio

from apicheck.sources.proxy import ProxyConfig
from apicheck.db import get_engine, ProxyLogs, create_database

VALID_CONTENT_TYPES = (
    "text/html", "application/json", "application/javascript",
    "application/xml", "text/xml", "text/plain", "text/css",
    "application/x-javascript"
)


class APICheckDumpToDatabase:

    def __init__(self):
        self._connection = None
        self.proxy_config = ProxyConfig()

    def response(self, flow):
        asyncio.get_event_loop().create_task(self.save_response(flow))

    def clean_content(self, content: dict, exclude: str = None) -> dict:
        data = content["data"]

        ret = {}
        for x, y in data.__dict__.items():
            if x == "headers" or x.startswith("_"):
                continue

            if exclude and x == exclude:
                continue

            try:
                ret[x] = y.decode("UTF-8")
            except (AttributeError, UnicodeDecodeError):
                ret[x] = y

        ret["headers"] = {
            x.decode("UTF-8"): y.decode("UTF-8")
            for x, y in data.headers.fields
        }

        return ret

    async def save_response(self, flow):
        """Save request / response into database"""
        if not self._connection:
            self._connection = await get_engine().connect()

            # Create database
            await create_database()

        plain_request = json.dumps(self.clean_content(flow.request.__dict__))

        #
        # Doesn't store assets content, by default
        #
        exclude = None
        if not self.proxy_config.store_assets_content:
            content_type = flow.response.data.headers[b"content-type"]
            if content_type not in VALID_CONTENT_TYPES:
                exclude = "content"

        plain_response = self.clean_content(
            flow.response.__dict__, exclude=exclude
        )

        try:
            await self._connection.execute(ProxyLogs.insert().values(
                request=str(plain_request)),
                response=str(plain_response)
            )
        except Exception as e:
            print("!" * 20, e)


addons = [
    APICheckDumpToDatabase()
]
