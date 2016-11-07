import pytest

from apitest.core.helpers import make_url_signature


@pytest.fixture
def dummy_data_order_1():
    return "http://example.com/api/users", \
           "GET", \
           {
               "Content-Type": "application/x-www-form-urlencoded",
               "Host": "example.com"
           }, \
           "user=John&password=2", \
           "440d9139b8df911602587a8615f92b06e3fe4901"


@pytest.fixture
def dummy_data_order_2():
    
    # This fixture change the order of body: user / password
    return "http://example.com/api/users", \
           "GET", \
           {
               "Host": "example.com",
               "Content-Type": "application/x-www-form-urlencoded"
           }, \
           "password=2&user=John", \
           "440d9139b8df911602587a8615f92b06e3fe4901"


def test_make_url_signature_format(dummy_data_order_1):
    url, method, headers, body, signature = dummy_data_order_1
    
    assert isinstance(make_url_signature(url, method=method, headers=headers, body=body), str)


def test_make_url_signature_signature(dummy_data_order_1):
    url, method, headers, body, signature = dummy_data_order_1
    
    assert make_url_signature(url,
                              method=method,
                              headers=headers,
                              body=body) == "440d9139b8df911602587a8615f92b06e3fe4901"


def test_make_url_signature_signature_invalid_content_type(dummy_data_order_1):
    url, method, headers, body, signature = dummy_data_order_1
    
    headers["Content-Type"] = "application/json"
    
    assert make_url_signature(url,
                              method=method,
                              headers=headers,
                              body=body) == "f23096e8f195e0932d92b34c155d34f3558eb923"


def test_make_url_signature_signature_order(dummy_data_order_1, dummy_data_order_2):
    url1, method1, headers1, body1, signature1 = dummy_data_order_1
    url2, method2, headers2, body2, signature2 = dummy_data_order_2
    
    url_signature_1 = make_url_signature(url1,
                                         method=method1,
                                         headers=headers1,
                                         body=body1)
    
    url_signature_2 = make_url_signature(url2,
                                         method=method2,
                                         headers=headers2,
                                         body=body2)
    
    assert url_signature_1 == url_signature_2
