from typing import Tuple
import sys

from apicheck.core.generator import Definition


def int_extractor(definition: Definition) -> Tuple[int, int, int]:
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


def str_extractor(definition: Definition) -> Tuple[int, int]:
    minimum = 10
    maximum = 200
    if "maxLength" in definition:
        maximum = definition["maxLength"]
    if "minLength" in definition:
        minimum = definition["minLength"]
    return minimum, maximum
