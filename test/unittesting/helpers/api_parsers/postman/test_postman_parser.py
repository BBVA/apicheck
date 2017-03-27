import json
import pytest


from os.path import join, dirname, abspath

from actions.parser.postman.parsers import postman_parser
from apitest import APITest, ApitestInvalidFormatError


@pytest.fixture
def postman_info_json():
    example_postman_json = abspath(join(dirname(__file__), "Postman_Echo.postman_collection.json"))
    
    return json.load(open(example_postman_json, "r"))


def test_postman_parser_runs_ok(postman_info_json):
    assert isinstance(postman_parser(postman_info_json,
                                     {
                                         "echo_digest_nonce": "ex",
                                         "echo_digest_realm": "ex2"
                                     }), APITest)


def test_postman_parser_runs_none_input():
    with pytest.raises(AssertionError):
        postman_parser(None)


def test_postman_parser_runs_empty_dict_input():
    with pytest.raises(AssertionError):
        postman_parser({})


def test_postman_parser_runs_invalid_postman_format():
    with pytest.raises(ApitestInvalidFormatError):
        postman_parser(dict(hello="world"))


