
def generator(field: dict, strategies):
    for matcher, fun in strategies:
        if matcher(field):
            return fun(field, strategies)
    raise TypeError(f"No strategy found for {field}")


def _type_matcher(expected):
    def _match(x):
        return x["type"] == expected
    return _match