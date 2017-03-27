import pytest

from os.path import join, basename

from apitest.core.helpers import find_files_by_extension, ApitestNotFoundError


@pytest.fixture
def test_path(tmpdir):
    
    for x in ('xx1.jinja2.py', 'xx1.jinja.py', 'xx1.txt'):
        open(join(str(tmpdir), x), "w").write("xxx")
    
    yield str(tmpdir)


def test_find_files_by_extension_runs_ok(test_path):
    
    oks_returns = {join(test_path, "xx1.jinja2.py"), join(test_path, "xx1.jinja.py")}
    func_returns = set(list(x for x in find_files_by_extension(test_path)))

    assert len(func_returns) == 2
    assert len(oks_returns.difference(func_returns)) == 0


def test_find_files_by_extension_invalid_extensions(test_path):
    
    oks_returns = {join(test_path, "xx1.jinja2.py")}
    func_returns = set(list(x for x in find_files_by_extension(test_path,
                                                               extensions=("jinja2.py", ))))

    assert len(func_returns) == 1
    assert len(oks_returns.difference(func_returns)) == 0


def test_find_files_by_extension_invalid_input_value():

    with pytest.raises(AssertionError):
        assert list(find_files_by_extension(None))


def test_find_files_by_extension_non_exits_input_path():

    with pytest.raises(ApitestNotFoundError):
        assert list(find_files_by_extension(""))
