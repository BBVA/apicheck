"""
This file contains utils and reusable functions
"""

import string
import logging

from os import listdir
from hashlib import sha1
from os.path import join, exists
from contextlib import contextmanager
from collections import namedtuple, OrderedDict

from .exceptions import ApitestUnknownTypeError, ApitestNotFoundError


log = logging.getLogger("apitest")


def dict_to_obj(data):
    """
    Transform an input dict into a object.

    >>> data = dict(hello="world", bye="see you")
    >>> obj = dict_to_obj(data)
    >>> obj.hello
    'world'

    :param data: input dictionary data
    :type data: dict
    """
    assert isinstance(data, dict)

    if not data:
        return namedtuple("OBJ", [])

    obj = namedtuple("OBJ", list(data.keys()))

    return obj(**data)


def make_directoriable(name: str) -> str:
    """
    Convert any name in a valid directory / file name

    >>> make_directoriable("Hello World guy!")
    "hello_world_guy"

    :param name: name to convert
    :type name: str

    :return: converted name
    :rtype: str
    """
    if not name:
        return ""

    valid_chars = string.ascii_letters + "_-/ " + string.digits

    _tmp_path = "".join(x.lower().replace(" ", "_").replace("-", "_").replace("/", "_") for x in name if x in valid_chars)

    if _tmp_path.startswith("_"):
        _tmp_path = _tmp_path[1:]
    if _tmp_path.endswith("_"):
        _tmp_path = _tmp_path[:-1]

    return _tmp_path


def find_files_by_extension(base_dir: str, *, extensions: iter = None):
    """
    Find in a directory for files by extensions.

    It return the ABSOLUTE PATH.

    >>> find_files_by_extension("/etc", extensions=("cfg", "config"))
    ["/etc/auth.config", "/etc/dns.cfg"]

    :param base_dir: dir where looking files
    :type base_dir: str

    :param extensions: file extensions to search
    :type extensions: list(str)

    :return: generator with templates
    :rtype: generator(str)

    :raise ApitestNotFoundError: if base dir not found
    :raise AssertionError: If base dir is not a string
    """
    assert isinstance(base_dir, str)

    extensions = extensions or ("jinja.py", "jinja2.py")

    if not exists(base_dir):
        raise ApitestNotFoundError("Base dir '{}' not found".format(base_dir))

    for file in listdir(base_dir):
        if not file.startswith("_") and any(True for x in extensions if file.endswith(x)):
            yield join(base_dir, file)


def find_data_type(data: object) -> str:
    """
    Try to find the type of data object. Valid returned values are:

    - "str"
    - "int"
    - "float"
    - "bool"
    - "list"
    - "dict"

    If we can't determinate the type, exception 'ApitestUnknownTypeError' is raised.

    :param data: object to determinate de data type
    :type data: object

    :return: and string with the name of data type
    :rtype: str

    :raises ApitestUnknownTypeError: when can't determinate the data type
    """
    if str(data) in ("True", "False"):
        return "bool"

    # Type: FLOAT
    try:
        if float(data) == data:
            if str(float(data)) == str(data):
                return "float"
    except (ValueError, TypeError):
        pass

    # Type: INT
    try:
        if int(data) == data:
            return "int"
    except (ValueError, TypeError):
        pass

    # Type: LIST
    try:
        if list(data) == data:
            return "list"
    except TypeError:
        pass

    # Type: DICT
    try:
        if dict(data) == data:
            return "dict"
    except (ValueError, TypeError):
        pass

    # Type: STR
    if type(data) == type(str(data)):
        return "str"

    # If this point is reach, type is not detected... then raises exception
    raise ApitestUnknownTypeError("Can't determinate the data type of '{}'".format(data))


