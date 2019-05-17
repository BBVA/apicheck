from urllib.parse import urlparse


def _compare_paths(a, b):
    def _count_equals(i):
        if a[i] == b[i]:
            return 1
        return 0
    return sum(map(_count_equals, range(min(len(a), len(b)))))


def find_endpoint(rules, url):
    if not rules or not url or len(rules) == 0:
        return None
    parsed = urlparse(url)

    most = 0
    most_path = None
    for url in rules:
        current = _compare_paths(url.split("/"), parsed.path.split("/"))
        if current > most:
            most_path = url
    return most_path
