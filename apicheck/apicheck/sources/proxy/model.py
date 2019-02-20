from dataclasses import dataclass

from apicheck.model import Singleton


@dataclass(frozen=True)
class ProxyConfig(object, metaclass=Singleton):
    db_connection_string: str
    domain: str
    listen_addr: str = "127.0.0.1"
    listen_port: int = 8080
    store_assets_content: bool = False
