import sys

from typing import List, Dict, Iterable, Set
from abc import ABCMeta


class DictSerializer(metaclass=ABCMeta):

    def to_dict(self, *, exclude_fields: List[str] or Set[str] = None) -> Dict:
        """
        This method get all public class properties and return a Dict object
        """
        rest = {}
        for k, v in self.__dict__.items():
            if k.startswith("_") and k not in exclude_fields:
                continue

            rest[k] = v

        return rest


class APIDeployments(DictSerializer):

    def __init__(self,
                 domain: str = None,
                 scheme: str = None,
                 port: int = None):
        self.domain: str = domain
        self.scheme: str = scheme or "http"
        self.port: int = port or 80


class APIMetadata(DictSerializer):

    def __init__(self,
                 name: str,
                 base_api_path: str,
                 version: str,
                 deployments: List[APIDeployments]):
        self.version: str = version
        self.base_api_path: str = base_api_path
        self.name: str = name
        self.deployments: List[APIDeployments] = deployments

    def to_dict(self, *, exclude_fields: List[str] or Set[str] = None):
        simple_params = super(APIMetadata, self).to_dict(
            exclude_fields=("deployments",)
        )

        simple_params["deployments"] = [
            x.to_dict() for x in self.deployments
        ]

        return simple_params


class EndPointParam(DictSerializer):

    def __init__(self,
                 name: str,
                 param_type: str = "string",
                 description: str = None,
                 default: str = None,
                 minimum_value: int = None,
                 maximum_value: int = None,
                 max_length: int = None):
        self.name: str = name
        self.default: str = default
        self.param_type: str = param_type or "string"
        self.description: str = description or ""
        self.max_length: int = max_length or None
        self.minimum_value: int = minimum_value or None
        self.maximum_value: int = maximum_value or sys.maxsize


class EndPointResponse(DictSerializer):

    def __init__(self,
                 http_code: int,
                 content_type: str,
                 description: str = None,
                 params: List[EndPointParam] = None):
        self.http_code: int = http_code
        self.content_type: str = content_type
        self.description: str = description or ""
        self.params: List[EndPointParam] = params or []

    def to_dict(self, *, exclude_fields: List[str] or Set[str] = None):
        simple_params = super(EndPointResponse, self).to_dict(
            exclude_fields=("params",)
        )

        simple_params["params"] = [
            x.to_dict() for x in self.params
        ]

        return simple_params


class EndPointBody(DictSerializer):

    def __init__(self,
                 content_type: str,
                 description: str = None,
                 required: bool = None,
                 params: List[EndPointParam] = None):
        self.content_type = content_type
        self.required = required or False
        self.description = description or ""
        self.params: List[EndPointParam] = params or []

    def to_dict(self, *, exclude_fields: List[str] or Set[str] = None):
        simple_params = super(EndPointBody, self).to_dict(
            exclude_fields=("params",)
        )

        simple_params["params"] = [
            x.to_dict() for x in self.params
        ]

        return simple_params


class EndPoint(DictSerializer):

    def __init__(self,
                 uri: str,
                 verb: str,
                 *,
                 query_params: List[EndPointParam] = None,
                 responses: List[EndPointParam] = None,
                 http_headers: List[dict] = None,
                 description: str = None,
                 body: EndPointBody = None):
        self.uri: str = uri
        self.verb: str = verb

        self.query_params: List[EndPointParam] = query_params or []
        self.responses: List[EndPointResponse] = responses or []
        self.http_headers: List[Dict[str]] = http_headers or []
        self.body: EndPointBody = body or None
        self.description: str = description or ""

    def __repr__(self):
        return f"<End-Point [{self.verb}] -> '{self.uri}'>"

    def to_dict(self, *, exclude_fields: List[str] = None):
        simple_params = super(EndPoint, self).to_dict(
            exclude_fields=("query_params", "http_headers", "body",
                            "responses")
        )

        simple_params["query_params"] = [
            x.to_dict() for x in self.query_params
        ]

        if self.body:
            simple_params["body"] = self.body.to_dict()
        else:
            simple_params["body"] = None

        if self.responses:
            simple_params["responses"] = [
                x.to_dict() for x in self.responses
            ]
        else:
            simple_params["responses"] = None

        return simple_params


class APITestModel:

    def __init__(self,
                 metadata: APIMetadata = None,
                 endpoints: Iterable[EndPoint] or List[EndPoint] = None):
        self.metadata = metadata
        self.end_points: List[EndPoint] or List[EndPoint] = endpoints


