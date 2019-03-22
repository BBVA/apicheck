from typing import List
from dataclasses import dataclass


@dataclass
class Response:
    http_code: str
    http_message: str
    body: str
    headers: dict


@dataclass
class Request:
    uri: str
    method: str
    headers: dict
    responses: List[Response]


@dataclass
class API:
    name: str
    version: str
    end_points: List[Request]
