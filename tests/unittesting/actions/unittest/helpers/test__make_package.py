import pytest

from os.path import join, exists

from apitest import ApitestNotFoundError
from apitest.actions.unittest.helpers import _make_package


def test__make_package_runs_ok(tmpdir):
    # Create __init__.py
    _make_package(str(tmpdir))
    
    # Check file __init__.py exits
    assert exists(join(str(tmpdir), "__init__.py")) is True


def test___make_package_runs_none_input():

    with pytest.raises(AssertionError):
        _make_package(None)
        

def test___make_package_runs_non_exits_path(tmpdir):

    with pytest.raises(ApitestNotFoundError):
        _make_package(join(str(tmpdir), "xxxxxx"))
