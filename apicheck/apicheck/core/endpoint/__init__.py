import re


from apicheck.core.dict_helpers import search, ref_resolver, transform_tree
from apicheck.core.generator import generator
from apicheck.core.generator.open_api_strategy import strategy as open_api_strategies


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
                raise NotImplementedError("query params")
        else:
            raise NotImplementedError("Nope")
    return url


def _get_gen(query, item, params=None):
    path = query
    if params:
        path = _param_resolver(path, params)
    yield {
        "method": "get",
        "path": path,
        "headers": {},
    }


def _put_gen(query, item, params=None):
    path = query
    if params:
        path = _param_resolver(path, params)
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


def _post_gen(query, item, params=None):
    res = {
        "method": "post",
        "headers": {}
    }
    path = query
    if params:
        path = _param_resolver(path, params)
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
        if not item:
            raise ValueError("Item not found")
        if not method in item:
            raise ValueError("Method not found on item")
        if "parameters" in item:
            parameters = item["parameters"]
        else:
            parameters = None
        resolved = transform_tree(item, transformer)
        if method == "get":
            res = _get_gen(query, resolved, parameters)
        elif method == "put":
            res = _put_gen(query, resolved, parameters)
        elif method == "post":
            res = _post_gen(query, resolved, parameters)
        else:
            raise NotImplementedError("No way man")
        return res
    return _enpoint_generator
