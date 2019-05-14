from itertools import repeat
import random
import sys
from typing import Any, Callable, Dict, Iterator, List, Tuple, TypeVar, Union

from . import AbsentValue, Definition, Properties, _type_matcher, generator

import apicheck.core.generator.metadata.openapi3 as m
import apicheck.core.generator.processor as p


Strategy = Tuple[Callable[[Dict], bool], Callable[[Dict], Any]]

X = TypeVar('X')
MaybeValue = Union[X, AbsentValue]
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


def _open_api_object(
        definition: Definition,
        strategies: List[Strategy]
        ) -> Iterator[MaybeValue[AsDefined]]:
    proc = p.object_processor(m.properties_extractor(definition), strategies)
    while True:
        yield proc()


def _open_api_int(definition: Definition, _: List[Strategy]):
    proc = p.int_processor(*m.int_extractor(definition))

    while True:
        yield proc()


def _open_api_list(definition: Definition, strategies: List[Strategy]):
    proc = p.list_processor(strategies, *m.list_extractor(definition))
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
