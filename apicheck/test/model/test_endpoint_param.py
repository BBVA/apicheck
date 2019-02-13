import inspect

from apicheck.model import EndPointParam


def test_is_a_class():
    assert inspect.isclass(EndPointParam)


def test_can_create():
    EndPointParam(
        "name",
        "name",
        "name",
        "name",
        "name",
        "name",
        1
    )

    assert True


def test_has_correct_properties():

    properties = {
        "name": "name",
        "param_type": "name",
        "description": "name",
        "default": "name",
        "minimum_value": "name",
        "maximum_value": "name",
        "max_length": 1,

    }

    o = EndPointParam(**properties)

    for param_name, param_value in properties.items():
        assert hasattr(o, param_name)
        assert getattr(o, param_name) is param_value


def test_properties_has_correct_types():

    properties = {
        "name": ("name", str),
        "param_type": ("name", str),
        "description": ("name", str),
        "default": ("name", str),
        "minimum_value": ("name", str),
        "maximum_value": ("name", str),
        "max_length": (1, int),
    }

    o = EndPointParam(**{x: y[0] for x, y in properties.items()})

    for param_name, (param_value, param_type) in properties.items():

        assert hasattr(o, param_name)
        assert getattr(o, param_name) is param_value
        assert type(getattr(o, param_name)) is param_type


def test_properties_invalid_types_has_exception():

    incorrect_properties = {
        "name": 1,
        "param_type": 1,
        "description": 1,
        "default": 1,
        "minimum_value": 1,
        "maximum_value": 1,
        "max_length": "",
    }
    correct_properties = {
        "name": "name",
        "param_type": "name",
        "description": "name",
        "default": "name",
        "minimum_value": "name",
        "maximum_value": "name",
        "max_length": 1,
    }

    for incorrect_pro, incorrect_value in incorrect_properties.items():
        new_params = correct_properties.copy()
        new_params[incorrect_pro] = incorrect_value
        try:
            EndPointParam(**new_params)
        except ValueError:
            assert True
        else:
            assert False, f"Property '{incorrect_pro}' has invalid type"
