
from apitest import SharedConfig, URL, String


class ApitestSendtoModel(SharedConfig):
    proxy_url = URL(default="http://127.0.0.1:8080")
    proxy_user = String()
    proxy_password = String()
    apitest_file = String()
    
    
__all__ = ("ApitestSendtoModel", )


