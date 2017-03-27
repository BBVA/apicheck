import pytest

from random import choice, randint

from apitest.utils.url_fuzzers import fuzz_value_from_type, build_fuzzed_http_header


@pytest.fixture
def dummy_data():
    var_names = ["Content-Type", "User-Agent", "Host", "Language", "Accept-Language"]

    return {var_names[i]: fuzz_value_from_type(choice("a")) for i in range(randint(1, len(var_names)))}


def test_build_fuzzed_http_header_type(dummy_data):
    r = build_fuzzed_http_header(dummy_data)
    
    assert isinstance(r, dict)


def test_build_fuzzed_http_header_values(dummy_data):
    r = build_fuzzed_http_header(dummy_data)
    
    assert dummy_data.keys() == r.keys()
