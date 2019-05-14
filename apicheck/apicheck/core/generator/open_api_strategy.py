from itertools import repeat
import random
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, TypeVar, Union

from . import AbsentValue, Definition, Properties, _type_matcher, generator

import apicheck.core.generator.metadata.openapi3 as m
import apicheck.core.generator.processor as p


Strategy = Tuple[Callable[[Dict], bool], Callable[[Dict], Any]]

X = TypeVar('X')
MaybeValue = Union[X, AbsentValue]
MaybeCallable = Callable[[], MaybeValue[X]]
AsDefined = Dict[str, Any]


def _open_api_str(
        definition: Definition,
        _: List[Strategy]
        ) -> Iterator[MaybeValue[str]]:
    """
    Yields a string of fake text with a length between 10 and 200, or between
    definition["minLength"] and definition["maxLength"] if those are defined.

    :param definition: specification of a definition
    """
    proc = p.str_processor(*m.str_extractor(definition))

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
        return p.fail(
            AbsentValue("Can't gen a property-less object without policy")
        )
    return _object_gen_proc(properties)


def _open_api_object(
        definition: Definition,
        strategies: List[Strategy]
        ) -> Iterator[MaybeValue[AsDefined]]:
    proc = _object_processor(m.properties_extractor(definition), strategies)
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
            return p.fail(
                AbsentValue("No multiple exists within the requested range")
            )
        m_init = multiple + ((m_s - m) * multiple)
        return _gen

    if maximum < minimum:
        return p.fail(AbsentValue("Invalid Maximum or Minimum"))
    elif multiple_of:
        return _generate_multiple_of(minimum, maximum, multiple_of)
    else:
        return _generate_simple(minimum, maximum)


def _open_api_int(definition: Definition, _: List[Strategy]):
    proc = _get_int_processor(*m.int_extractor(definition))

    while True:
        yield proc()


def _get_list_processor(
        strategies: List[Strategy],
        element_definition: Definition,
        minimum: int,
        maximum: int,
        must_be_unique: bool
        ) -> MaybeCallable[List[Any]]:
    def _must_be_unique() -> MaybeValue[List[Any]]:
        raise NotImplementedError()

    def gen() -> MaybeValue[List[Any]]:
        size = random.randint(minimum, maximum)
        item_gen = generator(element_definition, strategies)
        return [next(item_gen) for _ in range(size)]

    if must_be_unique:
        return _must_be_unique
    else:
        return gen


def _open_api_list(definition: Definition, strategies: List[Strategy]):
    proc = _get_list_processor(strategies, *m.list_extractor(definition))
    while True:
        yield proc()


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
