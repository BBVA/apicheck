from apicheck.core.dict_helpers import search

from typing import Callable, List, Any
import sys
import random

from faker import Faker


fake = Faker()


def open_api_str(field: dict, strategies):
    minimum = 10
    maximum = 200
    if "maxLength" in field:
        maximum = field["maxLength"]
    if "minLength" in field:
        minimum = field["minLength"]
    while True:
        r = fake.text()
        while len(r) < minimum:
            r = r + r
        if len(r) > maximum:
            r = r[:maximum-1]
        yield r


def open_api_object(field: dict, strategies):
    def _make_gen(v):
        return generator(v, strategies)
    properties = field["properties"]
    keys = properties.keys()
    generators = list(map(_make_gen, properties.values()))
    prop_builder = list(zip(keys, generators))
    while True:
        yield {
            k: next(g)
            for k, g in prop_builder
        }


def open_api_int(field: dict, strategies):
    minimum = -sys.maxsize-1
    maximum = sys.maxsize
    if "minimum" in field:
        minimum = field["minimum"]
    if "maximum" in field:
        maximum = field["maximum"]
    if "exclusiveMinimum" in field:
        minimum = minimum+1
    if "exclusiveMaximum" in field:
        maximum = maximum-1
    while True:
        r = random.randint(minimum, maximum)
        if "multipleOf" in field:
            rem = r % field["multipleOf"]
            r = r - rem
        yield r


def open_api_list(field: dict, strategies):
    def _must_unique(gen):
        for _ in range(1000):
            res = gen()
            if len(res) == len(set(res)):
                return res
        raise ValueError("Cannot generate unique list with this parameters")
    minimum = 1
    if "minItems" in field:
        minimum = field["minItems"]
    maximum = minimum + 9
    if "maxItems" in field:
        maximum = field["maxItems"]
    item_type = field["items"]
    item_gen = generator(item_type, open_api_strategies)
    size = random.randint(minimum, maximum)
    gen = lambda: [next(item_gen) for _ in range(size)]
    while True:
        if "uniqueItems" in field and field["uniqueItems"]:
            yield _must_unique(gen())
        yield gen()


def open_api_bool(field: dict, strategies):
    while True:
        n = random.randint(1, 10)
        yield n % 2 == 0


def dict_generator(words_dict):
    def _generator(field: dict, strategies):
        for n in words_dict:
            yield n
    return _generator


def type_matcher(expected):
    def _match(x):
        return x["type"] == expected
    return _match


open_api_strategies = [
    (type_matcher("string"), open_api_str),
    (type_matcher("integer"), open_api_int),
    (type_matcher("object"), open_api_object),
    (type_matcher("array"), open_api_list),
    (type_matcher("boolean"), open_api_bool)
]


def generator(field: dict, strategies):
    for matcher, fun in strategies:
        if matcher(field):
            return fun(field, strategies)
    return lambda: None


def test_string_field():
    field = {
        "type": "string",
        "example": "fieldname"
    }

    gen = generator(field, open_api_strategies)

    res = next(gen)

    assert isinstance(res, str)
    assert res != ""

    res2 = next(gen)

    assert isinstance(res2, str)
    assert res2 != ""

    assert res != res2


def test_string_boundaries():
    field = {
        "type": "string",
        "minLength": 2,
        "maxLength": 10,
        "example": "fieldname"
    }

    gen = generator(field, open_api_strategies)

    for _ in range(1000):
        res = next(gen)
        assert len(res) >= 2
        assert len(res) <= 10


def test_integer_field():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "example": 123
    }

    gen = generator(field, open_api_strategies)

    res = next(gen)

    assert isinstance(res, int)

    res2 = next(gen)

    assert isinstance(res, int)

    assert res != res2


def test_integer_boundaries():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "minimum": 0,
        "maximum": 10,
        "example": 123
    }

    gen = generator(field, open_api_strategies)
    for _ in range(1000):
        res = next(gen)
        assert res >= 0
        assert res <= 10


def test_integer_exclusive_boundaries():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "minimum": 0,
        "maximum": 10,
        "exclusiveMinimum": True,
        "exclusiveMaximum": True,
        "example": 123
    }

    gen = generator(field, open_api_strategies)
    for _ in range(1000):
        res = next(gen)
        assert res > 0
        assert res < 10


