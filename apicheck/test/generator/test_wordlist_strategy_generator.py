from typing import List

from apicheck.core.generator import generator
from apicheck.core.generator.dict_strategy import dict_generator


def test_wordlist_generator():
    field = {
        "type": "string"
    }

    words = [
        "A", "B", "C"
    ]

    def allways_true(k, v):
        return True

    gen = generator(field, [(allways_true, dict_generator(words))])

    res = list(gen)

    assert isinstance(res, List)
    assert res[0] == "A"
    assert res[1] == "B"
    assert res[2] == "C"