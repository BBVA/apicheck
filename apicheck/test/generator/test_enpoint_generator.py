import json
import sys
import os
import random
import re
from typing import Callable, Generator, Tuple, Set

import pytest

from apicheck.core.endpoint import request_generator
from apicheck.core.dict_helpers import search, ref_resolver, transform_tree


@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "..",
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


def test_invalid_info_request_genetaror():
    try:
        request_generator(None)
    except ValueError as ex:
        assert isinstance(ex, ValueError)
    else:
        assert False, "Value Error expected if None data supplied"
    try:
        request_generator({})
    except ValueError as ex:
        assert isinstance(ex, ValueError)
    else:
        assert False, "Value Error expected if empty dict supplied"
    try:
        request_generator(["A", "B", "C"])
    except ValueError as ex:
        assert isinstance(ex, ValueError)
    else:
        assert False, "Value Error expected if not dict supplied"


def test_request_generator_must_return_a_function(openapi3_content):
    res = request_generator(openapi3_content)
    assert isinstance(res, Callable)


def test_request_generator_function_valid_endpoint(openapi3_content):
    query = request_generator(openapi3_content)

    try:
        query(None)
    except ValueError as ex:
        assert isinstance(ex, ValueError)
    else:
        assert False, "Value Error expected if None is supplied as query"
    try:
        query("")
    except ValueError as ex:
        assert isinstance(ex, ValueError)
    else:
        assert False, "Value Error expected if empty string is supplied as query"


def test_request_generator_must_return_a_generator(openapi3_content):
    query = request_generator(openapi3_content)

    res = query("/account")

    assert isinstance(res, Generator)


def test_request_generator_must_return_none_if_query_not_found(openapi3_content):
    query = request_generator(openapi3_content)

    try:
        res = query("/cuck_norris")
    except ValueError as ve:
        assert True
    else:
        assert False, "exception expected"


VALID_PATH = r"/[a-zA-Z0-9/]+"


def test_request_generator_must_return_valid_request(openapi3_content):
    query = request_generator(openapi3_content)

    gen = query("/account")

    res = next(gen)

    assert isinstance(res, dict)

    assert "method" in res, "Response must have a methd"
    the_method = res["method"]
    assert the_method == "get", "the method will be get by default"

    assert "path" in res, "Response must have a path to call"
    the_path = res["path"]
    assert re.match(VALID_PATH, the_path), "must be a valid path"

    assert "headers" in res, "Response must have headers, even if they are empty"
    the_headers = res["headers"]
    assert len(the_headers) == 0, "Headers are empty now"


def test_request_generator_must_return_valid_post_request(openapi3_content):
    query = request_generator(openapi3_content)
    gen = query("/account", method="put")
    res = next(gen)

    assert isinstance(res, dict)

    assert "method" in res
    the_method = res["method"]
    assert the_method == "put"

    assert "path" in res
    the_path = res["path"]
    assert re.match(VALID_PATH, the_path)

    assert "headers" in res
    the_headers = res["headers"]
    assert "Content-Type" in the_headers
    assert the_headers["Content-Type"] == "application/json"

    assert "body" in res
    item = res["body"]
    assert "address_1" in item
    assert "address_2" in item
    assert "balance" in item
    assert "city" in item
    assert "company" in item
    assert "credit_card" in item
    assert "email" in item
    assert "first_name" in item
    assert "last_name" in item
    assert "phone" in item
    assert "state" in item
    assert "tax_id" in item
    assert "zip" in item


def test_no_struct_schema(openapi3_content):
    current = search(openapi3_content, "/linode/instances")
    query = request_generator(openapi3_content)
    try:
        if "get" in current:
            gen = query("/linode/instances")
            res = next(gen)
            assert res is not None
        if "post" in current:
            gen = query("/linode/instances", method="post")
            res = next(gen)
            assert res is not None
    except ValueError as ve:
        print("cannot generate data", ve)
    except Exception as ex:
        assert False, f"uncontrolled exception in, {ex}"


def test_strange_parameters(openapi3_content):
    url = "/linode/instances/{linodeId}/disks"
    current = search(openapi3_content, url)
    query = request_generator(openapi3_content)
    try:
        if "get" in current:
            gen = query(url)
            res = next(gen)
            assert res is not None
        if "post" in current:
            gen = query(url, method="post")
            res = next(gen)
            assert res is not None
    except ValueError as ve:
        print("cannot generate data", ve)
    except Exception as ex:
        assert False, f"uncontrolled exception in, {ex}"


def test_all_in(openapi3_content):
    raw_endpoints = search(openapi3_content, "paths")
    query = request_generator(openapi3_content)
    resolver = ref_resolver(openapi3_content)
    endpoints = transform_tree(raw_endpoints, resolver)

    for url, endpoint in endpoints.items():
        try:
            if "get" in endpoint:
                gen = query(url)
                res = next(gen)
                assert res is not None
            if "put" in endpoint:
                gen = query(url, method="put")
                res = next(gen)
                assert res is not None
            if "post" in endpoint:
                gen = query(url, method="post")
                res = next(gen)
                assert res is not None
            if "delete" in endpoint:
                #TODO: delete generator
                pass
        except ValueError as ve:
            print("cannot generate data", ve, url)
        except Exception as ex:
            assert False, f"uncontrolled exception in {url}, {endpoint}, {ex}"

