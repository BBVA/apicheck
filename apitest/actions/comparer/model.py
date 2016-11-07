
from apitest import SharedConfig, String


class ApitestComparerModel(SharedConfig):
    api_old_connection_string = String()
    api_current_connection_string = String()
    
__all__ = ("ApitestComparerModel", )


