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

        

