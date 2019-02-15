import inspect

from apicheck.formats import openapi


def test_is_a_function():
    assert inspect.isfunction(openapi)


def test_return_none_if_bad_content_passed():
    assert openapi(None) is None
    assert openapi("") is None
    assert openapi("potatoes") is None
