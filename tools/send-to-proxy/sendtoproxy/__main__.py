import os
import sys
import json
import select

import requests
import argparse

from urllib.parse import urlparse
from dataclasses import dataclass
from python_pipes import read_stdin_lines

# Disable SSL Warnings
requests.packages.urllib3.disable_warnings()


class UnknownException(Exception):
    pass


class InvalidJsonFormat(Exception):
    pass


class InvalidProxyFormat(Exception):
    pass


@dataclass
class Request:

    url: str
    body: str = None
    method: str = "GET"
    version: str = "1.1"
    headers: dict = None

    @classmethod
    def from_json(cls, json_data: str) -> object or InvalidJsonFormat:
        # Load json data
        try:
            loaded_json = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise InvalidJsonFormat("Input value doesn't has valid JSON")

        return cls(**loaded_json["request"])

    # def __str__(self):
    #     return pprint.pprint(self.__dict__)

    def __post_init__(self):
        self.method = self.method.lower()


def parse_proxy(proxy: str) -> str or InvalidProxyFormat:
    """Check proxy format and return the tuple:

    (SCHEME: PROXY_URL)
    """
    proxy_schemes = ("http", "https", "socks")

    scheme, netloc, path, *_ = urlparse(proxy)

    if not scheme:
        raise InvalidProxyFormat(
            f"Proxy must include one of these schemes: "
            f"{','.join(proxy_schemes)}"
        )

    if not any(scheme.startswith(x) for x in proxy_schemes):
        raise InvalidProxyFormat(
            f"Proxy must starts with one of them: {','.join(proxy_schemes)}"
        )

    # check for proxy port
    try:
        host, port = netloc.split(":")
    except ValueError:
        raise InvalidProxyFormat("Proxy must include host and port "
                                 "(HOST:PORT)")

    return scheme, proxy


def send_one_input_data(input_data, args: argparse.Namespace) -> str:
    #
    # Load json request
    #
    req = Request.from_json(input_data)

    # Prepare input proxy
    proxy_scheme, proxy_url = parse_proxy(args.PROXY)
    proxies = {
        "https": proxy_url,
        "http": proxy_url
    }

    #
    # Get request method
    #
    method = getattr(requests, req.method)

    # Perform query
    if req.method == "get":
        params = dict(
            url=req.url,
            headers=req.headers,
            proxies=proxies
        )
    else:
        params = dict(
            url=req.url,
            headers=req.headers,
            data=req.body,
            proxies=proxies
        )

    # Remove SSL Verification
    params["verify"] = False

    response = method(**params)

    return req.url, response


def run(args: argparse.Namespace):
    quiet = args.quiet or False

    # -------------------------------------------------------------------------
    # Read info by stdin or parameter
    # -------------------------------------------------------------------------
    for has_stdin_pipe, has_stdout_pipe, json_line in read_stdin_lines():
        if not has_stdin_pipe:
            raise FileNotFoundError(
                "Input data must be entered as a UNIX pipeline. For example: "
                "'cat info.json | tool-name'")

        print(json_line)
        request_url, response = send_one_input_data(json_line, args)

        if not quiet:
            message = f"[*] Request sent: '{request_url}'"

            if has_stdout_pipe:
                sys.stderr.write(message)
                sys.stderr.flush()

            else:
                # You're being piped or redirected
                sys.stdout.write(json.dumps(json_line))
                sys.stdout.flush()

                sys.stdout.write(message)
                sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(
        description='Read requests from stdin and send them to a remote proxy'
    )
    parser.add_argument("PROXY", help="proxy in format: SCHEME://HOST:PORT")
    parser.add_argument("-q", "--quiet",
                        help="don't display any information in stdout",
                        action="store_true",
                        default=False)
    parsed_cli = parser.parse_args()

    try:
        run(parsed_cli)
    except Exception as e:
        print(f"[!!] {e}", file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
