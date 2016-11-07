import pytest
    

@pytest.fixture(scope="module")
def make_requests(make_request, request_good, request_bad):
    def _make_req(url, *, method="GET", headers=None, body=None):
        
        # --------------------------------------------------------------------------
        # Generate and cache a GOOD response from original END-POINT API Request
        # --------------------------------------------------------------------------
        resp_ok = request_good(url, method=method, headers=headers, body=body)

        # --------------------------------------------------------------------------
        # Generate and cache a BAD response from original END-POINT API Request
        # --------------------------------------------------------------------------
        resp_bad = request_bad(url, method=method, headers=headers, body=body)
        
        # --------------------------------------------------------------------------
        # Make the current request
        # --------------------------------------------------------------------------
        resp_from_test = make_request(url=url, method=method, headers=headers, body=body)
        
        return resp_from_test, resp_ok, resp_bad
    
    return _make_req
