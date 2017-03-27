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


