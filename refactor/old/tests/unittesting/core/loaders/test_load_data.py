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
import json
import pytest

from apitest import APITest
from apitest.core.loaders import load_data

import apitest.core.loaders


@pytest.fixture
def build_temp_file(apitest_json):
    def _temp_file(path):
        with open(path, "w") as f:
            f.write(json.dumps(apitest_json))
    return _temp_file


# --------------------------------------------------------------------------
# Monkey Patching for DB calls
# --------------------------------------------------------------------------
def _load_from_mongo_new(param):
    return apitest.core.loaders._tmp_data


def _load_from_file_new(param):
    return apitest.core.loaders._tmp_data


# --------------------------------------------------------------------------
# Start tests
# --------------------------------------------------------------------------
def test_load_data_runs_invalid_input_data():
    with pytest.raises(AssertionError):
        load_data(None)


def test_load_data_runs_ok_file(apitest_json):

    test_file = "/apitest.json"

    # Build local file
    build_temp_file(test_file)

    apitest.core.loaders._tmp_data = apitest_json
    apitest.core.loaders._load_from_file = _load_from_file_new
    apitest.core.loaders._load_from_mongo = _load_from_mongo_new

    assert isinstance(load_data(test_file), APITest)


def test_load_data_runs_ok_file_uri(apitest_json):

    test_file = "file://apitest.json"

    # Build local file
    build_temp_file(test_file)

    apitest.core.loaders._tmp_data = apitest_json
    apitest.core.loaders._load_from_file = _load_from_file_new
    apitest.core.loaders._load_from_mongo = _load_from_mongo_new

    assert isinstance(load_data(test_file), APITest)


def test_load_data_runs_ok_mongo_uri(apitest_json):

    test_file = "mongodb://127.0.0.1"

    # Build local file
    build_temp_file(test_file)

    apitest.core.loaders._tmp_data = apitest_json
    apitest.core.loaders._load_from_file = _load_from_file_new
    apitest.core.loaders._load_from_mongo = _load_from_mongo_new

    assert isinstance(load_data(test_file), APITest)



