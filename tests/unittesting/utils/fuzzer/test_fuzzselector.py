import pytest

from apitest.utils.url_fuzzers import FUZZSelector


def test_fuzzselector_type():
    with pytest.raises(ValueError):
        FUZZSelector(None)


def test_fuzzselector_invalid_length():
    with pytest.raises(ValueError):
        FUZZSelector(1111111)


def test_fuzzselector_test_url():
    f = FUZZSelector(FUZZSelector.URL)
    assert f.is_url is True


def test_fuzzselector_test_body():
    f = FUZZSelector(FUZZSelector.BODY)
    assert f.is_body is True


def test_fuzzselector_test_cookies():
    f = FUZZSelector(FUZZSelector.COOKIE)
    assert f.is_cookie is True


def test_fuzzselector_test_headers():
    f = FUZZSelector(FUZZSelector.HEADER)
    assert f.is_header is True


def test_fuzzselector_test_method():
    f = FUZZSelector(FUZZSelector.METHOD)
    assert f.is_method is True


def test_fuzzselector_test_composed_values():
    f = FUZZSelector(FUZZSelector.HEADER | FUZZSelector.URL)
    assert f.is_header is True
    assert f.is_url is True
