from typing import Optional, Tuple
import sys

from apicheck.core.generator import Definition, Properties


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


def properties_extractor(definition: Definition) -> Optional[Properties]:
    if "properties" in definition:
        return definition["properties"]
    return None


def list_extractor(
        definition: Definition
        ) -> Tuple[Definition, int, int, bool]:
    minimum = 1
    if "minItems" in definition:
        minimum = definition["minItems"]
    maximum = minimum + 9
    if "maxItems" in definition:
        maximum = definition["maxItems"]
    items_must_be_unique = "uniqueItems" in definition and definition["uniqueItems"]
    return definition["items"], minimum, maximum, items_must_be_unique
