import pytest

from apitest.core.helpers import make_directoriable


def test_make_directoriable_ok_case():
    assert make_directoriable("Hello World guy!") == "hello_world_guy"


def test_make_directoriable_underline():
    assert make_directoriable("Hello-World-guy!") == "hello_world_guy"


def test_make_directoriable_bad_input():
    assert make_directoriable(None) == ""
