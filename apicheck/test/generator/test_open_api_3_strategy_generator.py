from typing import List

from apicheck.core.generator import generator, AbsentValue
from apicheck.core.generator.open_api_strategy import strategy as open_api_strategies


def test_no_field():
    gen = generator(None, open_api_strategies)

    res = next(gen)

    assert isinstance(res, AbsentValue)


def test_no_strategies():
    field = {
        "type": "string",
        "example": "fieldname"
    }
    gen = generator(field, None)

    res = next(gen)

    assert isinstance(res, AbsentValue)


def test_no_strategy_found():
    field = {
        "type": "strong",
        "example": "waka"
    }
    gen = generator(field, open_api_strategies)

    res = next(gen)

    assert isinstance(res, AbsentValue)



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
        assert len(res) >= field["minLength"]
        assert len(res) <= field["maxLength"]


def test_string_incorrect_boundaries():
    field = {
        "type": "string",
        "minLength": 10,
        "maxLength": 5,
        "example": "fieldname"
    }

    gen = generator(field, open_api_strategies)

    for _ in range(1000):
        res = next(gen)
        assert isinstance(res, AbsentValue)


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