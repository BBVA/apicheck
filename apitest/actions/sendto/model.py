
from apitest import SharedConfig, String


class ApitestModel(SharedConfig):
    file_path = String()
    
__all__ = ("ApitestModel", )


