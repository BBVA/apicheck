import random
import sys

from . import generator, _type_matcher

from faker import Faker


fake = Faker()


def _open_api_str(field: dict, strategies):
    minimum = 10
    maximum = 200
    if "maxLength" in field:
        maximum = field["maxLength"]
    if "minLength" in field:
        minimum = field["minLength"]
    while True:
        r = fake.text()
        while len(r) < minimum:
            r = r + r
        if len(r) > maximum:
            r = r[:maximum-1]
        yield r


def _open_api_object(field: dict, strategies):
    def _make_gen(v):
        return generator(v, strategies)
    if "properties" not in field:
        raise ValueError("Can't gen a property-less object without policy")
    properties = field["properties"]
    prop_builder = []
    # TODO: v my ass, it's a Field!
    for k, v in properties.items():
        g = generator(v, strategies)
        prop_builder.append((k, g))
    while True:
        res = {}
        # TODO: human names
        for k, g in prop_builder:
            next_value = next(g)
            res[k] = next_value
        yield res


def _open_api_int(field: dict, strategies):
    minimum = -sys.maxsize-1
    maximum = sys.maxsize
    if "minimum" in field:
        minimum = field["minimum"]
    if "maximum" in field:
        maximum = field["maximum"]
    if "exclusiveMinimum" in field:
        minimum = minimum+1
    if "exclusiveMaximum" in field:
        maximum = maximum-1
    while True:
        r = random.randint(minimum, maximum)
        if "multipleOf" in field:
            rem = r % field["multipleOf"]
            r = r - rem
        yield r


def _open_api_list(field: dict, strategies):
    def _must_unique(gen):
        for _ in range(1000):
            res = gen()
            if len(res) == len(set(res)):
                return res
        raise ValueError("Cannot generate unique list with this parameters")
    minimum = 1
    if "minItems" in field:
        minimum = field["minItems"]
    maximum = minimum + 9
    if "maxItems" in field:
        maximum = field["maxItems"]
    item_type = field["items"]
    item_gen = generator(item_type, strategies)
    size = random.randint(minimum, maximum)

    def gen():
        return [next(item_gen) for _ in range(size)]

    while True:
        if "uniqueItems" in field and field["uniqueItems"]:
            yield _must_unique(gen())
        # TODO: constant size?
        yield gen()


def _open_api_bool(field: dict, strategies):
    while True:
        n = random.randint(1, 10)
        yield n % 2 == 0


strategy = [
    (_type_matcher("string"), _open_api_str),
    (_type_matcher("integer"), _open_api_int),
    (_type_matcher("number"), _open_api_int),
    (_type_matcher("object"), _open_api_object),
    (_type_matcher("array"), _open_api_list),
    (_type_matcher("boolean"), _open_api_bool)
]
