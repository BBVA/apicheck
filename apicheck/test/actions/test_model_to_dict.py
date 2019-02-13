import inspect

from apicheck.actions import model_to_dict
from apicheck.model import EndPointParam


def test_is_function():
    assert inspect.isfunction(model_to_dict)


def test_must_receive_model():
    m = EndPointParam()
    assert model_to_dict()
