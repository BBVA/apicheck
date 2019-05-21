from apicheck.core.generator import generator
from . import rules_strategy


def merge_body(current_body, properties):
    res = {}
    for k, v in current_body.items():
        if k in properties:
            gen = generator(properties[k], rules_strategy)
            res[k] = next(gen)
        else:
            res[k] = v
    return res