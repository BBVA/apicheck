import pytest

from apitest import APITestHeader
from apitest.helpers.api_parsers.postman import from_http_content_type_get_type


def test_from_http_content_type_get_type_runs_ok_with_body_mode():
    headers = [APITestHeader(key="Language", value="en")]

    assert from_http_content_type_get_type(headers=headers, body_mode="formdata") == "application/www-form-urlencoded"


def test_from_http_content_type_get_type_runs_ok_with_content_type():
    headers = [APITestHeader(key="Content-Type", value="application/json")]

    assert from_http_content_type_get_type(headers=headers, body_mode="formdata") == "application/json"


def test_from_http_content_type_get_type_runs_ok_with_empty_content_type():
    assert from_http_content_type_get_type(headers=[], body_mode=None) == "text/plain"
