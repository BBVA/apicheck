{% if body_content %}
from apitest.helpers.fuzzer import build_fuzzed_method

    {% for payload in payloads %}

# --------------------------------------------------------------------------
# Test for body content parameters
# --------------------------------------------------------------------------
        {% for body_key, body_value in body_content.items() %}

def test_xss_body_case_00{{ loop.index }}_param_{{ body_key | lower | replace("-", "_") }}(make_requests):
    # {{ payload }}

    response, original, _ = make_requests("{{ url }}",
    method="{{ method }}")

    assert response.status_code != original.status_code

        {% endfor %}

    {% endfor %}
{% endif %}