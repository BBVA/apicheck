"""
This file contains the code to manage OpenAPI 3 format
"""
from typing import List, Dict
from functools import lru_cache
from urllib.parse import urlparse

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError as e:
    from yaml import Loader, Dumper

from exceptions import APICheckException
from apicheck.db import APIDefinitions, get_engine


HTTP_METHODS = ("get", "head", "post", "put", "delete", "connect",
                "options", "trace")


class Server:

    def __init__(self, content: str):
        scheme, netloc, path, *_ = urlparse(content)

        self.scheme: str = scheme
        self.path: str = path

        if ":" in netloc:
            host, port = netloc.split(maxsplit=1)
        else:
            host = netloc
            port = "443" if netloc.startswith("https") else "80"

        self.hostname: str = host
        self.port: str = port


class _HTTPHeaders:

    def __init__(self, content: dict):
        self.content: dict = content or {}

    @property
    @lru_cache(maxsize=1)
    def description(self) -> str:
        return self.content.get("description", "")


class HTTPHeadersResponse(_HTTPHeaders):

    def __init__(self, content: dict):
        super().__init__(content)

    @property
    @lru_cache(maxsize=1)
    def headers(self) -> dict:
        return {
            "Content-Type": x
            for x in self.content.keys()
        }


class EndPointResponse:

    def __init__(self, http_code: str, content: dict):
        self.content = content
        self.http_code = http_code

    @property
    @lru_cache(maxsize=1)
    def headers(self) -> HTTPHeadersResponse:
        return HTTPHeadersResponse(
            self.content.get("content", None)
        )

    @property
    def body(self):
        return ""


class HTTPHeadersRequest(_HTTPHeaders):

    def __init__(self, content: dict):
        super().__init__(content)

    @property
    @lru_cache(maxsize=1)
    def required(self) -> bool:
        return self.content.get("required", False)

    @property
    @lru_cache(maxsize=1)
    def headers(self) -> dict:
        return {
            "Content-Type": x
            for x in self.content.get("content", {}).keys()
        }


class EndPointRequest:

    def __init__(self, content: dict):
        self.content = content

    @property
    @lru_cache(maxsize=1)
    def headers(self) -> HTTPHeadersRequest:
        return HTTPHeadersRequest(
            self.content.get("requestBody", None)
        )

    @property
    def body(self):
        return ""

    @property
    def responses(self) -> List[EndPointResponse]:
        return [
            EndPointResponse(http_code, data)
            for http_code, data
            in self.content.get("responses", {}).items()
        ]


class EndPointMethod:

    def __init__(self, method: str, content: dict):
        self.content = content
        self.method: str = method
        self._request_headers = None
        self._response_headers = None
        self._body = None

    @property
    @lru_cache(maxsize=1)
    def request(self):
        return EndPointRequest(self.content)

    @property
    @lru_cache(maxsize=1)
    def tags(self) -> list:
        return self.content.get("tags", [])

    @property
    @lru_cache(maxsize=1)
    def summary(self) -> str:
        return self.content.get("summary", "")

    @property
    @lru_cache(maxsize=1)
    def description(self) -> str:
        return self.content.get("description", "")

    @property
    @lru_cache(maxsize=1)
    def operationId(self) -> str:
        return self.content.get("operationId", "")

    @property
    @lru_cache(maxsize=1)
    def security(self) -> dict:
        return self.content.get("security", {})

    @property
    @lru_cache(maxsize=1)
    def examples(self) -> dict:
        return self.content.get("x-code-samples", {})


class EndPoint:

    def __init__(self, uri: str, content: dict):
        self.uri = uri
        self.content = content
        self._methods: dict = None
        self._properties: dict = None

    @property
    def methods(self) -> Dict[str, EndPointMethod]:
        if not self._methods:
            self._methods = {}
            for x, y in self.content.items():
                if x not in HTTP_METHODS:
                    continue

                self._methods[x] = EndPointMethod(x, y)

        return self._methods

    @property
    def properties(self) -> dict:
        if not self._properties:
            self._properties = {}
            for x, y in self.content.items():
                if x in HTTP_METHODS:
                    continue
                self.properties[x] = y

        return self.properties


class OpenAPI3:

    def __init__(self, content: str):
        self._raw = content
        self._end_points = None
        self._servers = None
        # self.content = load(self._raw, Loader=Loader)

    # @classmethod
    # async def from_db(cls, api_id: str):
    #     try:
    #         connection = await get_engine().connect()
    #     except Exception as e:
    #         raise APICheckException(f"Can't connect to database. Error: {e}")
    #
    #     c = await connection.execute(
    #         APIDefinitions.select().where(
    #             APIDefinitions.c.metadata_id==api_id
    #         ).order_by(APIDefinitions.c.id.desc())
    #     )
    #
    #     try:
    #         _, _, _, content, _ = await c.fetchone()
    #     except TypeError:
    #         # API not found
    #         raise APICheckException(f"API '{api_id}' not found in database")
    #
    #     return cls(content)

    @property
    def end_points(self) -> List[EndPoint]:
        if not self._end_points:
            self._end_points = [
                EndPoint(uri, data)
                for uri, data in self.content["paths"].items()
            ]

        return self._end_points

    @property
    def servers(self) -> List[Server]:
        if not self._servers:
            self._servers = [
                Server(x["url"]) for x in self.content["servers"]
            ]

        return self._servers
