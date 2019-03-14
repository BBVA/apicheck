import os
import json
import pytest

from dataclasses import dataclass
from typing import Any, Callable

FAKE_DICT = {
    "put": {
        "x-linode-grant": "read_write",
        "summary": "Update account",
        "description": "blah",
        "operationId": "updateAcount",
        "x-linode-cli-action": "update",
        "juan": {
            "x-linode-grant": "read_write",
            "summary": "Update account"
        }
    }
}

@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


@dataclass
class Pepe:
    x_linode_grant: str
    summary: str


@dataclass
class Put:
    x_linode_grant: str
    summary: str
    description: str
    operationId: str
    x_linode_cli_action: str
    my_pepe: Pepe

class DefModel:
    pass

@dataclass
class ParserMap:
    destination: str
    klass: Callable

@dataclass
class ParserRef:
    destination: str
    klass: DefModel  # Other logic.



# def parse(content, data_dict) -> dict or object:
#
#     ret = {}
#     for key, value in content.items():
#
#         try:
#             rule_result = data_dict[key](value)
#         except KeyError:
#             # We haven't the rule
#             rule_result = {key.replace("-", "_"): value}
#
#         except TypeError:
#             raise TypeError(f"Unmapped '{value}' property on Dataclass "
#                             f"{key.capitalize()}")
#
#         try:
#             ret.update(rule_result)
#         except TypeError as e:
#             # Rule result not a dict. Only root case/class.
#             return rule_result
#
#     return ret

def parse(content, data_dict: dict) -> dict or object:

    ret = {}
    for key, value in content.items():

        try:
            parser_map: ParserMap = data_dict[key]
            parsed = parser_map.klass(**parse(value, data_dict))

            if parser_map.destination:
                rule_result = {parser_map.destination: parsed}
            else:
                return parsed

        except KeyError:
            # We haven't the rule
            rule_result = {key.replace("-", "_"): value}

        except TypeError:
            raise TypeError(f"Unmapped '{value}' property on Dataclass "
                            f"{key.capitalize()}")

        ret.update(rule_result)

    return ret


def test_put():

    # DATA_DICT = {
    #     "put": lambda x: Put(**parse(x, DATA_DICT)),
    #     "juan": lambda x: {"juan": Pepe(**parse(x, DATA_DICT))}
    # }
    DATA_DICT = {
        "put": ParserMap(None, Put),  # Root
        "juan": ParserMap("my_pepe", Pepe),
    }

    c = parse(FAKE_DICT, DATA_DICT)

    assert isinstance(c, Put)
    assert getattr(c, "x_linode_grant") == "read_write"
    assert getattr(c, "summary") == "Update account"

