try:
    from ujson import load, loads
except ImportError:  # pragma: no cover
    from json import load, loads

from booby import *
from enum import Enum
from booby.fields import __all__ as __all__booby__


# --------------------------------------------------------------------------
# Execution config
# --------------------------------------------------------------------------
class SharedConfig(Model):
    verbosity = Integer(default=0)
    debug = Boolean(default=False)
    timeout = Integer(default=10)


# --------------------------------------------------------------------------
# API Test Model
# --------------------------------------------------------------------------
class APITestContentType(Enum):
    form = "application/www-form-urlencoded"
    json = "application/json"
    raw = "text/plain"


class APITestCookie(Model):
    __ignore_missing__ = True

    expires = String()
    host_only = Boolean(default=False)
    http_only = Boolean(default=False)
    domain = String(default="*")
    path = String(default="/")
    secure = Boolean(default=False)
    session = Boolean(default=True)
    value = String()


class APITestBody(Model):
    __ignore_missing__ = True

    #: HTTP Format content type. Example: "application/json"
    content_type = String()
    value = Raw()


class APITestHeader(Model):
    __ignore_missing__ = True

    key = String()
    value = String()


class APITestResponse(Model):
    __ignore_missing__ = True

    code = Integer(default=200)
    status = String(default="OK")
    headers = Collection(APITestHeader)
    cookies = Collection(APITestCookie)
    body = Embedded(APITestBody)


class APITestRequest(Model):
    __ignore_missing__ = True

    url = URL()
    method = String()
    headers = Collection(APITestHeader)
    body = Embedded(APITestBody)


class APITestEndPoint(Model):
    __ignore_missing__ = True

    name = String()
    description = String()
    request = Embedded(APITestRequest)
    response = Collection(APITestResponse)


class APITestCollection(Model):
    __ignore_missing__ = True

    name = String()
    description = String()
    end_points = Collection(APITestEndPoint)


class APITest(Model):
    """
    Main Class for APITest collection data structure.

    This Class act as a entry point to load API Test collection.

    You can load and API Test JSON file directly doing:

    >>> import json
    >>> data =json.load(open("myjson.json", "r").read())
    >>> APITest(**data)

    .. note:

        Pay attention to the two asterisk before of "data" var. These are necessary to tell
        Python that the must load the JSON as a **kwarg input arguments.

        Summary:

        **WRONG:**

        APITest(data)

        **GOOD**

        APITest(**data)

    """
    __ignore_missing__ = True

    title = String()
    description = String()
    version = Integer(default=2)
    collections = Collection(APITestCollection)


def transform_apitest_body_to_queryable(request: APITestBody):
    """
    This function get an instance of APITestBody and transform it into a valid data for a make a query.

    >>> transform_apitest_body_to_queryable(APITestBody({}))
    >>>

    :param request:
    :type request:
    :return:
    :rtype:
    """
    assert isinstance(request, APITestBody)

    # Select the type of data by Content-type in HTTP Header
    content_type = request.content_type
    body = request.value

    if not content_type:
        content_type = "application/json"

    try:
        content = APITestContentType(content_type)
    except ValueError:
        return body

    if content == APITestContentType.raw:
        return body
    elif content == APITestContentType.json:
        return loads(body)
    elif content == APITestContentType.form:
        return body


__all__ = ("APITestContentType", "APITestCookie", "APITestBody", "APITestHeader",
           "APITestResponse", "APITestRequest", "APITestEndPoint", "APITestCollection", "APITest",
           "transform_apitest_body_to_queryable", "SharedConfig") + __all__booby__
