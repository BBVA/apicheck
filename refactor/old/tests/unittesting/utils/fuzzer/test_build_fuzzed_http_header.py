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

from apitest.utils.url_fuzzers import fuzz_value_from_type, build_fuzzed_http_header


@pytest.fixture
def dummy_data():
    var_names = ["Content-Type", "User-Agent", "Host", "Language", "Accept-Language"]

    return {var_names[i]: fuzz_value_from_type(choice("a")) for i in range(randint(1, len(var_names)))}


def test_build_fuzzed_http_header_type(dummy_data):
    r = build_fuzzed_http_header(dummy_data)

    assert isinstance(r, dict)


def test_build_fuzzed_http_header_values(dummy_data):
    r = build_fuzzed_http_header(dummy_data)

    assert dummy_data.keys() == r.keys()
