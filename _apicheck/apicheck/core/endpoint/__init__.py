import re

from apicheck.core.dict_helpers import search, ref_resolver, transform_tree
from apicheck.core.generator import generator, fail, AbsentValue


def _param_generator(strategy, path, parameters):
    def _gen():
        url = path
        for p in parameters:
            if "schema" not in p:
                raise ValueError("cannot generate values without schema!")
            gen = generator(p["schema"], strategy)
            res = next(gen)
            if "in" in p:
                if p["in"] == "path":
                    url = re.sub(r"\{"+p["name"]+r"\}", str(res), url)
                else:
                    raise NotImplementedError("query params")
            else:
                raise NotImplementedError("Nope")
        return url
    while True:
        yield _gen()


def _get_gen(query, item, strategy, params=None):
    path = query
    if params:
        path = _param_generator(strategy, path, params)
    else:
        def _query():
            while True:
                yield query
        path = _query()
    while True:
        yield {
            "method": "get",
            "path": next(path),
            "headers": {},
        }


def _put_gen(query, item, strategy, params=None):
    path = query
    if params:
        path = _param_generator(strategy, path, params)
    else:
        def _query():
            while True:
                yield query
        path = _query()
    current = item["put"]
    body = current["requestBody"]["content"]
    content_type, schema = [(x, y["schema"]) for x, y in body.items()][0]
    gen = generator(schema, strategy)
    while True:
        yield {
            "method": "put",
            "path": next(path),
            "headers": {
                "Content-Type": content_type
            },
            "body": next(gen)
        }


def _post_gen(query, item, strategy, params=None):
    def recover_content_type_schema(cur_item):
        body_spec = current["requestBody"]["content"]
        for x, y in body_spec.items():
            return x, y["schema"]
    path = query
    if params:
        path = _param_generator(strategy, path, params)
    else:
        def _query():
            while True:
                yield query
        path = _query()
    while True:
        res = {
            "method": "post",
            "headers": {}
        }
        res["path"] = next(path)
        current = item["post"]
        if "requestBody" in current:
            content_type, schema = recover_content_type_schema(current)
            gen = generator(schema, strategy)
            res["headers"]["Content-Type"] = content_type
            body = next(gen)
            res["body"] = body
        yield res


def _delete_gen(query, item, strategy, params=None):
    path = query
    if params:
        path = _param_generator(strategy, path, params)
    else:
        def _query():
            while True:
                yield query
        path = _query()
    while True:
        yield {
            "method": "delete",
            "path": next(path),
            "headers": {},
        }


def request_generator(open_api_data: dict,
                      default_strategy: list = []):
    if not open_api_data or not isinstance(open_api_data, dict):
        return fail(AbsentValue("Not openapi data supplied"))
    if not default_strategy:
        from apicheck.core.generator.open_api_strategy import strategy
        default_strategy = strategy
    transformer = ref_resolver(open_api_data)

    def _endpoint_generator(query, ancestors=set([]), method="get"):
        if not query:
            return AbsentValue("Invalid query")
        item = search(open_api_data, query, ancestors=ancestors)
        if not item or method not in item:
            return AbsentValue("Item not found")
        if "parameters" in item:
            parameters = item["parameters"]
        else:
            parameters = None
        resolved = transform_tree(item, transformer)
        if method == "get":
            res = _get_gen(query, resolved, default_strategy, parameters)
        elif method == "put":
            res = _put_gen(query, resolved, default_strategy, parameters)
        elif method == "post":
            res = _post_gen(query, resolved, default_strategy, parameters)
        else:
            res = _delete_gen(query, resolved, default_strategy, parameters)
        return res
    return _endpoint_generator
