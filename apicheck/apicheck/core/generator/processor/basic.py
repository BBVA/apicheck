from typing import *

from faker import Faker

from apicheck.core.generator import AbsentValue, Properties, generator

Strategy = Tuple[Callable[[Dict], bool], Callable[[Dict], Any]]

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


def object_processor(
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
        return fail(
            AbsentValue("Can't gen a property-less object without policy")
        )
    return _object_gen_proc(properties)

