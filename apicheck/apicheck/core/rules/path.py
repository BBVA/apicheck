from urllib.parse import urlparse, urlunparse

from apicheck.core.generator import generator
from . import rules_strategy


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
    parsed = urlparse(current_path)
    parsed_parts = parsed.path.split("/")
    rule_parts = rule_path.split("/")
    for prop, info in properties.items():
        i = _find_index_in_part(rule_parts, "{"+prop+"}")
        if not i:
            continue
        if isinstance(i, dict):
            gen = generator(info, rules_strategy)
            parsed_parts[i] = str(next(gen))
        else:
            parsed_parts[i] = str(info)
    new_path = "/".join(parsed_parts)

    return urlunparse(parsed._replace(path=new_path))


def _parse_current_path(current):
    parsed = urlparse(current)
    out = {}
    for part in parsed.query.split("&"):
        [k, v] = part.split("=")
        out[k] = v
    return parsed, out


# TODO: replace with gen_properties in body.py
def _generate_new_query(properties):
    out = {}
    for k, v in properties.items():
        if isinstance(v, dict):
            gen = generator(v, rules_strategy)
            out[k] = str(next(gen))
        else:
            out[k] = str(v)
    return out


def _compose_query_string(path):
    parts = [f"{k}={v}" for k, v in path.items()]
    return "&".join(parts)


def merge_queries(current_path, properties):
    parsed = urlparse(current_path)
    parsed_query = parsed.query.split("&")
    out = {}
    for part in parsed_query:
        [key, value] = part.split("=")
        if key in properties:
            spec = properties[key]
            if isinstance(spec, dict):
                gen = generator(spec, rules_strategy)
                out[key] = str(next(gen))
            else:
                out[key] = str(spec)
        else:
            out[key] = value
    parts_joined = [f"{k}={v}" for k, v in out.items()]
    new_query = "&".join(parts_joined)

    return urlunparse(parsed._replace(query=new_query))


def override_query(current_path, properties):
    new_query = _generate_new_query(properties)
    query_str = _compose_query_string(new_query)
    parsed, _ = _parse_current_path(current_path)
    return urlunparse(parsed._replace(query=query_str))