def test_integer_multiple_of():
    field = {
        "type": "integer",
        "description": "This authorization's ID, used for revoking access.\n",
        "multipleOf": 10,
        "example": 123
    }

    gen = generator(field, open_api_strategies)
    for _ in range(1000):
        res = next(gen)
        assert res % 10 == 0


def test_array_field():
    field = {
        "type": "array",
        "items": {
            "type": "integer",
            "example": 123
        }
    }

    gen = generator(field, open_api_strategies)

    res = next(gen)

    assert isinstance(res, List)
    assert len(res) <= 10

    res2 = next(gen)

    assert isinstance(res2, List)
    assert len(res2) <= 10

    assert res != res2


def test_array_boundaries():
    field = {
        "type": "array",
        "maxItems": 9,
        "minItems": 2,
        "items": {
            "type": "integer",
            "example": 123
        }
    }

    gen = generator(field, open_api_strategies)

    for _ in range(1000):
        res = next(gen)
        assert isinstance(res, List)
        assert len(res) <= 9
        assert len(res) >= 2


def test_array_unique():
    field = {
        "type": "array",
        "uniqueItems": True,
        "minItems": 10,
        "items": {
            "type": "integer",
            "minimum": 1,
            "maximum": 40,
            "example": 123
        }
    }

    gen = generator(field, open_api_strategies)

    for _ in range(1000):
        try:
            res = next(gen)
            assert isinstance(res, List)
            len(res) == len(set(res))
            break
        except:
            pass


def test_object_field():
    field = {
        "type": "object",
        "description": "An object for describing a "
        "single error that occurred "
        "during the processing of a "
        "request.\n",
        "properties": {
            "reason": {
                "type": "string",
                "description": "What happened to "
                "cause this error. In "
                "most cases, this can "
                "be fixed immediately "
                "by changing the data "
                "you sent in the "
                "request, but in some "
                "cases you will be "
                "instructed to [open "
                "a Support Ticket]("
                "#operation/createTicket) or perform some other action before you can complete the request successfully.\n",
                "example": "fieldname must be a "
                "valid value"
            }
        }
    }

    gen = generator(field, open_api_strategies)

    res = next(gen)

    assert isinstance(res, dict)
    assert len(res.keys()) > 0
    assert "reason" in res

    value = res["reason"]

    assert isinstance(value, str)


def test_compund_item():
    compound_item = {
        "type": "object",
        "properties": {
                "errors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "description": "An object for describing a "
                        "single error that occurred "
                        "during the processing of a "
                        "request.\n",
                        "properties": {
                            "reason": {
                                "type": "string",
                                "description": "What happened to "
                                "cause this error. In "
                                "most cases, this can "
                                "be fixed immediately "
                                "by changing the data "
                                "you sent in the "
                                "request, but in some "
                                "cases you will be "
                                "instructed to [open "
                                "a Support Ticket]("
                                "#operation/createTicket) or perform some other action before you can complete the request successfully.\n",
                                "example": "fieldname must be a "
                                "valid value"
                            },
                            "field": {
                                "type": "string",
                                "description": "The field in the "
                                "request that caused "
                                "this error. This may "
                                "be a path, separated "
                                "by periods in the "
                                "case of nested "
                                "fields. In some "
                                "cases this may come "
                                "back as \"null\" if "
                                "the error is not "
                                "specific to any "
                                "single element of "
                                "the request.\n",
                                "example": "fieldname"
                            }
                        }
                    }
                }
        }
    }

    gen = generator(compound_item, open_api_strategies)

    res = next(gen)

    assert isinstance(res, dict)
    assert "errors" in res

    error_list = res["errors"]
    assert isinstance(error_list, List)
    assert len(error_list) <= 10

    for item in error_list:
        assert "reason" in item
        assert isinstance(item["reason"], str)
        assert "field" in item
        assert isinstance(item["field"], str)


def test_boolean_field():
    field = {
        "type": "boolean"
    }

    gen = generator(field, open_api_strategies)

    res = next(gen)

    assert isinstance(res, bool)

    res2 = [next(gen) for _ in range(1000)]
    assert any(res2)
    not_res2 = [not x for x in res2]
    assert any(not_res2)


def test_wordlist_generator():
    field = {
        "type": "string"
    }

    words = [
        "A", "B", "C"
    ]

    strategy = [
        (type_matcher("string"), dict_generator(words))
    ]

    gen = generator(field, strategy)

    res = list(gen)

    assert isinstance(res, List)
    assert res[0] == "A"
    assert res[1] == "B"
    assert res[2] == "C"