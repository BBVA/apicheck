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

from apitest.core.model import transform_apitest_body_to_queryable, APITestBody


def test_transform_apit_test_body_to_queryable_runs_ok_json():
    data = APITestBody(**dict(content_type="application/json",
                              value='{"hello": "world"}'))

    assert transform_apitest_body_to_queryable(data) == {"hello": "world"}


def test_transform_apit_test_body_to_queryable_runs_ok_xform():
    data = APITestBody(**dict(content_type="application/www-form-urlencoded",
                              value='hello=world'))

    assert transform_apitest_body_to_queryable(data) == "hello=world"


def test_transform_apit_test_body_to_queryable_runs_ok_text():
    data = APITestBody(**dict(content_type="text/plain",
                              value='hello=world asdf asd fsadf'))

    assert transform_apitest_body_to_queryable(data) == "hello=world asdf asd fsadf"


def test_transform_apit_test_body_to_queryable_default_content_type():
    data = APITestBody(**dict(content_type=None,
                              value='{"hello": "world"}'))

    assert transform_apitest_body_to_queryable(data) == {"hello": "world"}


def test_transform_apit_test_body_to_queryable_unknown_content_type():
    data = APITestBody(**dict(content_type="application/pdf",
                              value='KLASDPIFNPUIEBIUBIUH98'))

    assert transform_apitest_body_to_queryable(data) == "KLASDPIFNPUIEBIUBIUH98"


