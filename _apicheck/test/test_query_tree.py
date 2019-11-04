import os
import json
import pytest

from dataclasses import dataclass
from typing import Any, Callable, List, Tuple, Set

from apicheck.core.dict_helpers import search, search_all, transform_tree, ref_resolver


@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


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


