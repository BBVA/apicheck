from dataclasses import dataclass

from apicheck.model import CommonModel


@dataclass(frozen=True)
class ProxyConfig(CommonModel):
    domain: str
    listen_addr: str = "127.0.0.1"
    listen_port: int = 8080
    store_assets_content: bool = False
    learning_mode: bool = False
    promiscuous: bool = False

