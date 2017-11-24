# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
