from urllib.parse import urlparse
from string import ascii_letters, digits
from random import randint, random, choice

from ..core.helpers import find_data_type


class FUZZSelector(object):
    URL = 1
    BODY = 10
    COOKIE = 100
    HEADER = 1000
    METHOD = 10000
    
    def __init__(self, bitwise):
        if not bitwise:
            raise ValueError("Invalid bits in selectors")
        
        self._bitwise = "{:05}".format(bitwise)
        
        if len(self._bitwise) != 5:
            raise ValueError("Invalid values for bitwise value. Length is not 5")
    
    @property
    def is_url(self):
        return bool(int(self._bitwise[-1]))
    
    @property
    def is_body(self):
        return bool(int(self._bitwise[-2]))
    
    @property
    def is_cookie(self):
        return bool(int(self._bitwise[-3]))
    
    @property
    def is_header(self):
        return bool(int(self._bitwise[-4]))
    
    @property
    def is_method(self):
        return bool(int(self._bitwise[-5]))
    

def build_fuzzed_url(url: str, *, exclude_params: list = None,  encode: bool = False) -> str:
    """
    Get the parameters of an URL and fuzz them.
     
    URL types:
        1.
            + www.xxxx.com/api/users/hello
        2.
            + www.xxxx.com/api/users/hello?param1=value1&param2=value2
            + www.xxxx.com/api/users/hello/?param1=value1&param2=value2
            + www.xxxx.com/api/users/hello.php?param1=value1&param2=value2
    
    >>> build_fuzzed_url("http://example.com/api/users?country=es&name=John&lang=en&user=john_doc&password=1234")
    http://example.com/api/users?country=JBB5HiNqLY&name=False&lang=False&user=GUTU3ucZ0H2c9mPbOjE&password=19383874
    
    :param url: a valid URL
    :type url: str
    
    :param exclude_params: exclude these params from list to fuzz
    :type exclude_params: list(str)
    
    :param encode:
    :type encode:
    :return:
    :rtype:
    """
    if not url:
        return ""
    
    exclude_params = exclude_params or []
    
    scheme, host, path, _, query, fragment = urlparse(url)
    
    if query:
        query_params = dict([tuple(elem.split("=", maxsplit=1)) for elem in query.split("&")])
        
        fuzzed_params = "&".join("%s=%s" % (key, fuzz_value_from_type(value))
                                 for key, value in query_params.items() if key not in exclude_params)
    else:
        fuzzed_params = ""
    
    return "{scheme}://{host}{path}{query}".format_map(dict(scheme=scheme,
                                                            host=host,
                                                            path=path,
                                                            query="?%s" % fuzzed_params if fuzzed_params else ""))


def build_fuzzed_x_form(data: str, *, exclude_params: list = None, encode: bool = False) -> str:
    """
    >>> build_fuzzed_x_form("name=John&user=1&password=False")
    name=XjPqv9sEbG&user=774752&password=True
    
    :param data: Input data as string
    :type data: str
    
    :param exclude_params: exclude these params from list to fuzz
    :type exclude_params: list(str)
    
    :param encode: URL encode the data result (NOT IMPLEMENTED YET)
    :type encode: bool
    
    :return: string with the implementation
    :rtype: str
    """
    
    if not data:
        return ""
    exclude_params = exclude_params or []
    input_data = dict([tuple(elem.split("=", maxsplit=1)) for elem in data.split("&")])
    
    return "&".join("%s=%s" % (key,fuzz_value_from_type(value))
                    for key, value in input_data.items() if key not in exclude_params)


def build_fuzzed_json(data: dict, *, exclude_params: list = None, encode : bool = False) -> dict:  # TODO: Improve algorithm
    """
    :param data: Input JSON data as dict format
    :type data: dict
    
    :param exclude_params: exclude these params from list to fuzz
    :type exclude_params: list(str)
    
    :param encode: URL encode the data result (NOT IMPLEMENTED YET)
    :type encode: bool
    
    :return: string with the implementation
    :rtype: str
    """
    exclude_params = exclude_params or []
    
    def recursive_build_fuzzed_json(data):
        if not data:
            return data
        
        if isinstance(data, list):
            results = []
            for d in data:
                results.append(recursive_build_fuzzed_json(d))
        else:
            results = {}
            
            for key, value in data.items():
                if isinstance(value, list):
                    results[key] = recursive_build_fuzzed_json(value)
                else:
                    if key not in exclude_params:
                        value = fuzz_value_from_type(value)
                    results[key] = value
        
        return results
    
    return recursive_build_fuzzed_json(data)


def build_fuzzed_http_header(data: dict, *, exclude_params: list = None, encode: bool = False) -> dict:
    """
    >>> headers = {"Content-Type": dump_json, "Ldump_jsonage": "en;es-ES"}
    >>> build_fuzzed_http_header()
    {"Content-Type": "vnS", "Language": "OUDypzPBBA5WvG1ZTGK"}

    :param data: data header as dict
    :type data: dict(str: str)

    :param exclude_params: exclude these params from list to fuzz
    :type exclude_params: list(str)

    :param encode: URL encode the data result (NOT IMPLEMENTED YET)
    :type encode: bool

    :return: dict with fuzzed params
    :rtype: dict(str: str)
    """
    assert data is not None

    exclude_params = exclude_params or []
    
    return {key: fuzz_value_from_type(value)
            for key, value in data.items() if key not in exclude_params}


def fuzz_value_from_type(param: object):
    # 1 - Get type
    actions = {
        "str": lambda: "".join(choice(ascii_letters + digits) for _ in range(randint(2, 20))),
        "int": lambda: randint(0, 999999),
        "float": lambda: random() * (10 * randint(1, 100)),
        "bool": lambda: choice((True, False))
    }
    
    # 2 - Build random data depending of type
    return actions[find_data_type(param)]()


def build_fuzzed_method(*, allow_invalid_methods=False) -> str:
    """
    Get a random HTTP method
    
    :param allow_invalid_methods: is setted to True, return a random value as method
    :type allow_invalid_methods: str
    
    :return: a string with as a method
    :rtype: str
    """
    if allow_invalid_methods:
        return fuzz_value_from_type("").upper()
    
    http_methods = ("GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "PATH", "CONNECT")
    
    return choice(http_methods)


__all__ = ("build_fuzzed_url", "build_fuzzed_http_header", "build_fuzzed_json", "build_fuzzed_x_form",
           "FUZZSelector", "build_fuzzed_method")
