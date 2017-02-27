import pytest
import requests

from requests.cookies import RequestsCookieJar

try:
    import ujson as json
except ImportError:
    import json

from apitest.helpers.fuzzer import *
from apitest.core.helpers import make_url_signature


class Response(object):
    """
    This class is a wrapper of requests response. This is necessary because py.test cache need a JSON serializable
    data type.
    
    This class only get useful requests response data, and make it serializable.
    """
    
    def __init__(self, *, status_code: int = 200, headers: dict = None, cookies: dict = None,
                 reason: str = None, body: str = None):
        
        body = body or ""
        status_code = status_code or 200
        headers = headers or {}
        cookies = cookies or {}
        if isinstance(cookies, RequestsCookieJar):
            cookies = dict(cookies)
        reason = reason or "OK"
        
        assert isinstance(body, str)
        assert isinstance(reason, str)
        assert isinstance(headers, dict)
        assert isinstance(cookies, dict)
        assert isinstance(status_code, int)
        assert isinstance(status_code, int)
        
        self.body = body
        self.reason = reason
        self.headers = headers
        self.cookies = cookies
        self.status_code = status_code
        
        self.__content_type_cache = None
        self.__content_body_cache = None
    
    @classmethod
    def build_from_json(cls, **kwargs):
        o = cls(status_code=kwargs.get("status_code"),
                headers=kwargs.get("headers"),
                body=kwargs.get("body"),
                cookies=kwargs.get("cookies"),
                reason=kwargs.get("reason"))
        
        return o
    
    @property
    def dump_json(self):
        
        return {key: value for key, value in vars(self).items() if not key.startswith("_")}
    
    @property
    def json_body(self):
        """
        :return: return content type as JSON data type, if content Type of response is JSON
        :rtype: dict
        """
        if not self.__content_body_cache:
            if self.content_type == "json":
                self.__content_body_cache = json.loads(self.body)
            else:
                self.__content_body_cache = self.body
        
        return self.__content_body_cache
    
    @property
    def content_type(self):
        """
        :return: return a string with the content type. Available values are: "json", "raw"
        :rtype: str
        """
        if not self.__content_type_cache:
            if any(True for value in self.headers.values() if "application/json" in value):
                self.__content_type_cache = "json"
            else:
                self.__content_type_cache = "raw"
        
        return self.__content_type_cache


@pytest.fixture(scope="module")
def request_good(request):
    def _new_fn(url: str, *, method: str = "GET", headers: dict = None, body: str = None):
        # Get the unique signature for the Query
        url_signature = "%s_ok" % make_url_signature(url,
                                                     method=method,
                                                     headers=headers,
                                                     body=body)
        
        response = request.config.cache.get(url_signature, None)
        # If response is not cached
        if not response:
            # Get and store a GOOD requests
            raw_response = requests.request(url=url, method=method, headers=headers, data=body)
            
            response = Response(status_code=raw_response.status_code,
                                headers=dict(raw_response.headers),
                                cookies=raw_response.cookies,
                                reason=raw_response.reason,
                                body=raw_response.text)
            
            request.config.cache.set(url_signature, response.dump_json)
        else:
            # Recover response from cached info
            response = Response.build_from_json(**response)
        
        return response
    
    return _new_fn


@pytest.fixture(scope="module")
def request_bad(request):
    def _new_fn(url: str, *, method: str = "GET", headers: dict = None, body: str = None, fuzz_selector: int = None):
        url_signature = "%s_bad" % make_url_signature(url,
                                                      method=method,
                                                      headers=headers,
                                                      body=body)
        
        # Get selectors
        fuzz_opt = fuzz_selector or FUZZSelector.BODY | FUZZSelector.BODY
        
        # Build fuzzer options
        fuzzer = FUZZSelector(fuzz_opt)
        
        response = request.config.cache.get(url_signature, None)
        # If response is not cached
        if not response:
    
            # --------------------------------------------------------------------------
            # Fuzz selected values
            # --------------------------------------------------------------------------
            fuzzed_url = build_fuzzed_url(url) if fuzzer.is_url else url
            fuzzed_headers = build_fuzzed_http_header(headers) if fuzzer.is_header else headers
            fuzzed_method = build_fuzzed_method() if fuzzer.is_method else method
            
            if headers and "application/json" in headers.values():
                # TODO: make for dump_json
                fuzzed_body = build_fuzzed_x_form(body)
            else:
                fuzzed_body = build_fuzzed_x_form(body)
            
            # Get and store a BAD requests
            raw_response = requests.request(url=fuzzed_url, method=fuzzed_method, headers=fuzzed_headers, data=fuzzed_body)
            
            response = Response(status_code=raw_response.status_code,
                                headers=dict(raw_response.headers),
                                cookies=raw_response.cookies,
                                reason=raw_response.reason,
                                body=raw_response.text)
            
            request.config.cache.set(url_signature, response.dump_json)
        
        else:
            response = Response.build_from_json(**response)
        
        return response
    
    return _new_fn


@pytest.fixture(scope="module")
def make_request():
    def _new_fn(url: str, *, method: str = "GET", headers: dict = None, body: str = None):
        raw_response = requests.request(url=url, method=method, headers=headers, data=body)
        
        return Response(status_code=raw_response.status_code,
                        headers=dict(raw_response.headers),
                        cookies=raw_response.cookies,
                        reason=raw_response.reason,
                        body=raw_response.text)
    
    return _new_fn
