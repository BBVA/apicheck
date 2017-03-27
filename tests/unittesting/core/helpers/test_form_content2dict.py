import pytest

from apitest.core.helpers import form_content2dict


def test_form_content2dict_runs_ok():
    assert form_content2dict("user=john&password=1234") == {"user": "john", "password": "1234"}


def test_form_content2dict_runs_null_input():
    assert form_content2dict(None) == dict(form_data="")
    

def test_form_content2dict_runs_invalid_input():
    assert form_content2dict("aaaaa") == dict(form_data="aaaaa")
