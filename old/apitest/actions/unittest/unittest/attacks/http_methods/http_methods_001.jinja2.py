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
from apitest.helpers.fuzzer import build_fuzzed_method


def test_http_methods_case_unexpected(make_requests):
    # Get different method that original request
    method = ""
    while not method and method != "{{ method }}":
        method = build_fuzzed_method()

    response, original, _ = make_requests("{{ url }}",
                                          method=method,
                                          build_fuzzed_response=False)

    assert response.status_code in (500, 405, 404)


def test_http_methods_case_invalid(make_requests):

    response, original, _ = make_requests("{{ url }}",
                                          method="POTATO",
                                          build_fuzzed_response=False)

    assert response.status_code in (500, 405)


def test_http_methods_case_dangerous(make_requests):

    response, original, _ = make_requests("{{ url }}",
                                          method="DELETE",
                                          build_fuzzed_response=False)

    assert response.status_code != 200


def test_http_methods_case_trace(make_requests):

    response, original, _ = make_requests("{{ url }}",
                                          method="TRACE",
                                          build_fuzzed_response=False)

    assert response.status_code != 200
