import inspect

from apicheck.actions import model_to_dict
from apicheck.model import EndPointParam


def test_is_function():
    assert inspect.isfunction(model_to_dict)


def test_happy_path():
    result = model_to_dict(EndPointParam("pepe"))

    valid_result = {
        "name": "pepe",
        "param_type": "string",
        "description": "",
        "default": None,
        "minimum_value": None,
        "maximum_value": None,
        "max_length": 500,

    }

    assert type(result) is dict
    assert result == valid_result


def test_check_inputs():
    result = model_to_dict(EndPointParam(
        name="juan",
        param_type="integer",
        description="My values",
        default="me",
        minimum_value="1000",
        maximum_value="10000",
        max_length=5000
    ))

    valid_result = {
        "name": "juan",
        "param_type": "integer",
        "description": "My values",
        "default": "me",
        "minimum_value": "1000",
        "maximum_value": "10000",
        "max_length": 5000,

    }

    assert type(result) is dict
    assert result == valid_result
