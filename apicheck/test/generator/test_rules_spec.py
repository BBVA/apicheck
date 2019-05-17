import os
import json

import pytest

from apicheck.core.generator import AbsentValue
from apicheck.core.rules import rules_processsor


@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "..",
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


def test_custom_policy(openapi3_content):
    rules = {
        "/linode/instances/{linodeId}/disks": {
            "pathParams": {
                "linodeId": 500
            },
            "body": {
                "stackscript_data": {
                    "type": "dictionary",
                    "values": [
                        "A"
                    ]
                }
            }
        }
    }
    res_in = {
        "method": "post",
        "path": "/linode/instances/3850272634059/disks",
        "headers": [],
        "body": {
            "path": "/tmp/example",
            "stackscript_data": AbsentValue("No properties available")
        }
    }
    proc = rules_processsor(rules)
    res = proc(res_in)
    """
    assert res is not None
    assert "path" in res
    assert res["path"] == "/linode/instances/500/disks"
    assert "method" in res
    assert res["method"] == "post"
    assert "headers" in res
    assert len(res["headers"]) == 0
    assert "body" in res
    assert "path" in res["body"]
    assert res["body"]["path"] == "/tmp/example"
    assert "stackscript_data" in res["body"]
    assert not isinstance(res["body"]["stackscript_data"], AbsentValue)
    assert res["body"]["stackscript_data"] == "A"
    """


def test_custom_policy_complete(openapi3_content):
    url = "/linode/instances/{linodeId}/disks"

    # TODO: methods could be: a list or a string
    rules = {
        "/linode/instances/{linodeId}/disks": {
            "methods": "get",
            "pathParams": {},
            "headers": {},
            "queryParams": {},
            "body": {
                "stackscript_data": {
                    "type": "dictionary",
                    "values": [
                        "A"
                    ]
                }
            }
        }
    }
    # TODO
    assert True