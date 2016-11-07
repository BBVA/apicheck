{%- if url_params|length != 0 %}
from apitest.helpers.fuzzer import build_fuzzed_method

# --------------------------------------------------------------------------
# Test for URL content parameters
# --------------------------------------------------------------------------
    {%- for payload in payloads %}
        {%- set outer_loop = loop %}
        {%- for url_param_key, url_param_value in url_params.items() %}
def test_xss_url_case_00{{ loop.index }}_payload_00{{ outer_loop.index }}_param_{{ url_param_key | replace("-", "_") }}(make_requests):
    # Payload: {{ payload }}
    response, original, _ = make_requests("{{ url }}",
                                          method="{{ method }}")

    assert response.status_code != original.status_code

        {%- endfor %}

    {% endfor %}
{% endif %}