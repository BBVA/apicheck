import pytest

from random import choice, randint

from apitest.utils.url_fuzzers import fuzz_value_from_type, build_fuzzed_json


@pytest.fixture
def dummy_data():
    """Build random JSON documents"""
    
    var_names = ["name", "user", "password", "lang", "country", "back", "mode", "action", "before"]
    var_types = [1, True, 1.0, "hello"]
    
    def dummy_recursive_data(deep=-1):
        
        if deep < 0:
            return
        
        # Build a init dict as JSON
        init_data = {var_names[i]: choice(var_types) for i in range(randint(1, len(var_names)))}
        
        # Choice a randon number of sud-documents
        for _ in range(randint(1, 4)):
            recursive_return = dummy_recursive_data(deep - 1)
            if recursive_return:
                init_data[fuzz_value_from_type("a")] = [recursive_return]
        
        return init_data

    return dummy_recursive_data(randint(1, 4))


def test_build_fuzzed_url_type(dummy_data):
    r = build_fuzzed_json(dummy_data)
    
    assert isinstance(r, dict)


def test_build_fuzzed_url_type_empty_input():
    r = build_fuzzed_json(None)
    
    assert r is None


def test_build_fuzzed_url_type_empty_dict_input():
    r = build_fuzzed_json({})
    
    assert r == {}


def test_build_fuzzed_url_format(dummy_data):
    r = build_fuzzed_json(dummy_data)
    
    assert r.keys() == dummy_data.keys()
