from apitest.utils.url_fuzzers import fuzz_value_from_type


def test_fuzz_param_int():
    assert isinstance(fuzz_value_from_type(1), int)


def test_fuzz_param_str():
    assert isinstance(fuzz_value_from_type("hello"), str)


def test_fuzz_param_float():
    assert isinstance(fuzz_value_from_type(1.0), float)


def test_fuzz_param_bool():
    assert isinstance(fuzz_value_from_type(True), bool)
