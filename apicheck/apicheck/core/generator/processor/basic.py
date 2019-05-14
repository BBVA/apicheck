from typing import *
import random

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


def int_processor(
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
            return fail(
                AbsentValue("No multiple exists within the requested range")
            )
        m_init = multiple + ((m_s - m) * multiple)
        return _gen

    if maximum < minimum:
        return fail(AbsentValue("Invalid Maximum or Minimum"))
    elif multiple_of:
        return _generate_multiple_of(minimum, maximum, multiple_of)
    else:
        return _generate_simple(minimum, maximum)

