import pytest

from os.path import join, dirname, abspath

from apitest import APITest, ApitestInvalidFormatError
from apitest.helpers.api_parsers.postman import postman_parser_form_file


@pytest.fixture
def postman_json_path():
    return abspath(join(dirname(__file__), "Postman_Echo.postman_collection.json"))
        

@pytest.fixture
def postman_invalid_json_path():
    return abspath(join(dirname(__file__), "postman_invalid_json.json"))
        

@pytest.fixture
def invalid_json_path():
    return abspath(join(dirname(__file__), "invalid_json.json"))
        

def test_postman_parser_form_file_runs_ok(postman_json_path):
    assert isinstance(postman_parser_form_file(postman_json_path), APITest)


def test_postman_parser_form_file_runs_ok_empty_input():
    with pytest.raises(AssertionError):
        postman_parser_form_file(None)
    

def test_postman_parser_form_file_runs_ok_invalid_postman_file(postman_invalid_json_path):
    with pytest.raises(ApitestInvalidFormatError):
        postman_parser_form_file(postman_invalid_json_path)
        

def test_postman_parser_form_file_runs_ok_invalid_json_file(invalid_json_path):
    with pytest.raises(ApitestInvalidFormatError):
        postman_parser_form_file(invalid_json_path)
