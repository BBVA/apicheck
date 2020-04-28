import json
import os
import select
import sys

import requests
import argparse
import jsonschema

from urllib.parse import urlparse
from dataclasses import dataclass

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
    headers: dict = None

    @classmethod
    def from_json(cls, json_data: str) -> object or InvalidJsonFormat:
        # Load json data
        try:
            loaded_json = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise InvalidJsonFormat("Input value doesn't has valid JSON")

        # Check json format
        try:
            # Load json-schema for validation
            with open(os.path.join(os.path.dirname(__file__),
                                   "json-schema.json"), "r") as f:
                json_schema = json.load(f)

            jsonschema.validate(loaded_json, schema=json_schema)
        except jsonschema.ValidationError as e:
            raise InvalidJsonFormat(
                f"JSON data doesn't have correct format: {e}"
            )
        except Exception as e:
            raise UnknownException(e)

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


def send_one_input_data(input_data, args: argparse.Namespace):
    #
    # Load json request
    #
    print("[*] Validating JSON format", file=sys.stderr)
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

    print("[*] Sending request to proxy", file=sys.stderr)
    response = method(**params)

    return response


def run(args: argparse.Namespace):
    # -------------------------------------------------------------------------
    # Read info by stdin or parameter
    # -------------------------------------------------------------------------
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:

        #
        # APICheck input JSON format line by line. The JSON will be one per
        # line
        #
        for content in sys.stdin.readlines():

            response = send_one_input_data(content, args)

            if not args.QUIET_MODE:
                print(
                    json.dumps({
                        "source": "sendtoproxy",
                        "outputStatus": 0,
                        "outputMessage": response.content.decode("UTF-8")
                    }),
                    file=sys.stdout
                )

    else:
        raise FileNotFoundError("Input data must be entered as a UNIX "
                                "pipeline")


def main():
    parser = argparse.ArgumentParser(
        description='Read requests from stdin and send them to a remote proxy'
    )
    parser.add_argument("PROXY", help="proxy in format: SCHEME://HOST:PORT")
    parser.add_argument("-q", "--quiet",
                        dest="QUIET_MODE",
                        help="don't display any information in stdout",
                        action="store_true",
                        default=False)
    parsed_cli = parser.parse_args()

    try:
        run(parsed_cli)
    except Exception as e:
        print(
            json.dumps({
                "source": "sendtoproxy",
                "outputStatus": 1,
                "outputMessage": str(e)
            }),
            file=sys.stdout
        )
        exit(1)


if __name__ == '__main__':
    main()
