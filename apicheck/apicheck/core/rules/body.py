from apicheck.core.generator import generator, _type_matcher 
from apicheck.core.generator.open_api_strategy import strategy
from apicheck.core.generator.dict_strategy import dict_generator


default_strategy = strategy + [
    (_type_matcher("dictionary"), dict_generator)
]


def merge_body(current_body, properties):
    res = {}
    for k, v in current_body.items():
        if k in properties:
            gen = generator(properties[k], default_strategy)
            res[k] = next(gen)
        else:
            res[k] = v
    return res