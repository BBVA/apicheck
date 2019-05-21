from typing import Any, Dict

from apicheck.core.generator import _type_matcher 
from apicheck.core.generator.open_api_strategy import strategy
from apicheck.core.generator.dict_strategy import dict_generator


rules_strategy = strategy + [
    (_type_matcher("dictionary"), dict_generator)
]


def rules_processor(rules: Dict[str, Any]):
    import apicheck.core.rules.path as pa
    import apicheck.core.rules.body as bo

    def _proc(request: Dict[str, Any]):
        # TODO: a request without path it's a valid request?
        if "path" in request:
            endpoint = pa.find_endpoint(rules, request["path"])
            # TODO: how can i deal if no endpoint found?
        else:
            return request
        rule = rules[endpoint]
        if "pathParams" in rule:
            request["path"] = pa.merge_paths(request["path"], endpoint, rule["pathParams"])
        if "queryParams" in rule:
            request["path"] = pa.merge_queries(request["path"], rule["queryParams"])
        if "body" in rule:
            request["body"] = bo.merge_body(request["body"], rule["body"])
        return request
    if not rules or len(rules) == 0:
        return lambda x: x
    return _proc