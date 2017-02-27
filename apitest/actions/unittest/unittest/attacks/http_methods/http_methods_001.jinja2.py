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
