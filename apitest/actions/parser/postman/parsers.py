"""
This file contains aux function to handle Postman files and data types
"""

import re

from typing import List, Union, Dict

try:
    from ujson import load, loads, dumps
except ImportError:  # pragma no cover
    from json import load, loads, dumps

from apitest import APITest, APITestContentType, APITestHeader, APITestBody, APITestCookie, \
    APITestResponse, APITestEndPoint, APITestRequest, APITestCollection, ApitestValueError, ApitestInvalidFormatError, \
    ApitestMissingDataError


class PostmanConfig:
    def __init__(self, variables: Union[List, dict] = None):
        """
        Extra Postman configuration.

        Variables
        ---------

        This could be passed as a dictionary or a List:

        As a dict
        +++++++++

        >>> vars = {'var1': 'value1', 'var2': 'value2'}
        >>> PostmanConfig(variables=vars)

        As a List
        +++++++++

        >>> vars = ["var1=value1", "var2=value2"]
        >>> PostmanConfig(variables=vars)

        """
        assert isinstance(variables, (dict, list, tuple))

        self.variables = {}

        if isinstance(variables, (list, tuple)):
            for x in variables:
                key, value = x.split("=", maxsplit=1)

                self.variables["{{%s}}" % key] = value

        else:
            for k, v in variables.items():
                # Fix var format
                _fixed_var = k
                if not v.startswith("{{"):
                    _fixed_var = "{{%s" % _fixed_var
                if not v.endswith("}}"):
                    _fixed_var = "%s}}" % _fixed_var

                self.variables[_fixed_var] = v


def from_http_content_type_get_type(headers: list, body_mode: str) -> str:
    """
    Get a valid HTTP Content-Type value from HTTP headers get the data type as a string from Postman Collection

    >>> headers = [APITestHeader(key="Language", value="en")]
    >>> from_http_content_type_get_type(headers=headers, body_mode="formdata")
    'application/www-form-urlencoded'

    :param headers: a list APITestHeader objects
    :type headers: list(APITestHeader)

    :param body_mode: content of 'body.mode' property form parser JSON file
    :type body_mode: str

    :return: HTTP Content type
    :rtype: str
    """
    # Looking for Content-type in headers
    header_content_type = "".join([header.value for header in headers if header.key.lower() == "content-type"])
    if header_content_type:
        return header_content_type

    if body_mode == "formdata":
        return APITestContentType.form.value
    else:
        return APITestContentType.raw.value


def from_raw_body_get_python_object(data_type: str, data: str):
    """
    This functions get a raw body as String format and transform to a Python Object form Postman collection

    With JSON content:

    >>> content = APITestContentType("application/json")
    >>>
    >>> data = from_raw_body_get_python_object(data_type=content, data='[{"user": 1,"password":"hello"}]')
    [{'user': 1, 'password': 'hello'}]
    >>> type(data)
    <class 'list'>

    >>> input_data = [
        {
            "key": "hello",
            "value": "world"
        },
        {
            "key": "hi",
            "value": "you rules!"
        }
    ]

    With a xform content:

    >>> data2 = from_raw_body_get_python_object(data_type=APITestContentType.form, data=input_data)
    "hello=world&hi=you+rules!
    >>> type(data2)
    <class 'str'>

    :param data_type: APITestContentType data object
    :type data_type: APITestContentType

    :param data: a raw body object as string
    :type data: str

    :return: A Python object with the info
    :rtype: object

    :raises: ApitestValueError
    """
    # Check if content type is valid
    try:
        content = APITestContentType(data_type)
    except ValueError:
        return data

    if content == APITestContentType.raw:
        return data
    elif content == APITestContentType.json:
        try:
            if not data:
                return {}

            return loads(data)
        except ValueError as e:
            raise ApitestValueError("Invalid JSON string data")

    elif content == APITestContentType.form:
        try:
            return "&".join("%s=%s" % (item.get("key"), item.get("value").replace(" ", "+")) for item in data)
        except AttributeError:
            raise ApitestValueError("Invalid Form data")


# --------------------------------------------------------------------------
# Handle postman variables
# --------------------------------------------------------------------------
def extract_postman_variables(postman_info: object) -> object:
    """
    This function try to find Postman variables and return a list them.

    Postman collections can have variables. These variables are necessary for build the requests.

    The Postman variable have the format:

    {{variable}}

    :return: a list of Postman variables
    """
    postman_variable_regex = r'''(\{{[\w\d\-\_\.\s]+}})'''

    variables_match = re.findall(postman_variable_regex, dumps(postman_info))

    if not variables_match:
        return []

    # {{ XXX }} -> XXX
    filtered_vars = []
    for match_var in variables_match:
        filtered_vars.append(match_var.replace("{{", "").replace("}}", ""))

    return list(set(filtered_vars))


def replace_postman_variables(postman_info: dict,
                              postman_variables: list,
                              variables_to_replace: List[Dict]) -> \
        Union[dict, ApitestMissingDataError]:

    postman_info_as_text = dumps(postman_info)

    # Check that postman variables and postman config variables has all of
    # required vars
    postman_env_variables = set(postman_variables). \
        difference(set([x for x in variables_to_replace]))

    if postman_env_variables:
        raise ApitestMissingDataError(
            "The Postman collections need some environment variables. Please "
            "specify these variables and try again: '{}'".format(
                ", ".join(postman_env_variables)))

    for postman_var in postman_variables:
        postman_info_as_text = postman_info_as_text.replace(
            "{{%s}}" % postman_var,
            variables_to_replace[postman_var])

    return loads(postman_info_as_text)


