
def generator(field: dict, strategies, key=None):
    for matcher, fun in strategies:
        if matcher(key, field):
            return fun(field, strategies)
    # TODO: use own error
    raise ValueError(f"No strategy found for {field}")


def _type_matcher(expected):
    def _match(key, item):
        if "type" in item:
            return item["type"] == expected
        return False
    return _match
