from dataclasses import dataclass

from apicheck.config import CommonConfig


@dataclass
class RunningConfig(CommonConfig):
    name: str
    dest: str
