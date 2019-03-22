from typing import Tuple, Set


def ref_resolver(tree):
    def _resolve(element):
        if isinstance(element, dict) and "$ref" in element:
            parts = element["$ref"][2:].split("/")
            target = parts[-1]
            ancestors = set(parts[0:-1])
            ref = search(tree, target, ancestors=ancestors)
            return ref

    return _resolve


def transform_tree(current, transformer):
    change = transformer(current)
    if change:
        return transform_tree(change, transformer)
    elif current.__class__.__name__ == "dict":
        return {k: transform_tree(v, transformer) for k, v in current.items()}
    elif current.__class__.__name__ == "list":
        return [transform_tree(v, transformer) for v in current]
    else:
        return current


def _search(current, target, path) -> Tuple[str, object]:
    if isinstance(current, dict):
        if target in current:
            yield (*path, target), current[target]

        for x, y in current.items():
            for res in _search(y, target, (*path, x)):
                yield res
    elif isinstance(current, list):
        for item in current:
            for res in _search(item, target, path):
                yield res


def search(tree: dict,
           target: str,
           ancestors: Set[str] = set([])) -> list:
    for (path, element) in _search(tree, target, tuple()):
        if ancestors <= set(path):
            return element


def search_all(tree: dict,
               target: str,
               ancestors: Set[str] = set([])) -> list:
    res = list()
    for (path, element) in _search(tree, target, tuple()):
        if ancestors <= set(path):
            res.append(element)

    return res
