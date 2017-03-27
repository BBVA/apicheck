# try:
#     from ujson import load
# except ImportError:
#     from json import load
#
# from apitest import APITest, postman_parser, PostmanConfig
#
#
# def parse_postman_file(path: str, postman_config: PostmanConfig) -> APITest:
#     """
#     This function parse a Postman file and return an APITest object instance
#
#     :param path: path to postaman file
#     :type path: str
#
#     :return: APITest instance
#     :rtype: APITest
#     """
#     assert isinstance(path, str)
#
#     with open(path, "r") as f:
#         json_info = load(f)
#
#         return postman_parser(json_info, postman_config)
#
#
# __all__ = ("parse_postman_file", )
