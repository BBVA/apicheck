import json
import sys
import os
import random
import re
from typing import Callable, Generator, Tuple, Set

import pytest

from apicheck.core.dict_helpers import search, ref_resolver, transform_tree
from apicheck.core.generator import generator
from apicheck.core.generator.open_api_strategy import strategy as open_api_strategies


@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "..",
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


def _param_resolver(path, parameters):
    url = path
    for p in parameters:
        if not "schema" in p:
            raise ValueError("cannot generate values without schema!")
        gen = generator(p["schema"], open_api_strategies)
        res = next(gen)
        if "in" in p:
            if p["in"] == "path":
                url = re.sub(r"\{"+p["name"]+"\}", str(res), url)
        else:
            raise NotImplementedError("Nope")
    return url


def _get_gen(query, item):
    path = query
    if "parametrs" in item:
        raise NotImplementedError("Nope")
    yield {
        "method": "get",
        "path": path,
        "headers": {},
    }


def _put_gen(query, item):
    path = query
    current = item["put"]
    body = current["requestBody"]["content"]
    content_type, schema = [(x, y["schema"]) for x, y in body.items()][0]
    gen = generator(schema, open_api_strategies)
    yield {
        "method": "put",
        "path": path,
        "headers": {
            "Content-Type": content_type
        },
        "body": next(gen)
    }


def _post_gen(query, item):
    res = {
        "method": "post",
        "headers": {}
    }
    path = query
    if "parameters" in item:
        path = _param_resolver(path, item["parameters"])
    res["path"] = path
    current = item["post"]
    if "requestBody" in current:
        body_spec = current["requestBody"]["content"]
        content_type, schema = [(x, y["schema"]) for x, y in body_spec.items()][0]
        gen = generator(schema, open_api_strategies)
        res["headers"]["Content-Type"] = content_type
        body = next(gen)
        res["body"] = body
    yield res



def request_generator(open_api_data:dict, defautl_strategy:list=None, extended_strategy:list=None):
    if not open_api_data or not isinstance(open_api_data, dict):
        raise ValueError("Not data supplied")
    transformer = ref_resolver(open_api_data)
    def _enpoint_generator(query, ancestors=set([]), method="get"):
        if not query:
            raise ValueError("Invalid query")
        item = search(open_api_data, query, ancestors=ancestors)
        if not item or not method in item:
            return None
        resolved = transform_tree(item, transformer)
        if method == "get":
            return _get_gen(query, resolved)
        elif method == "put":
            return _put_gen(query, resolved)
        elif method == "post":
            return _post_gen(query, resolved)
        raise NotImplementedError("Nope")
    return _enpoint_generator


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

    res = query("/cuck_norris")

    assert res is None, "Must be none if query not found"


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
    endpoint = search(openapi3_content, "/linode/instances")
    #TODO: research about this fucking thing


def tost_all_in(openapi3_content):
    endpoints = search(openapi3_content, "paths")
    query = request_generator(openapi3_content)
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

