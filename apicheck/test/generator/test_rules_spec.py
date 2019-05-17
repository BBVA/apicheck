import os
import json

import pytest

from apicheck.core.generator import AbsentValue
from apicheck.core.rules import rules_processsor


def test_no_rules():
    req = object
    proc = rules_processsor(None)
    res = proc(req)
    assert res == req
    proc = rules_processsor({})
    res = proc(req)
    assert res == req


def test_endpoint_not_found():
    req = object
    rules = {
        "/my/fine/endpoint": {}
    }

    proc = rules_processsor(None)
    res = proc(req)
    assert res == req
    

def test_custom_policy():
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
    assert res is not None
    assert "path" in res
    assert res["path"] == "/linode/instances/500/disks"
    """
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


def test_custom_policy_complete():
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