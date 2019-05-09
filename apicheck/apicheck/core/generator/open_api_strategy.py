from itertools import repeat
import random
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, TypeVar, Union

from faker import Faker

from . import AbsentValue, Definition, Properties, _type_matcher, generator

import apicheck.core.generator.metadata.openapi3 as m

fake = Faker()


Strategy = Tuple[Callable[[Dict], bool], Callable[[Dict], Any]]

X = TypeVar('X')
MaybeValue = Union[X, AbsentValue]
MaybeCallable = Callable[[], MaybeValue[X]]
AsDefined = Dict[str, Any]


def _fail(element: AbsentValue) -> MaybeCallable[X]:
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
    def _str_processor(minimum: int, maximum: int) -> MaybeCallable[str]:
        def _generate() -> MaybeValue[str]:
            r = fake.text()
            while len(r) < minimum:
                r = r + r
            if len(r) > maximum:
                r = r[:maximum-1]
            return r

        if maximum < minimum:
            return _fail(AbsentValue("Incorrect maxLength or minLength"))
        return _generate

    proc = _str_processor(*m.str_extractor(definition))

    while True:
        yield proc()


def _object_processor(
        properties: Optional[Properties],
        strategies: List[Strategy]
        ) -> MaybeCallable[AsDefined]:
    def _object_gen_proc(properties: Properties) -> MaybeCallable[AsDefined]:
        def _proc() -> AsDefined:
            return {
                name: next(generator)
                for name, generator
                in property_builder
            }

        property_builder = [
            (name, generator(definition, strategies))
            for name, definition
            in properties.items()
        ]
        return _proc

    if not properties:
        return _fail(
            AbsentValue("Can't gen a property-less object without policy")
        )
    return _object_gen_proc(properties)


def _open_api_object(
        definition: Definition,
        strategies: List[Strategy]
        ) -> Iterator[MaybeValue[AsDefined]]:
    def _get_properties(definition: Definition) -> Optional[Properties]:
        if "properties" in definition:
            return definition["properties"]
        return None

    proc = _object_processor(_get_properties(definition), strategies)
    while True:
        yield proc()


def _get_int_processor(
        minimum: int,
        maximum: int,
        multiple_of: int
        ) -> MaybeCallable[int]:
    def _generate_simple(min_val: int, max_val: int) -> Callable[[], int]:
        return lambda: random.randint(min_val, max_val)

    def _generate_multiple_of(
            min_val: int,
            max_val: int,
            multiple: int
            ) -> MaybeCallable[int]:
        def _gen() -> int:
            r = random.randint(0, m-1)
            return m_init + r * multiple

        m_s = max_val // multiple
        m_i = min_val // multiple
        m = m_s - m_i
        if m <= 0:
            return _fail(
                AbsentValue("No multiple exists within the requested range")
            )
        m_init = multiple + ((m_s - m) * multiple)
        return _gen

    if maximum < minimum:
        return _fail(AbsentValue("Invalid Maximum or Minimum"))
    elif multiple_of:
        return _generate_multiple_of(minimum, maximum, multiple_of)
    else:
        return _generate_simple(minimum, maximum)


def _open_api_int(definition: Definition, _: List[Strategy]):
    proc = _get_int_processor(*m.int_extractor(definition))

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
            yield _must_be_unique(gen(size))
        yield gen(size)


def _open_api_bool(_: Definition, __: List[Strategy]):
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
