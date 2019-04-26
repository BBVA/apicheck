
def generator(field: dict, strategies):
    for matcher, fun in strategies:
        # TODO: remove key
        if matcher(field):
            return fun(field, strategies)
    # TODO: use own error
    raise ValueError(f"No strategy found for {field}")


def _type_matcher(expected):
    def _match(item):
        if "type" in item:
            return item["type"] == expected
        return False
    return _match
