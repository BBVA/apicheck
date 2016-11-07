import pytest

from apitest import APITestContentType, ApitestValueError
from apitest.helpers.api_parsers.postman import from_raw_body_get_python_object


def test_from_raw_body_get_python_object_runs_ok():
    resp = from_raw_body_get_python_object(data_type="application/json", data='[{"user": 1,"password":"hello"}]')
    
    assert resp == [{'user': 1, 'password': 'hello'}]


def test_from_raw_body_get_python_object_empty_data():
    resp = from_raw_body_get_python_object(data_type=None, data='[{"user": 1,"password":"hello"}]')
    
    assert resp == '[{"user": 1,"password":"hello"}]'


def test_from_raw_body_get_python_object_raw_input():
    resp = from_raw_body_get_python_object(data_type=APITestContentType.raw, data='[{"user": 1,"password":"hello"}]')
    
    assert resp == '[{"user": 1,"password":"hello"}]'


def test_from_raw_body_get_python_object_json_input():
    resp = from_raw_body_get_python_object(data_type=APITestContentType.json, data='[{"user": 1,"password":"hello"}]')
    
    assert resp == [{"user": 1,"password":"hello"}]

    
def test_from_raw_body_get_python_object_json_input_invalid_json():
    
    with pytest.raises(ApitestValueError):
        from_raw_body_get_python_object(data_type=APITestContentType.json, data="[{'user': 1}]")
    

def test_from_raw_body_get_python_object_xform_input():
    input_data = [
        {
            "key": "hello",
            "value": "world"
        },
        {
            "key": "hi",
            "value": "you rules!"
        }
    ]
    resp = from_raw_body_get_python_object(data_type=APITestContentType.form, data=input_data)
    
    assert resp == "hello=world&hi=you+rules!"


def test_from_raw_body_get_python_object_xform_input_invalid_input():
    input_data = [
        {
            "blah": "hello",
            "blah2": "world"
        }
    ]
    
    with pytest.raises(ApitestValueError):
        resp = from_raw_body_get_python_object(data_type=APITestContentType.form, data=input_data)
    