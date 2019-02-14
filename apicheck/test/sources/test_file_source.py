import inspect
import os
import tempfile

from apicheck.sources import file_source


def test_is_a_function():
    assert inspect.isfunction(file_source)


def test_can_read_complete_file():
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write('potatoes')
        content = file_source(path)
        assert content == 'potatoes'
    finally:
        os.remove(path)


def test_except_when_file_not_found():
    try:
        file_source("noway.txt")
    except FileNotFoundError:
        assert True
    else:
        assert False, "Must raise exception if file not exists"


def test_cannot_read_whiout_a_valid_path():
    try:
        file_source(None)
    except ValueError:
        assert True
    else:
        assert False, "Path is requiered"
