def test_sqli_case_001(make_requests):
    current, good, bad = make_requests("{{ url }}")

    assert bad.status_code == current.status_code
    assert bad.body == current.body

