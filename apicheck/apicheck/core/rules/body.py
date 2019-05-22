from apicheck.core.generator import generator
from . import rules_strategy


def merge_body(current_body, properties):
    res = current_body.copy()
    res.update(_gen_properties(properties))
    return res


def override_body(current_body, properties):
    return _gen_properties(properties)


def _gen_properties(properties):
    res = {}
    for k, v in properties.items():
        if isinstance(v, dict):
            gen = generator(properties[k], rules_strategy)
            res[k] = next(gen)
        else:
            res[k] = v
    return res
