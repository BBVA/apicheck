from urllib.parse import urlparse


def find_endpoint(rules, url):
    if not rules or not url or len(rules) == 0:
        return None
    parsed = urlparse(url)
    for url in rules:
        if url == parsed.path:
            return url
    return None
