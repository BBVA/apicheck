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

from apitest.core.helpers import dict_to_obj


def test_dict_to_obj_response_ok():

    ret = dict_to_obj(dict(hello="world", bye="see you"))

    assert hasattr(ret, "hello")
    assert hasattr(ret, "bye")


def test_dict_to_obj_response_invalid_input():

    with pytest.raises(AssertionError):
        dict_to_obj(None)


def test_dict_to_obj_response_empty():

    assert issubclass(dict_to_obj({}), object)
