import inspect

from apicheck.model import EndPointResponse, EndPointParam


def test_is_a_class():
    assert inspect.isclass(EndPointResponse)


def test_can_create():
    EndPointResponse(200, "application/json", "", [], {})

    assert True


def test_has_correct_properties():

    properties = {
        "http_code": 200,
        "content_type": "application/json",
        "description": "name",
        "params": [],
        "headers": {},

    }

    o = EndPointResponse(**properties)

    for param_name, param_value in properties.items():
        assert hasattr(o, param_name)
        assert getattr(o, param_name) is param_value


def test_properties_has_correct_types():

    properties = {
        "http_code": (200, int),
        "content_type": ("application/json", str),
        "description": ("des", str),
        "params": ([], list),
        "headers": ({}, dict)
    }

    o = EndPointResponse(**{x: y[0] for x, y in properties.items()})

    for param_name, (param_value, param_type) in properties.items():

        assert hasattr(o, param_name)
        assert getattr(o, param_name) is param_value
        assert type(getattr(o, param_name)) is param_type


def test_properties_invalid_types_has_exception():

    incorrect_properties = {
        "http_code": "",
        "content_type": 1,
        "description": 1,
        "params": 1,
        "headers": 1,
    }
    correct_properties = {
        "http_code": 0,
        "content_type": "name",
        "description": "name",
        "params": [],
        "headers": {},
    }

    for incorrect_pro, incorrect_value in incorrect_properties.items():
        new_params = correct_properties.copy()
        new_params[incorrect_pro] = incorrect_value
        try:
            EndPointResponse(**new_params)
        except ValueError:
            assert True
        else:
            assert False, f"Property '{incorrect_pro}' has invalid type"


def test_property_params_has_correct_type():
    correct_properties = {
        "http_code": 200,
        "content_type": "name",
        "description": "name",
        "params": 0,
        "headers": 0
    }

    try:
        EndPointResponse(**correct_properties)
    except ValueError:
        assert True
    else:
        assert False


def test_property_params_hast_correct_linked_type():
    correct_properties = {
        "http_code": 200,
        "content_type": "name",
        "description": "name",
        "params": [EndPointParam("name")],
        "headers": {"Content-Type": "application/json"}
    }

    try:
        EndPointResponse(**correct_properties)
    except ValueError:
        assert True
    else:
        assert False


def test_default_values():
    properties = {
        "http_code": 200,
        "content_type": "application/json",
        "description": None,
        "params": [],
        "headers": {}
    }

    e = EndPointResponse()

    for pro_name, prop_default in properties.items():
        assert getattr(e, pro_name) == prop_default, \
                f"Property '{pro_name}' has invalid default " \
                f"value: '{prop_default}'"


def test_is_frozen():
    e = EndPointResponse()

    try:
        e.http_code = 300
    except AttributeError:
        assert True
    else:
        assert False


def test_property_http_code_has_correct_value():
    try:
        EndPointResponse(http_code=9000)
    except ValueError:
        assert True
    else:
        assert False


def test_valid_content_types():
    try:
        EndPointResponse(content_type="XXXXX")
    except ValueError:
        assert True
    else:
        assert False
