from dataclasses import dataclass

from apicheck.model import CommonModel


@dataclass(frozen=True)
class APIManageConfig(CommonModel):
    api_action: str
