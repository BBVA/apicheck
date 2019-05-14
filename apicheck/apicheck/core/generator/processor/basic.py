from typing import *

from faker import Faker

from apicheck.core.generator import AbsentValue

X = TypeVar('X')
MaybeValue = Union[X, AbsentValue]
MaybeCallable = Callable[[], MaybeValue[X]]
AsDefined = Dict[str, Any]


def fail(element: AbsentValue) -> MaybeCallable[X]:
    return lambda: element


fake = Faker()


def str_processor(minimum: int, maximum: int) -> MaybeCallable[str]:
    def _generate() -> MaybeValue[str]:
        r = fake.text()
        while len(r) < minimum:
            r = r + r
        if len(r) > maximum:
            r = r[:maximum-1]
        return r

    if maximum < minimum:
        return fail(AbsentValue("Incorrect maxLength or minLength"))
    return _generate
