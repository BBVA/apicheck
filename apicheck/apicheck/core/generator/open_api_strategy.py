import random
import sys
from typing import Iterator

from faker import Faker

from . import AbsentValue, _type_matcher, generator

fake = Faker()


def _open_api_str(field: dict, strategies) -> Iterator[str]:
    """
    Yields a string of fake text with a length between 10 and 200, or between
    field["minLength"] and field["maxLength"] if those are defined.

    :param field: specification of a field
    """
    def _fail(element):
        return lambda: element

    def _generate():
        r = fake.text()
        while len(r) < minimum:
            r = r + r
        if len(r) > maximum:
            r = r[:maximum-1]
        return r
    minimum = 10
    maximum = 200
    if "maxLength" in field:
        maximum = field["maxLength"]
    if "minLength" in field:
        minimum = field["minLength"]

    if maximum < minimum:
        proc = _fail(AbsentValue("Incorrect maxLenght or minLenght"))
    else:
        proc = _generate

    while True:
        yield proc()


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
        r = {}
        # TODO: human names
        for k, g in prop_builder:
            next_value = next(g)
            r[k] = next_value
        yield r


def _get_int_processor(minimum: int, maximum: int, multiple_of: int) -> callable:
    def _fail(element):
        return lambda: element

    def _generate_simple(min_val, max_val):
        return lambda: random.randint(min_val, max_val)

    def _generate_multiple_of(min_val, max_val, multiple):
        def _gen():
            r = random.randint(0, m-1)
            return m_init + r * multiple

        m_s = max_val // multiple
        m_i = min_val // multiple
        m = m_s - m_i
        if m <= 0:
            return _fail(AbsentValue("No multiple exists within the requested range"))
        m_init = multiple + ((m_s - m) * multiple)
        return _gen

    if maximum < minimum:
        return _fail(AbsentValue("Invalid Maximum or Minimum"))
    elif multiple_of:
        return _generate_multiple_of(minimum, maximum, multiple_of)
    else:
        return _generate_simple(minimum, maximum)


def _open_api_int(field: dict, strategies):
    def _get_params(field: dict) -> (int, int, int):
        minimum = -sys.maxsize - 1
        maximum = sys.maxsize
        if "minimum" in field:
            minimum = field["minimum"]
        if "maximum" in field:
            maximum = field["maximum"]
        if "exclusiveMinimum" in field:
            minimum = minimum + 1
        if "exclusiveMaximum" in field:
            maximum = maximum - 1

        if "multipleOf" in field:
            multiple_of = field["multipleOf"]
        else:
            multiple_of = None

        return minimum, maximum, multiple_of

    proc = _get_int_processor(*_get_params(field))

    while True:
        yield proc()


def _open_api_list(field: dict, strategies):
    def _must_unique(gen):
        for _ in range(1000):
            r = gen()
            if len(r) == len(set(r)):
                return r
        raise ValueError("Cannot generate unique list with this parameters")
    minimum = 1
    if "minItems" in field:
        minimum = field["minItems"]
    maximum = minimum + 9
    if "maxItems" in field:
        maximum = field["maxItems"]
    item_type = field["items"]
    item_gen = generator(item_type, strategies)

    def gen(size: int):
        return [next(item_gen) for _ in range(size)]

    while True:
        size = random.randint(minimum, maximum)
        if "uniqueItems" in field and field["uniqueItems"]:
            yield _must_unique(gen(size))
        yield gen(size)


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
