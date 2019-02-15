import inspect

from apicheck.formats import openapi


def test_is_a_function():
    assert inspect.isfunction(openapi)
