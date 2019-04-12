# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest


@pytest.fixture(scope="module")
def make_requests(make_request, request_good, request_bad):
    def _make_req(url: str, *, method: str = "GET",
                  headers: dict = None, body: str = None,
                  build_fuzzed_response: bool = True, build_good_response: bool = True):

        # --------------------------------------------------------------------------
        # Generate and cache a GOOD response from original END-POINT API EndPointRequest
        # --------------------------------------------------------------------------
        resp_ok = None
        if build_good_response:
            resp_ok = request_good(url, method=method, headers=headers, body=body)

        # --------------------------------------------------------------------------
        # Generate and cache a BAD response from original END-POINT API EndPointRequest
        # --------------------------------------------------------------------------
        resp_bad = None
        if build_fuzzed_response:
            resp_bad = request_bad(url, method=method, headers=headers, body=body)

        # --------------------------------------------------------------------------
        # Make the current request
        # --------------------------------------------------------------------------
        resp_from_test = make_request(url=url, method=method, headers=headers, body=body)

        return resp_from_test, resp_ok, resp_bad

    return _make_req
