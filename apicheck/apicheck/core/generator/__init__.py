from itertools import repeat


class AbsentValue(object):
    def __init__(self, reason):
        self.reason = reason


def generator(field: dict, strategies):
    if not field:
        return repeat(AbsentValue("no field provided on generator"))
    if not strategies:
        return repeat(AbsentValue("no strategies provided on generator"))
    for matcher, fun in strategies:
        if matcher(field):
            return fun(field, strategies)
    return repeat(AbsentValue("no strategy found"))


def _type_matcher(expected):
    def _match(item):
        if "type" in item:
            return item["type"] == expected
        return False
    return _match
