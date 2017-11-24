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

from apitest.utils.url_fuzzers import FUZZSelector


def test_fuzzselector_type():
    with pytest.raises(ValueError):
        FUZZSelector(None)


def test_fuzzselector_invalid_length():
    with pytest.raises(ValueError):
        FUZZSelector(1111111)


def test_fuzzselector_test_url():
    f = FUZZSelector(FUZZSelector.URL)
    assert f.is_url is True


def test_fuzzselector_test_body():
    f = FUZZSelector(FUZZSelector.BODY)
    assert f.is_body is True


def test_fuzzselector_test_cookies():
    f = FUZZSelector(FUZZSelector.COOKIE)
    assert f.is_cookie is True


def test_fuzzselector_test_headers():
    f = FUZZSelector(FUZZSelector.HEADER)
    assert f.is_header is True


def test_fuzzselector_test_method():
    f = FUZZSelector(FUZZSelector.METHOD)
    assert f.is_method is True


def test_fuzzselector_test_composed_values():
    f = FUZZSelector(FUZZSelector.HEADER | FUZZSelector.URL)
    assert f.is_header is True
    assert f.is_url is True
