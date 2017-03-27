import pytest

from os.path import join, dirname, abspath

from actions.parser.postman.parsers import postman_parser_form_file
from apitest import APITest, ApitestInvalidFormatError


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
    assert isinstance(postman_parser_form_file(postman_json_path,
                                               {
                                                   "echo_digest_nonce": "ex",
                                                   "echo_digest_realm": "ex2"
                                               }), APITest)


def test_postman_parser_form_file_runs_ok_empty_input():
    with pytest.raises(AssertionError):
        postman_parser_form_file(None)
    

def test_postman_parser_form_file_runs_ok_invalid_postman_file(postman_invalid_json_path):
    with pytest.raises(ApitestInvalidFormatError):
        postman_parser_form_file(postman_invalid_json_path)
        

def test_postman_parser_form_file_runs_ok_invalid_json_file(invalid_json_path):
    with pytest.raises(ApitestInvalidFormatError):
        postman_parser_form_file(invalid_json_path)
