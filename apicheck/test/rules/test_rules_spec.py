import os
import json

import pytest

from apicheck.core.generator import AbsentValue
from apicheck.core.rules import rules_processor


def _test_ruleset(rules, res_in, expected):
    proc = rules_processor(rules)
    res = proc(res_in)
    assert res is not None
    if expected.__class__.__name__ != "dict":
        return None
    for k, v in expected.items():
        assert k in res
        assert res[k] == v


def test_no_rules():
    req = {}
    _test_ruleset(None, req, req)
    _test_ruleset({}, req, req)


def test_endpoint_not_found():
    req = {}
    rules = {
        "/my/fine/endpoint": {}
    }
    _test_ruleset(rules, req, req)


def test_path_params():
    res_in = {
        "method": "post",
        "path": "/my/entity/33456979458037",
        "headers": []
    }
    rules = {
        "/by/entity/{id}": {
            "pathParams": {
                "id": "a09941c5a-51fe-4379-b6e3-e91b9788b4fb"
            }
        }
    }
    res_out = {
        "method": "post",
        "path": "/my/entity/a09941c5a-51fe-4379-b6e3-e91b9788b4fb",
        "headers": []
    }
    _test_ruleset(rules, res_in, res_out)


def test_query_params():
    res_in = {
        "method": "post",
        "path": "/my/great/endpoint?id=109497203948",
        "headers": []
    }
    rules = {
        "/my/great/endpoint": {
            "queryParams": {
                "id": "10"
            }
        }
    }
    res_out = {
        "method": "post",
        "path": "/my/great/endpoint?id=10",
        "headers": []
    }
    _test_ruleset(rules, res_in, res_out)


def test_query_params_generated():
    res_in = {
        "method": "post",
        "path": "/my/great/endpoint?id=109497203948",
        "headers": []
    }
    rules = {
        "/my/great/endpoint": {
            "queryParams": {
                "id": {
                    "type": "dictionary",
                    "values": [
                        "66"
                    ]
                }
            }
        }
    }
    res_out = {
        "method": "post",
        "path": "/my/great/endpoint?id=66",
        "headers": []
    }
    _test_ruleset(rules, res_in, res_out)


def test_body():
    res_in = {
        "method": "post",
        "path": "/my/great/endpoint",
        "headers": [],
        "body": {
            "first": "hello",
            "then": "loren ipsum"
        }
    }
    rules = {
        "/my/great/endpoint": {
            "body": {
                "then": "world"
            }
        }
    }
    res_out = {
        "method": "post",
        "path": "/my/great/endpoint",
        "headers": [],
        "body": {
            "first": "hello",
            "then": "world"
        }
    }
    _test_ruleset(rules, res_in, res_out)


def test_body_generator():
    res_in = {
        "method": "post",
        "path": "/my/great/endpoint",
        "headers": [],
        "body": {
            "first": "hello",
            "then": "loren ipsum"
        }
    }
    rules = {
        "/my/great/endpoint": {
            "body": {
                "then": {
                    "type": "dictionary",
                    "values": [
                        "world"
                    ]
                }
            }
        }
    }
    res_out = {
        "method": "post",
        "path": "/my/great/endpoint",
        "headers": [],
        "body": {
            "first": "hello",
            "then": "world"
        }
    }
    _test_ruleset(rules, res_in, res_out)


def test_method_filter():
    res_in_s = [
        {
            "method": "get",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "post",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "put",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "delete",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        }
    ]
    rules = {
        "/my/great/endpoint": {
            "queryParams": {
                "id": {
                    "type": "dictionary",
                    "values": [
                        "66"
                    ]
                }
            }
        }
    }
    res_out_s = [
        {
            "method": "get",
            "path": "/my/great/endpoint?id=66",
            "headers": []
        },
        {
            "method": "post",
            "path": "/my/great/endpoint?id=66",
            "headers": []
        },
        {
            "method": "put",
            "path": "/my/great/endpoint?id=66",
            "headers": []
        },
        {
            "method": "delete",
            "path": "/my/great/endpoint?id=66",
            "headers": []
        }
    ]
    for res_in, res_out in zip(res_in_s, res_out_s):
        _test_ruleset(rules, res_in, res_out)


def test_method_get_filter():
    res_in_s = [
        {
            "method": "get",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "post",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "put",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "delete",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        }
    ]
    rules = {
        "/my/great/endpoint": {
            "method": "get",
            "queryParams": {
                "id": {
                    "type": "dictionary",
                    "values": [
                        "66"
                    ]
                }
            }
        }
    }
    res_out_s = [
        {
            "method": "get",
            "path": "/my/great/endpoint?id=66",
            "headers": []
        },
        {
            "method": "post",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "put",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        },
        {
            "method": "delete",
            "path": "/my/great/endpoint?id=109497203948",
            "headers": []
        }
    ]
    for res_in, res_out in zip(res_in_s, res_out_s):
        _test_ruleset(rules, res_in, res_out)


def test_custom_policy():
    res_in = {
        "method": "post",
        "path": "/linode/instances/3850272634059/disks",
        "headers": [],
        "body": {
            "path": "/tmp/example",
            "stackscript_data": AbsentValue("No properties available")
        }
    }
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
    res_out = {
        "method": "post",
        "path": "/linode/instances/500/disks",
        "headers": [],
        "body": {
            "path": "/tmp/example",
            "stackscript_data": "A"
        }
    }
    _test_ruleset(rules, res_in, res_out)
