import mimetypes

from typing import Optional, List, Dict
from dataclasses import dataclass, fields, field


@dataclass
class BaseAPICheck(object):

    def __post_init__(self):
        params = [(f.name, f.type) for f in fields(self)]

        # ---------------------------------------------------------------------
        # Check basic types only
        # ---------------------------------------------------------------------
        for p_name, p_type in params:
            _p_type = p_type.__args__ \
                if hasattr(p_type, "__args__") \
                else (p_type, )

            # Check that types are only basic types
            if not any(x in _p_type for x in (str, int, list, dict, bool)):
                continue

            if type(getattr(self, p_name)) not in _p_type:
                raise ValueError(f"Invalid type for '{p_name}' property")


@dataclass(frozen=True)
class EndPointParam(BaseAPICheck):
    name: str
    param_type: str = "string"
    description: str = ""
    default: Optional[str] = None
    minimum_value: Optional[str] = None
    maximum_value: Optional[str] = None
    max_length: Optional[int] = 500


@dataclass(frozen=True)
class EndPointResponse(BaseAPICheck):
    http_code: Optional[int] = 200
    content_type: Optional[str] = "application/json"
    description: Optional[str] = None
    params: List[EndPointParam] = field(default_factory=list)
    headers: dict = field(default_factory=dict)

    def __post_init__(self):
        super(EndPointResponse, self).__post_init__()

        # Checking "params" type
        if type(self.params) is not list:
            raise ValueError("Invalid type for property 'params'")
        else:
            if self.params and \
                    not all(type(x) is EndPointParam for x in self.params):
                raise ValueError("Invalid type for 'params' element")

        # Checking "http_code" ranges
        if not (0 < self.http_code < 600):
            raise ValueError("Invalid 'http_code' value")

        # Checking valid content type
        if self.content_type is None or "/" not in self.content_type:
            raise ValueError("Invalid 'content_type'")
