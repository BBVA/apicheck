from dataclasses import dataclass

from apicheck.config import CommonConfig


@dataclass
class RunningConfig(CommonConfig):
    domain: str
    listen_addr: str = "127.0.0.1"
    listen_port: int = 8080
    store_assets_content: bool = False
    learning_mode: bool = False
    promiscuous: bool = False

    def __post_init__(self):
        if type(self.domain) is list:
            try:
                self.domain = self.domain[0]
            except IndexError:
                self.domain = ""

