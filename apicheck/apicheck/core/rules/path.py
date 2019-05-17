from urllib.parse import urlparse, urlsplit, urlunparse

from apicheck.core.generator import generator
from apicheck.core.generator.open_api_strategy import strategy


default_strategy = strategy


def _compare_paths(a, b):
    def _count_equals(i):
        if a[i] == b[i]:
            return 1
        return 0
    a_len = len(a)
    b_len = len(b)
    if a_len != b_len:
        return 0
    return sum(map(_count_equals, range(a_len)))


def find_endpoint(rules, url):
    if not rules or not url or len(rules) == 0:
        return None
    parsed = urlparse(url)

    most = 0
    most_path = None
    for url in rules:
        current = _compare_paths(url.split("/"), parsed.path.split("/"))
        if current > 0 and current > most:
            most = current
            most_path = url
    return most_path


def _find_index_in_part(parts, item):
    for i, x in enumerate(parts):
        if x == item:
            return i
    return None


def merge_paths(current_path, rule_path, properties):
    parsed = urlsplit(current_path)
    parsed_parts = parsed[2].split("/")
    rule_parts = rule_path.split("/")
    for prop, info in properties.items():
        i = _find_index_in_part(rule_parts, "{"+prop+"}")
        if not i:
            continue
        if isinstance(i, dict):
            gen = generator(info, default_strategy)
            parsed_parts[i] = str(next(gen))
        else:
            parsed_parts[i] = str(info)
    new_path = "/".join(parsed_parts)

    return urlunparse((parsed[0], parsed[1], new_path, parsed[3], parsed[4], None))


