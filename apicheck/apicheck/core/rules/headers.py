from apicheck.core.generator import generator
from . import rules_strategy


def merge_headers(current_headers, rules):
    res = current_headers.copy()
    res.update(_gen_properties(rules))
    return res


def override_headers(_, rules):
    return _gen_properties(rules)


def _gen_properties(rules):
    res = {}
    for k, v in rules.items():
        if isinstance(v, dict):
            gen = generator(rules[k], rules_strategy)
            res[k] = next(gen)
        else:
            res[k] = v
    return res
