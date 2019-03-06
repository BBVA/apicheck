from dataclasses import dataclass

from apicheck.model import CommonModel
from apicheck.exceptions import APICheckException


@dataclass
class RunningConfig(CommonModel):
    """
    api_id: Unique ID for the API
    source: origin of data: proxy or definition. Allowed values:
            "proxy|definition"
    """
    OPERATION_MODES = ("definition", "proxy")

    api_id: str
    proxy_destination: str
    source: str = "definition"
    proxy_ip: str = None
    proxy_port: str = None

    def __post_init__(self):
        if self.source not in self.OPERATION_MODES:
            raise APICheckException("Invalid value for source")
        if ":" not in self.proxy_destination:
            raise APICheckException("Invalid proxy destination format")
        else:
            self.proxy_ip, self.proxy_port = self.proxy_destination.split(
                ":", maxsplit=1
            )