def make_url_signature(url: str, *, method: str = "GET", headers: dict = None, body: str = None) -> str:
    """
    From a URL values, make a unique and replicable signature, returning string with the signature.

    :return: the signature value
    :rtype: str
    """
    #
    # For build the signature, the algorithm use:
    #   - URL
    #   - Headers fields names
    #   - body content
    #   - method
    headers = headers or {}
    body = body or ""

    # Re-order body to guarantee the same order all times
    if "application/json" in headers.values():
        body = body  # TODO: implement JSON in body
    else:
        if body:
            ordered_body = form_content2dict(body)

            body = "&".join(["%s=%s" % (key, value)for key, value in ordered_body.items()])

    pre_signature = "{url}#{method}#{headers}#{body}".format_map(dict(
        url=url,
        method=method,
        headers="#".join(OrderedDict(sorted(headers.items())).keys()),
        body=body))

    return sha1(pre_signature.encode()).hexdigest()


# --------------------------------------------------------------------------
# Helpers functions
# --------------------------------------------------------------------------
def form_content2dict(form_data: str) -> dict:
    """
    Transform an input raw form-form_data into a dict

    >>> body = "user=john&password=1234"
    >>> form_content2dict(form_data)
    {"user": "john", "password": "1234"}

    :param form_data: body content as string format.
    :type form_data: str

    :return: dictionary transformed
    :rtype: dict(str: str)
    """
    if not form_data:
        return OrderedDict(dict(form_data=""))

    if "&" not in form_data:
        return OrderedDict(dict(form_data=form_data))
    else:
        return OrderedDict(sorted(dict([tuple(elem.split("=", maxsplit=1)) for elem in form_data.split("&")]).items()))


def display_apitest_object_summary(data, *, display_function: object = None, prefix="[*]"):
    """
    Display a summary for an API Test object

    >>> import json
    >>> json_info = json.load("apitest_file.json")
    >>> apitest_info = APITest(**json_info)
    >>> import logging
    >>> log = logging.getLogger("apitest")
    >>> display_apitest_object_summary(apitest_info, display_function=log.debug)
    [*] Summary:
        - Total collections: 6
        - Total end-points: 21
        > DigestAuth Success   -     2 endpoints
        > Hawk Auth            -     3 endpoints
        > Get Cookies          -     3 endpoints
        > Response Headers     -     2 endpoints
        > DELETE Request       -     5 endpoints
        > Deflate Compressed Response -     6 endpoints

    :param data: APITest object instance
    :type data: APITest

    :param display_function: function used to diplay the information
    :type display_function: object

    :param prefix: Prefix used to display in console
    :type prefix: str
    """
    if not display_function:
        display_function = print

    pre_space = " " * len(prefix)

    display_function("{} Summary:".format(prefix))
    display_function("{} - File format is OKs".format(pre_space))
    display_function("{} -  File Summary:".format(pre_space))
    display_function("{}    + Total collections: {}".format(pre_space, len(data.collections)))
    display_function("{}    + Total end-points: {}".format(pre_space, sum(len(x.end_points) for x in data.collections)))

    for col in data.collections:
        display_function("{space}      > {name:{align}} - {endpoint:>5} endpoints".format(space=pre_space,
                                                                                          name=col.name,
                                                                                          align=30,
                                                                                          endpoint=len(col.end_points)))

        for end_point in col.end_points:
            display_function("{space}         |-> [{method}] {name:{align}}".format(method=end_point.request.method,
                                                                                    space=pre_space,
                                                                                    name=end_point.name,
                                                                                    align=40))


@contextmanager
def run_in_console(debug=False):
    try:
        yield
    except Exception as e:
        log.critical(" !! {}".format(e))

        if debug:
            log.critical(e, exc_info=True)
    finally:
        log.debug("Shutdown...")


def get_log_level(verbosity: int) -> int:
    verbosity *= 10

    if verbosity > logging.CRITICAL:
        verbosity = logging.CRITICAL

    if verbosity < logging.DEBUG:
        verbosity = logging.DEBUG

    return (logging.CRITICAL - verbosity) + 10


__all__ = ("dict_to_obj", "make_directoriable", "find_files_by_extension",
           "find_files_by_extension",
           "find_data_type", "form_content2dict",
           "display_apitest_object_summary",
           "run_in_console", "get_log_level")
