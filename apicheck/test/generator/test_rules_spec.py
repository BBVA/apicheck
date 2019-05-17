import os
import json

import pytest

from apicheck.core.generator import AbsentValue
# TODO: Everything brand new test


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
    url = "/linode/instances/{linodeId}/disks"
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
        "path": "",
        "headers": [],
        "body": {
            "path": "/tmp/example",
            "stackscript_data": AbsentValue("No properties available")
        }
    }
    res = None
    # TODO: must pass this test
    # assert "/linode/instances/500/disks" == res["path"]


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