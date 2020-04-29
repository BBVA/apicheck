import os

import gurl


HERE = os.path.dirname(__file__)


def test_empty():
    res = gurl.parse_curl_trace(None)

    assert res is None


def test_google():
    with open(os.path.join(HERE, "tracefiles", "google"), "rb") as f:
        res = gurl.parse_curl_trace(f)
        print(res)
        assert False