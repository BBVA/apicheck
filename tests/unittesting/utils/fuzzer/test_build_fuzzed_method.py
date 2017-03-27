import pytest

from apitest.utils.url_fuzzers import build_fuzzed_method


@pytest.fixture
def http_methods():
    return "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "PATH", "CONNECT"


def test_build_fuzzed_method_runs_ok(http_methods):
    assert build_fuzzed_method() in http_methods


def test_build_fuzzed_method_runs_invalid_methods(http_methods):
    assert isinstance(build_fuzzed_method(allow_invalid_methods=True), str)
