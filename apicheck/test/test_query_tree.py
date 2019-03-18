import os
import json
import pytest

from dataclasses import dataclass
from typing import Any, Callable, List, Tuple, Set


@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


unit = lambda x: x


def childs(tree: dict, parent: str, parser: Callable = unit) -> dict:
    if parent in tree:
        return parser(tree[parent])


def childs_in_lineage(tree: dict,
                      target: str,
                      ancestors: Set[str] = set([]),
                      parser: Callable = unit) -> dict:
    def recurse(current_tree: dict or list, path: Tuple[str]) -> List[dict]:
        ret = []
        if isinstance(current_tree, list):
            for x in current_tree:
                r = recurse(x, path)
                if r:
                    ret.extend(r)

        elif isinstance(current_tree, dict):
            subset = set(ancestors)
            superset = set(path)
            if target in current_tree and subset <= superset:
                return [(path, current_tree[target])]

            for x, y in current_tree.items():
                r = recurse(y, (*path, x))
                if r:
                    ret.extend(r)

        return ret

    return recurse(tree, tuple())


def test_query_without_lineage(openapi3_content):
    res = childs_in_lineage(openapi3_content,
        "title"
    )
    assert isinstance(res, list)
    assert len(res) > 1
    _, title = res[0]
    assert title == "Linode API"


def test_query_get_paths_responses(openapi3_content):
    result = childs_in_lineage(
        openapi3_content,
        "description",
        set(["post", "requestBody"]))

    print(result)
    assert True


# def test_query_get_paths_ref(openapi3_content):
#     result = childs_in_lineage(
#         openapi3_content,
#         "get",
#         "responses")
#
#     for path, content in result:
#         print(path)
#         print(content)
#     assert isinstance(result, dict)
