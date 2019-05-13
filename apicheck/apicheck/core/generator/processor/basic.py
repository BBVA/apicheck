from typing import *

from apicheck.core.generator import AbsentValue

X = TypeVar('X')
MaybeValue = Union[X, AbsentValue]
MaybeCallable = Callable[[], MaybeValue[X]]
AsDefined = Dict[str, Any]


def fail(element: AbsentValue) -> MaybeCallable[X]:
    return lambda: element
