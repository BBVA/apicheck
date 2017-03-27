import pytest

from random import choice, randint

from apitest.utils.url_fuzzers import fuzz_value_from_type, build_fuzzed_url


@pytest.fixture
def url_with_uri_params():
    
    var_names = ["name", "user", "password", "lang", "country"]
    var_types = [1, True, 1.0, "hello"]

    return "http://example.com/api/users?%s" % "&".join("%s=%s" % (var_names[i], fuzz_value_from_type(choice(var_types))) for i in range(randint(1, len(var_names))))


def test_build_fuzzed_url_type(url_with_uri_params):
    r = build_fuzzed_url(url_with_uri_params)
    
    assert isinstance(r, str)


def test_build_fuzzed_url_empty_input():
    r = build_fuzzed_url(None)
    
    assert r == ""


def test_build_fuzzed_url_format(url_with_uri_params):
    r = build_fuzzed_url(url_with_uri_params)
    
    assert len(r.split("&")) > 0


def test_build_fuzzed_url_empty_url_query(url_with_uri_params):
    r = build_fuzzed_url("http://example.com/api/users")
    
    assert r == "http://example.com/api/users"
