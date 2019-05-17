import apicheck.core.rules.path as pa


def rules_processsor(rules):
    def _proc(request):
        endpoint = pa.find_endpoint(rules, request["path"])
        rule = rules[endpoint]
        if "pathParams" in rule:
            request["path"] = pa.merge_paths(request["path"], endpoint, rule["pathParams"])
        return request
    if not rules or len(rules) == 0:
        return lambda x: x
    return _proc