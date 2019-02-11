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

from random import choice, randint

from apitest.utils.url_fuzzers import fuzz_value_from_type, build_fuzzed_x_form


@pytest.fixture
def dummy_data():
    var_names = ["name", "user", "password", "lang", "country"]
    var_types = [1, True, 1.0, "hello"]

    return "&".join("%s=%s" % (var_names[i], fuzz_value_from_type(choice(var_types))) for i in range(randint(1, len(var_names))))


def test_build_fuzzed_x_form_type(dummy_data):
    r = build_fuzzed_x_form(dummy_data)

    assert isinstance(r, str)


def test_build_fuzzed_x_form_type_empty_input():
    r = build_fuzzed_x_form(None)

    assert r == ""


def test_build_fuzzed_x_form_format(dummy_data):
    r = build_fuzzed_x_form(dummy_data)

    assert len(r.split("&")) > 0
