import pytest

from os.path import join, basename

from apitest.core.helpers import find_files_by_extension, ApitestNotFoundError


@pytest.fixture
def test_path(tmpdir):
    
    for x in ('xx1.jinja', 'xx1.jinja2', 'xx1.txt'):
        open(join(str(tmpdir), x), "w").write("xxx")
    
    return str(tmpdir)


def test_find_files_by_extension_runs_ok(test_path):
    
    oks_returns = {join(test_path, "xx1.jinja2"), join(test_path, "xx1.jinja")}
    func_returns = set(list(x for x in find_files_by_extension(test_path)))

    assert len(func_returns) == 2
    assert len(oks_returns.difference(func_returns)) == 0


def test_find_files_by_extension_invalid_extensions(test_path):
    
    oks_returns = {join(test_path, "xx1.jinja2")}
    func_returns = set(list(x for x in find_files_by_extension(test_path, extensions=("jinja", ))))

    assert len(func_returns) == 1
    assert len(oks_returns.difference(func_returns)) == 1


def test_find_files_by_extension_invalid_input_value():

    with pytest.raises(AssertionError):
        assert list(find_files_by_extension(None))


def test_find_files_by_extension_non_exits_input_path():

    with pytest.raises(ApitestNotFoundError):
        assert list(find_files_by_extension(""))
