
from apitest import SharedConfig, String


class ApitestPostmanParseModel(SharedConfig):
    file_path = String()
    output_file = String(default="apitest_parsed.dump_json")
    
__all__ = ("ApitestPostmanParseModel",)


