
from apitest import SharedConfig, String, List


class ApitestPostmanAnalyzeModel(SharedConfig):
    file_path = String()
    postman_variables = List()


class ApitestPostmanParseModel(ApitestPostmanAnalyzeModel):
    output_file = String(default="apitest_parsed.dump_json")


__all__ = ("ApitestPostmanAnalyzeModel", "ApitestPostmanParseModel")


