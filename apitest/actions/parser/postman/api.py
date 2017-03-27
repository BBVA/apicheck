from typing import List, Dict

try:
    from ujson import load
except ImportError:
    from json import load

from apitest import APITest

from .parsers import postman_parser


def parse_postman_file(path: str,
                       environment_vars: List[Dict]) -> APITest:
    """
    This function parse a Postman file and return an APITest object instance

    :param path: path to postman file
    :type path: str

    :return: APITest instance
    :rtype: APITest
    """
    assert isinstance(path, str)

    with open(path, "r") as f:
        json_info = load(f)

        return postman_parser(json_info,
                              environment_vars)


__all__ = ("parse_postman_file", )
