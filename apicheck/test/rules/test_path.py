import apicheck.core.rules.path as pa


def test_find_endpoint_invalid_params():
    none_expected_cases = [
        (None, None),
        ({}, None),
        (None, {}),
        ({}, {})
    ]

    for a, b in none_expected_cases:
        res = pa.find_endpoint(a, b)
        assert res is None


def test_find_endpoint_happy_path():
    path = "/some/good/path"
    rules = {
        path: {}
    }
    res = pa.find_endpoint(rules, path)
    assert res == path


def test_find_endpoint_with_params():
    path = "/some/{thing}/is/dinamic"
    rules = {
        path: {}
    }
    res = pa.find_endpoint(rules, "/some/how/is/dinamic")
    assert res == path