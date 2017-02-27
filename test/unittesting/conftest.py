import json
import pytest

from os.path import join, dirname

from apitest import APITest


@pytest.fixture
def apitest_invalid_file():
    return join(dirname(__file__), "examples", "apitest_postman_invalid.json")


@pytest.fixture
def apitest_file():
    return join(dirname(__file__), "examples", "apitest_postman.json")


@pytest.fixture
def apitest_json():
    example_json = join(dirname(__file__), "examples", "apitest_postman.json")
    
    return json.load(open(example_json, "r"))
    

@pytest.fixture
def apitest_obj(apitest_json):
    return APITest(**apitest_json)