# --------------------------------------------------------------------------
# Manage data
# --------------------------------------------------------------------------
def postman_parser(postman_info: dict,
                   environment_vars: Dict = None) -> APITest:
    """
    Get a parser collection, in JSON input format, and parser it

    :param postman_info: JSON parsed info from Postman
    :type postman_info: dict

    :param environment_vars: variables to replace
    :type environment_vars: dict

    :return: a Postman object
    :rtype: APITest

    :raise ApitestValueError: when an invalid Postman format was received
    """
    assert isinstance(postman_info, dict)
    assert len(postman_info) > 0

    # Try to find Postman variables in the JSON info from Postman Project
    variables_from_postman_file = extract_postman_variables(postman_info)

    # If variables was found, replace with the values
    if variables_from_postman_file:
        if not environment_vars:
            raise ApitestMissingDataError(
                "The Postman collections need some environment variables. "
                "Please specify these variables and try again: "
                ",".join(x for x in variables_from_postman_file))
        else:
            postman_info = replace_postman_variables(postman_info,
                                                     variables_from_postman_file,
                                                     environment_vars)

    collections = []

    try:
        # Get all collections
        for collection in postman_info.get("item"):

            end_points = []
            # Get each end-point
            for endpoint in collection.get("item"):

                # --------------------------------------------------------------------------
                # APITestRequest info
                # --------------------------------------------------------------------------
                query_info = endpoint.get("request")

                # APITestRequest headers
                request_headers = []
                for header in query_info.get("header"):
                    request_headers.append(APITestHeader(key=header.get("key"),
                                                         value=header.get("value")))

                # APITestRequest body
                request_body_content_type = from_http_content_type_get_type(request_headers, query_info.get("body").get("mode"))

                request_body = APITestBody(content_type=request_body_content_type,
                                           value=from_raw_body_get_python_object(data_type=request_body_content_type,
                                                                                 data=query_info.get("body").get("formdata")))

                # Build request
                _request_url = query_info.get("url") \
                    if query_info.get("url").startswith("http") \
                    else "http://{}".format(query_info.get("url"))
                request = APITestRequest(url=_request_url,
                                         method=query_info.get("method"),
                                         headers=request_headers,
                                         body=request_body)

                # --------------------------------------------------------------------------
                # APITestResponse info
                # --------------------------------------------------------------------------
                response_list = endpoint.get("response")

                responses = []
                if response_list:

                    for response_info in response_list:

                        # APITestResponse headers
                        response_headers = []
                        for header in response_info.get("header"):
                            response_headers.append(APITestHeader(key=header.get("key"),
                                                                  value=header.get("value")))

                        # APITestResponse APITestBody
                        response_body_content_type = from_http_content_type_get_type(response_headers, None)

                        response_body = APITestBody(content_type=response_body_content_type,
                                                    value=from_raw_body_get_python_object(data_type=response_body_content_type,
                                                                                          data=response_info.get("body")))

                        # APITestResponse cookie
                        response_cookies = []
                        for cookie in response_info.get("cookie"):
                            response_cookies.append(APITestCookie(expires=cookie.get("expires"),
                                                                  host_only=cookie.get("hostOnly"),
                                                                  http_only=cookie.get("httpOnly"),
                                                                  domain=cookie.get("domain"),
                                                                  path=cookie.get("path"),
                                                                  secure=cookie.get("secure"),
                                                                  session=cookie.get("session"),
                                                                  value=cookie.get("value")))

                            # Build response
                            responses.append(APITestResponse(code=response_info.get("code"),
                                                             status=response_info.get("status"),
                                                             headers=response_headers,
                                                             body=response_body,
                                                             cookies=response_cookies))

                end_points.append(APITestEndPoint(name=endpoint.get("name"),
                                                  description=endpoint.get("description"),
                                                  request=request,
                                                  response=responses))

            collections.append(APITestCollection(name=endpoint.get("name"),
                                                 description=endpoint.get("description"),
                                                 end_points=end_points))

    except Exception as exc:
        raise ApitestInvalidFormatError from exc

    data = APITest(title=postman_info.get("info").get("name"),
                   description=postman_info.get("info").get("description"),
                   collections=collections)

    return data


def postman_parser_form_file(file_path: str,
                             environment_vars: dict = None):
    """
    Get a parser collection, in JSON input format, and parser it

    :param file_path: file path
    :type file_path: str

    :return: a Postman object
    :rtype: APITest

    :raise ApitestInvalidFormatError: When the Postman JSON file has wrong format
    """
    assert file_path is not None

    with open(file_path, "r") as f:
        try:
            loaded_data = load(f)
        except (ValueError, TypeError) as e:
            raise ApitestInvalidFormatError from e

    return postman_parser(loaded_data,
                          environment_vars)


__all__ = ("postman_parser", "postman_parser_form_file", "PostmanConfig")

