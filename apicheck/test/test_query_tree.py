import os
import json
import pytest

from dataclasses import dataclass
from typing import Any, Callable, List, Tuple, Set


@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


def ref_resolver(tree):
    def _resolve(element):
        if isinstance(element, dict) and "$ref" in element:
            parts = element["$ref"][2:].split("/")
            target = parts[-1]
            ancestors = set(parts[0:-1])
            ref = search(tree, target, ancestors=ancestors)
            return ref

    return _resolve


def transform_tree(current, transformer):
    change = transformer(current)
    if change:
        return transform_tree(change, transformer)
    elif isinstance(current, dict):
        return {k: transform_tree(v, transformer) for k, v in current.items()}
    elif isinstance(current, list):
        return [transform_tree(v, transformer) for v in current]
    else:
        return current


def _search(current, target, path) -> Tuple[str, object]:
    if isinstance(current, dict):
        if target in current:
            yield (*path, target), current[target]

        for x, y in current.items():
            for res in _search(y, target, (*path, x)):
                yield res
    elif isinstance(current, list):
        for item in current:
            for res in _search(item, target, path):
                yield res


def search(tree: dict,
           target: str,
           ancestors: Set[str] = set([])) -> list:
    for (path, element) in _search(tree, target, tuple()):
        if ancestors <= set(path):
            return element


def search_all(tree: dict,
               target: str,
               ancestors: Set[str] = set([])) -> list:
    res = list()
    for (path, element) in _search(tree, target, tuple()):
        if ancestors <= set(path):
            res.append(element)

    return res


def test_listing_endpoints(openapi3_content):
    res = list(search(openapi3_content, "paths").keys())

    assert isinstance(res, list)
    assert len(res) > 0
    assert isinstance(res[0], str)


def test_get_specific_field(openapi3_content):
    res = search_all(openapi3_content, "version")

    assert isinstance(res, list)
    assert len(res) > 0
    assert isinstance(res[0], str)
    assert res[0] == "4.0.17"


def test_resolve_reference(openapi3_content):
    expected = {
        "description": "Error",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "description": "An object for describing a "
                                               "single error that occurred "
                                               "during the processing of a "
                                               "request.\n",
                                "properties": {
                                    "reason": {
                                        "type": "string",
                                        "description": "What happened to "
                                                       "cause this error. In "
                                                       "most cases, this can "
                                                       "be fixed immediately "
                                                       "by changing the data "
                                                       "you sent in the "
                                                       "request, but in some "
                                                       "cases you will be "
                                                       "instructed to [open "
                                                       "a Support Ticket]("
                                                       "#operation/createTicket) or perform some other action before you can complete the request successfully.\n",
                                        "example": "fieldname must be a "
                                                   "valid value"
                                    },
                                    "field": {
                                        "type": "string",
                                        "description": "The field in the "
                                                       "request that caused "
                                                       "this error. This may "
                                                       "be a path, separated "
                                                       "by periods in the "
                                                       "case of nested "
                                                       "fields. In some "
                                                       "cases this may come "
                                                       "back as \"null\" if "
                                                       "the error is not "
                                                       "specific to any "
                                                       "single element of "
                                                       "the request.\n",
                                        "example": "fieldname"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    res = search(openapi3_content, "default",
                 ancestors=set(["/account", "get", "responses"]))
    resolved = transform_tree(res, ref_resolver(openapi3_content))

    assert isinstance(resolved, dict)
    assert resolved == expected


def test_list_http_methods(openapi3_content):
    methods = ["get", "put", "post", "patch", "delete"]
    res = {
        k: v
        for k, v in search(openapi3_content, "/account").items()
        if k in methods
    }

    assert isinstance(res, dict)
    assert set(list(res.keys())) <= set(methods)


def test_resolve_all_tree(openapi3_content):
    resolved = transform_tree(openapi3_content, ref_resolver(openapi3_content))

    ref = search(resolved, "$ref")
    assert ref is None
