def test_has_endpoint_param():
    try:
        from apicheck.model import EndPointParam
    except ImportError:
        assert False, "EndPointparam not found"


def test_has_endpoint_response():
    try:
        from apicheck.model import EndPointResponse
    except ImportError:
        assert False, "EndPointResponse not found"


def test_has_action_to_dict():
    try:
        from apicheck.actions import model_to_dict
    except ImportError:
        assert False, "Can't find 'model_to_dict' action"
