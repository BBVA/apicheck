from itertools import repeat
from typing import *


class AbsentValue(object):
    def __init__(self, reason):
        self.reason = reason


Definition = Dict[str, Any]
Properties = Dict[str, Any]

Strategy = Tuple[Callable[[Dict], bool], Callable[[Dict], Any]]

X = TypeVar('X')
MaybeValue = Union[X, AbsentValue]
MaybeCallable = Callable[[], MaybeValue[X]]
AsDefined = Dict[str, Any]


def fail(element: AbsentValue) -> MaybeCallable[X]:
    def _any_case(*args, **kwargs):
        return element
    return _any_case


def generator(field: dict, strategies):
    if not field:
        return repeat(AbsentValue("no field provided on generator"))
    if not strategies:
        return repeat(AbsentValue("no strategies provided on generator"))
    for matcher, fun in strategies:
        if matcher(field):
            return fun(field, strategies)
    return repeat(AbsentValue("no strategy found"))


def _type_matcher(expected):
    def _match(item):
        if "type" in item:
            return item["type"] == expected
        return False
    return _match
