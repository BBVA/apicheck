import apicheck.core.rules.path as pa


def rules_processsor(rules):
    def _proc(request):
        endpoint = pa.find_endpoint(rules, request["path"])
        return request
    return _proc