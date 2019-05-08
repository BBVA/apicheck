from itertools import repeat
import random
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, TypeVar, Union

from faker import Faker

from . import AbsentValue, _type_matcher, generator

fake = Faker()


Strategy = Tuple[Callable[[Dict], bool], Callable[[Dict], Any]]
Definition = Dict[str, Any]

X = TypeVar('X')
MaybeValue = Union[X, AbsentValue]
AsDefined = Dict[str, Any]


def _fail(element: AbsentValue) -> Callable[[], MaybeValue[X]]:
    return lambda: element


def _open_api_str(
        definition: Definition,
        _: List[Strategy]
        ) -> Iterator[MaybeValue[str]]:
    """
    Yields a string of fake text with a length between 10 and 200, or between
    definition["minLength"] and definition["maxLength"] if those are defined.

    :param definition: specification of a definition
    """
    def _generate() -> MaybeValue[str]:
        r = fake.text()
        while len(r) < minimum:
            r = r + r
        if len(r) > maximum:
            r = r[:maximum-1]
        return r
    minimum = 10
    maximum = 200
    if "maxLength" in definition:
        maximum = definition["maxLength"]
    if "minLength" in definition:
        minimum = definition["minLength"]

    proc = _generate
    if maximum < minimum:
        proc = _fail(AbsentValue("Incorrect maxLength or minLength"))

    while True:
        yield proc()


def _object_processor(properties: Optional[Definition], strategies: List[Strategy]) -> Callable[[], MaybeValue[AsDefined]]:
    def _object_gen_proc(properties: Definition):
        def _proc():
            generated_object = {}
            for property_name, property_generator in property_builder:
                generated_object[property_name] = next(property_generator)
            return generated_object

        property_builder = []
        for property_name, property_def in properties.items():
            property_generator = generator(property_def, strategies)
            property_builder.append((property_name, property_generator))
        return _proc

    if not properties:
        return _fail(
            AbsentValue("Can't gen a property-less object without policy")
        )
    return _object_gen_proc(properties)


def _open_api_object(definition: Definition, strategies: List[Strategy]) -> Iterator[Union[AsDefined, AbsentValue]]:
    def _get_properties(definition: Definition) -> Optional[Definition]:
        if "properties" not in definition:
            return None
        else:
            return definition["properties"]

    proc = _object_processor(_get_properties(definition), strategies)
    while True:
        yield proc()


def _get_int_processor(minimum: int, maximum: int, multiple_of: int) -> Callable[[], Union[int, AbsentValue]]:
    def _generate_simple(min_val: int, max_val: int) -> Callable[[], int]:
        return lambda: random.randint(min_val, max_val)

    def _generate_multiple_of(min_val: int, max_val: int, multiple: int) -> Callable[[], Union[int, AbsentValue]]:
        def _gen() -> int:
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


def _open_api_int(definition: Definition, strategies: List[Strategy]):
    def _get_params(definition: Definition) -> Tuple[int, int, int]:
        minimum = -sys.maxsize - 1
        maximum = sys.maxsize
        if "minimum" in definition:
            minimum = definition["minimum"]
        if "maximum" in definition:
            maximum = definition["maximum"]
        if "exclusiveMinimum" in definition:
            minimum = minimum + 1
        if "exclusiveMaximum" in definition:
            maximum = maximum - 1

        if "multipleOf" in definition:
            multiple_of = definition["multipleOf"]
        else:
            multiple_of = None

        return minimum, maximum, multiple_of

    proc = _get_int_processor(*_get_params(definition))

    while True:
        yield proc()


def _open_api_list(definition: Definition, strategies: List[Strategy]):
    def _must_be_unique(gen: Callable[[], List[Any]]) -> MaybeValue[List[Any]]:
        raise NotImplementedError()
    minimum = 1
    if "minItems" in definition:
        minimum = definition["minItems"]
    maximum = minimum + 9
    if "maxItems" in definition:
        maximum = definition["maxItems"]
    item_type = definition["items"]
    item_gen = generator(item_type, strategies)

    def gen(size: int):
        return [next(item_gen) for _ in range(size)]

    while True:
        size = random.randint(minimum, maximum)
        if "uniqueItems" in definition and definition["uniqueItems"]:
            yield _must_unique(gen(size))
        yield gen(size)


def _open_api_bool(definition: Definition, strategies: List[Strategy]):
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
