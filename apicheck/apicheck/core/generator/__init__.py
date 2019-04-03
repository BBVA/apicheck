
def generator(field: dict, strategies):
    for matcher, fun in strategies:
        if matcher(field):
            return fun(field, strategies)
    #TODO: use own error
    raise ValueError(f"No strategy found for {field}")


def _type_matcher(expected):
    def _match(x):
        if "type" in x:
            return x["type"] == expected
        return False
    return _match