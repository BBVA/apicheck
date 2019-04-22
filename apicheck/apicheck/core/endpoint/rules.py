from apicheck.core.generator import _key_matcher
from apicheck.core.generator.dict_strategy import dict_generator


def rule_finder(rules: dict):
    def finder(path: str, method: str):
        # TODO: * wildcard
        # TODO: ** wildcard
        for url, rule in rules.items():
            if url == path:
                return rule
        return None
    return finder


def _rule_strategy(rule_body):
    rule_type = rule_body["type"]
    if rule_type == "dictionary":
        dictionary = rule_body["values"]
        return dict_generator(dictionary)
    raise NotImplementedError("Can't build rule for ", rule_body)


def make_strategy(rule: dict):
    strategies = []
    for prop, body_r in rule["body"].items():
        curr_strategy = (
            _key_matcher(prop),
            _rule_strategy(body_r)
        )
        strategies.append(curr_strategy)
    # TODO: path strategy
    # TODO: param strategy
    return strategies
