from typing import List
from dataclasses import dataclass, field


class ContentTypes:
    STRING = 1
    JSON = 2
    RAW = 3


@dataclass
class Response:
    http_code: str
    http_message: str = "OK"
    content: str or dict or bytes = None
    content_type: int = ContentTypes.JSON
    headers: dict = field(default_factory=dict)


@dataclass
class EndPointRequest:
    uri: str
    method: str
    responses: List[Response]
    content: str or dict or bytes = None
    content_type: int = ContentTypes.JSON
    headers: dict = field(default_factory=dict)


@dataclass
class API:
    name: str
    version: str
    end_points: List[EndPointRequest]
