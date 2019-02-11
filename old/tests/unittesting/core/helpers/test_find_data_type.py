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
import pytest

from apitest import ApitestUnknownTypeError
from apitest.core.helpers import find_data_type


def test_find_data_type_int():
    assert find_data_type(1) == 'int'


def test_find_data_type_str():
    assert find_data_type("a") == 'str'


def test_find_data_type_float():
    assert find_data_type(1.0) == 'float'


def test_find_data_type_list():
    assert find_data_type([]) == 'list'


def test_find_data_type_dict():
    assert find_data_type({}) == 'dict'


def test_find_data_type_bool():
    assert find_data_type(True) == 'bool'


def test_find_data_type_bool_2():
    assert find_data_type("True") == 'bool'


def test_find_data_type_unknown_object():

    class A():
        pass

    with pytest.raises(ApitestUnknownTypeError):
        find_data_type(A())

