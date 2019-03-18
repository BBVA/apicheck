import os
import json
import pytest

from dataclasses import dataclass
from typing import Any, Callable, List


@pytest.fixture()
def openapi3_content() -> dict:
    f = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "openapi3-linode.json")
    )

    with open(f, "r") as f:
        yield json.load(f)


# -------------------------------------------------------------------------
#
# Dataclass Model
#
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Info Root Model
# -------------------------------------------------------------------------
@dataclass
class InfoContact:
    name: str
    url: str


@dataclass
class InfoXLogo:
    url: str
    backgroundColor: str


@dataclass
class Info:
    version: str
    title: str
    description: str
    contact: str
    x_logo: InfoXLogo
    contact: InfoContact


# -------------------------------------------------------------------------
# Servers root model
# -------------------------------------------------------------------------
@dataclass
class Servers:
    url: List[str]


# -------------------------------------------------------------------------
# Paths root model
# -------------------------------------------------------------------------
@dataclass
class Paths:
    url: List[str]


# -------------------------------------------------------------------------
#
# Components model
#
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Components -> securitySchemes
# -------------------------------------------------------------------------
@dataclass
class ComponentsSecuritySchemesPersonalAccessToken:
    type: str
    scheme: str


@dataclass
class ComponentsSecuritySchemesOauthAuthorizationCodeScopes:
    account_read_only: str
    account_read_write: str
    domains_read_only: str
    domains_read_write: str
    events_read_only: str
    events_read_write: str
    images_read_only: str
    images_read_write: str
    ips_read_only: str
    ips_read_write: str
    linodes_read_only: str
    linodes_read_write: str
    longview_read_only: str
    longview_read_write: str
    nodebalancers_read_only: str
    nodebalancers_read_write: str
    stackscripts_read_only: str
    stackscripts_read_write: str
    volumes_read_only: str
    volumes_read_write: str


@dataclass
class ComponentsSecuritySchemesOauthAuthorizationCode:
    authorizationUrl: str
    tokenUrl: str
    scopes: ComponentsSecuritySchemesOauthAuthorizationCodeScopes


@dataclass
class ComponentsSecuritySchemesOauthFlows:
    authorizationCode: ComponentsSecuritySchemesOauthAuthorizationCode


@dataclass
class ComponentsSecuritySchemesOauth:
    type: str
    flows: ComponentsSecuritySchemesOauthFlows


@dataclass
class ComponentsSecuritySchemes:
    personalAccessToken: ComponentsSecuritySchemesPersonalAccessToken
    oauth: ComponentsSecuritySchemesOauth

# -------------------------------------------------------------------------
# Components -> responses
# -------------------------------------------------------------------------
@dataclass
class ComponentsResponsesContent:
    pass

@dataclass
class ComponentsErrorResponse:
    description: str
    content: ComponentsResponsesContent


@dataclass
class ComponentsResponses:
    ErrorResponse: ComponentsErrorResponse


# -------------------------------------------------------------------------
# Components -> Parameters
# -------------------------------------------------------------------------
@dataclass
class ComponentsParametersSchema:
    type: str
    minimum: int = 0
    default: int = -1
    maximum: int = -1


@dataclass
class ComponentsParametersPageOffset:
    name: str
    in_: str
    description: str
    required: bool
    schema: ComponentsParametersSchema


@dataclass
class ComponentsParametersPageSize:
    name: str
    in_: str
    description: str
    schema: ComponentsParametersSchema


@dataclass
class ComponentsParameters:
    pageOffset: ComponentsParametersPageOffset
    pageSize: ComponentsParametersPageSize


#
# Root components
#
@dataclass
class Components:
    securitySchemes: ComponentsSecuritySchemes
    responses: ComponentsResponses
    parameters: ComponentsParameters


# -------------------------------------------------------------------------
# Internal mappers
# -------------------------------------------------------------------------
@dataclass
class ParserMap:
    destination: str
    klass: Callable


def parse(content, data_dict: dict) -> dict or list or object:
    try:
        ret = {}
        for key, value in content.items():

            try:
                parser_map: ParserMap = data_dict[key]

                # Build dataclass
                parse_result = parse(value, data_dict)
                if type(parse_result) is dict:
                    parsed = parser_map.klass(**parse_result)
                else:
                    parsed = parser_map.klass(parse_result)

                if parser_map.destination:
                    rule_result = {parser_map.destination: parsed}
                else:
                    return parsed

            except KeyError:
                # We haven't the rule
                r_key = key.replace("-", "_").replace(":", "_")

                # Check if r_key has some reserved Python word
                for reserved_word in ("in", "class"):
                    if r_key == reserved_word:
                        r_key = f"{reserved_word}_"
                        break

                rule_result = {
                    r_key: value
                }

            except TypeError as e:
                _str_e = str(e)
                if "__init__() got an unexpected keyword argument" in _str_e:
                    prop_name = "".join(_str_e.split(" ")[-1])

                    raise TypeError(f"Missing property {prop_name} on "
                                    f"Dataclass: '{parser_map.klass.__name__}'")

                elif "required positional argument" in _str_e:
                    prop_name = "".join(_str_e.split(" ")[-1])
                    raise TypeError(
                        f"Missing property {prop_name} parameter "
                        f"in Dataclass '{parser_map.klass.__name__}'")

                raise TypeError(e)

            ret.update(rule_result)

        return ret

    except AttributeError as e:
        # When content is a list
        l_ret = []
        for c in content:
            l_ret.append(parse(c, data_dict))

        return l_ret


DATA_DICT_INFO = {
    # Info root element
    "info": ParserMap(None, Info),
    "x-logo": ParserMap("x_logo", InfoXLogo),
    "contact": ParserMap("contact", InfoContact)
}

DATA_DICT_SERVERS = {
    # Servers root element
    "servers": ParserMap(None, Servers)
}

DATA_DICT_COMPONENTS = {
    # Servers root element
    "components": ParserMap(None, Components),
    "securitySchemes": ParserMap("securitySchemes", ComponentsSecuritySchemes),
    "personalAccessToken": ParserMap("personalAccessToken", ComponentsSecuritySchemesPersonalAccessToken),
    "oauth": ParserMap("oauth", ComponentsSecuritySchemesOauth),
    "flows": ParserMap("flows", ComponentsSecuritySchemesOauthFlows),
    "authorizationCode": ParserMap("authorizationCode", ComponentsSecuritySchemesOauthAuthorizationCode),
    "scopes": ParserMap("scopes", ComponentsSecuritySchemesOauthAuthorizationCodeScopes),
    "responses": ParserMap("responses", ComponentsResponses),
    "parameters": ParserMap("parameters", ComponentsParameters),
    "ComponentErrorResponse": ParserMap("ComponentErrorResponse", ComponentsErrorResponse),
    "pageOffset": ParserMap("pageOffset", ComponentsParametersPageOffset),
    "pageSize": ParserMap("pageSize", ComponentsParametersPageSize),
    "schema": ParserMap("schema", ComponentsParametersSchema)
}


# -------------------------------------------------------------------------
# Info
# -------------------------------------------------------------------------
def test_info(openapi3_content):
    c: Info = parse(openapi3_content, DATA_DICT_INFO)

    assert isinstance(c, Info)
    assert c.version == "4.0.17"
    assert c.title == "Linode API"
    assert c.description == "# Introduction\nThe Linode API provides the ability to programmatically manage the full\nrange of Linode products and services.\n\nThis reference is designed to assist application developers and system\nadministrators.  Each endpoint includes descriptions, request syntax, and\nexamples using standard HTTP requests. Response data is returned in JSON\nformat.\n\n\nThis document was generated from our OpenAPI Specification.  See the\n<a target=\"_top\" href=\"https://www.openapis.org\">OpenAPI website</a> for more information.\n\n<a target=\"_top\" href=\"https://developers.linode.com/api/docs/v4/openapi.yaml\">Download the Linode OpenAPI Specification</a>.\n\n\n# Changelog\n\n<a target=\"_top\" href=\"https://developers.linode.com/changelog\">View our Changelog</a> to see release\nnotes on all changes made to our API.\n\n# Access and Authentication\n\nSome endpoints are publicly accessible without requiring authentication.\nAll endpoints affecting your Account, however, require either a Personal\nAccess Token or OAuth authentication (when using third-party\napplications).\n\n## Personal Access Token\n\nThe easiest way to access the API is with a Personal Access Token (PAT)\ngenerated from the\n<a target=\"_top\" href=\"https://cloud.linode.com/profile/tokens\">Linode Cloud Manager</a>.\n\nAll scopes for the OAuth security model (defined below) apply to this\nsecurity model as well.\n\n### Authentication\n\n| Security Scheme Type: | HTTP |\n|-----------------------|------|\n| **HTTP Authorization Scheme** | bearer |\n\n## OAuth\n\nThe OAuth workflow is a three-step process to authenticate a User before an\napplication can start making API calls on the User's behalf. If all you need\nis a Personal Access Token, feel free to skip ahead to the next section.\n\nFirst, the User visits the application's website and is directed to log with\nLinode. The User is then redirected to Linode's authentication server and\npresented the scope levels the application is requesting. Once the User\naccepts the request for access, we redirect them back to the application's\nspecified redirect URI with an access code.\n\nOnce the User has logged in to Linode and you have received an exchange code,\nyou will need to exchange that access code for an Authorization token. You\ndo this by making an HTTP POST request to the following address:\n\n```\nhttps://login.linode.com/oauth/token\n```\n\nMake this request as `application/x-www-form-urlencoded` or as\n`multipart/form-data` and include the following parameters in the POST body:\n\n| PARAMETER | DESCRIPTION |\n|-----------|-------------|\n| client_id | Your app's client ID |\n| client_secret | Your app's client secret |\n| code | The code you just received from the redirect |\n\nYou'll get a reponse like this:\n\n```json\n{\n  \"scope\": \"linodes:read_write\",\n  \"access_token\": \"03d084436a6c91fbafd5c4b20c82e5056a2e9ce1635920c30dc8d81dc7a6665c\"\n  \"token_type\": \"bearer\",\n  \"expires_in\": 7200,\n}\n```\n\nIncluded in the reponse is `access_token`. With this token, you can proceed to make\nauthenticated HTTP requests to the API by adding this header to each request:\n\n```\nAuthorization: Bearer 03d084436a6c91fbafd5c4b20c82e5056a2e9ce1635920c30dc8d81dc7a6665c\n```\n\n### Authentication\n\n| Security Scheme Type: | Oauth2 |\n|-----------------------|--------|\n| **AuthorizationCode Oauth Flow** |  **Authorization URL:** https://login.linode.com/oauth/authorize<br />**Token URL:** https://login.linode.com/oauth/token<br />**Scopes:**<br /><ul><li>`account:read_only` - Allows access to GET information about your Account.</li><li>`account:read_write` - Allows access to all endpoints related to your Account.</li><li>`domains:read_only` - Allows access to GET Domains on your Account.</li><li>`domains:read_write` - Allows access to all Domain endpoints.</li><li>`events:read_only` - Allows access to GET your Events.</li><li>`events:read_write` - Allows access to all endpoints related to your Events.</li><li>`images:read_only` - Allows access to GET your Images.</li><li>`images:read_write` - Allows access to all endpoints related to your Images.</li><li>`ips:read_only` - Allows access to GET your ips.</li><li>`ips:read_write` - Allows access to all endpoints related to your ips.</li><li>`linodes:read_only` - Allows access to GET Linodes on your Account.</li><li>`linodes:read_write` - Allow access to all endpoints related to your Linodes.</li><li>`longview:read_only` - Allows access to GET your Longview Clients.</li><li>`longview:read_write` - Allows access to all endpoints related to your Longview Clients.</li><li>`nodebalancers:read_only` - Allows access to GET NodeBalancers on your Account.</li><li>`nodebalancers:read_write` - Allows access to all NodeBalancer endpoints.</li><li>`stackscripts:read_only` - Allows access to GET your StackScripts.</li><li>`stackscripts:read_write` - Allows access to all endpoints related to your StackScripts.</li><li>`volumes:read_only` - Allows access to GET your Volumes.</li><li>`volumes:read_write` - Allows access to all endpoints related to your Volumes.</li></ul><br />|\n\n# Requests\n\nRequests must be made over HTTPS to ensure transactions are encrypted. The\nfollowing Request methods are supported:\n\n| METHOD | USAGE |\n|--------|-------|\n| GET    | Retrieves data about collections and individual resources. |\n| POST   | For collections, creates a new resource of that type. Also used to perform actions on action endpoints. |\n| PUT    | Updates an existing resource. |\n| DELETE | Deletes a resource. This is a destructive action. |\n\n\n# Responses\n\nActions will return one following HTTP response status codes:\n\n| STATUS  | DESCRIPTION |\n|---------|-------------|\n| 200 OK  | The request was successful. |\n| 204 No Content | The server successfully fulfilled the request and there is no additional content to send. |\n| 400 Bad Request | You submitted an invalid request (missing parameters, etc.). |\n| 401 Unauthorized | You failed to authenticate for this resource. |\n| 403 Forbidden | You are authenticated, but don't have permission to do this. |\n| 404 Not Found | The resource you're requesting does not exist. |\n| 429 Too Many Requests | You've hit a rate limit. |\n| 500 Internal Server Error | Please [open a Support Ticket](#operation/createTicket). |\n\n# Errors\n\nSuccess is indicated via <a href=\"https://en.wikipedia.org/wiki/List_of_HTTP_status_codes\" target=\"_top\">Standard HTTP status codes</a>.\n`2xx` codes indicate success, `4xx` codes indicate a request error, and\n`5xx` errors indicate a server error. A\nrequest error might be an invalid input, a required parameter being omitted,\nor a malformed request. A server error means something went wrong processing\nyour request. If this occurs, please\n[open a Support Ticket](#operation/createTicket)\nand let us know. Though errors are logged and we work quickly to resolve issues,\nopening a ticket and providing us with reproducable steps and data is always helpful.\n\nThe `errors` field is an array of the things that went wrong with your request.\nWe will try to include as many of the problems in the response as possible,\nbut it's conceivable that fixing these errors and resubmitting may result in\nnew errors coming back once we are able to get further along in the process\nof handling your request.\n\n\nWithin each error object, the `field` parameter will be included if the error\npertains to a specific field in the JSON you've submitted. This will be\nomitted if there is no relevant field. The `reason` is a human-readable\nexplanation of the error, and will always be included.\n\n# Pagination\n\nResource lists are always paginated. The response will look similar to this:\n\n```json\n{\n    \"data\": [ ... ],\n    \"page\": 1,\n    \"pages\": 3,\n    \"results\": 300\n}\n```\n\nPages start at 1. You may retrieve a specific page of results by adding\n`?page=x` to your URL (for example, `?page=4`). Page sizes default to 100,\nand can be set to return between 25 and 100. Page size can be set using\n`?page_size=x`.\n\n# Filtering and Sorting\n\nCollections are searchable by fields they include, marked in the spec as\n`x-linode-filterable: true`. Filters are passed\nin the `X-Filter` header and are formatted as JSON objects. Here is a request\ncall for Linode Types in our \"standard\" class:\n\n```Shell\ncurl \"https://api.linode.com/v4/linode/types\" \\\n  -H 'X-Filter: { \\\n    \"class\": \"standard\"\n  }'\n```\n\nThe filter object's keys are the keys of the object you're filtering,\nand the values are accepted values. You can add multiple filters by\nincluding more than one key. For example, filtering for \"standard\" Linode\nTypes that offer one vcpu:\n\n```Shell\n curl \"https://api.linode.com/v4/linode/types\" \\\n  -H 'X-Filter: { \\\n    \"class\": \"standard\",\n    \"vcpus\": 1\n  }'\n```\n\nIn the above example, both filters are combined with an \"and\" operation.\nHowever, if you wanted either Types with one vcpu or Types in our \"standard\"\nclass, you can add an operator:\n\n```Shell\ncurl \"https://api.linode.com/v4/linode/types\" \\\n  -H 'X-Filter: {\n    \"+or\": [\n      { \"vcpus\": 1 },\n      { \"class\": \"standard\" }\n    ]\n  }'\n```\n\nEach filter in the `+or` array is its own filter object, and all conditions\nin it are combined with an \"and\" operation as they were in the previous example.\n\nOther operators are also available. Operators are keys of a Filter JSON\nobject. Their value must be of the appropriate type, and they are evaluated\nas described below:\n\n| OPERATOR | TYPE   | DESCRIPTION                       |\n|----------|--------|-----------------------------------|\n| +and     | array  | All conditions must be true.       |\n| +or      | array  | One condition must be true.        |\n| +gt      | number | Value must be greater than number. |\n| +gte     | number | Value must be greater than or equal to number. |\n| +lt      | number | Value must be less than number. |\n| +lte     | number | Value must be less than or equal to number. |\n| +contains | string | Given string must be in the value. |\n| +neq      | string | Does not equal the value.          |\n| +order_by | string | Attribute to order the results by - must be filterable. |\n| +order    | string | Either \"asc\" or \"desc\". Defaults to \"asc\". Requires `+order_by`. |\n\nFor example, filtering for [Linode Types](#operation/getLinodeTypes)\nthat offer memory equal to or higher than 61440:\n\n```Shell\ncurl \"https://api.linode.com/v4/linode/types\" \\\n  -H 'X-Filter: {\n    \"memory\": {\n      \"+gte\": 61440\n    }\n  }'\n```\n\nYou can combine and nest operators to construct arbitrarily-complex queries.\nFor example, give me all [Linode Types](#operation/getLinodeTypes)\nwhich are either `standard` or `highmem` class, and\nhave between 12 and 20 vcpus:\n\n```Shell\ncurl \"https://api.linode.com/v4/linode/types\" \\\n  -H 'X-Filter: {\n    \"+or\": [\n      {\n        \"+or\": [\n          {\n            \"class\": \"standard\"\n          },\n          {\n            \"class\": \"highmem\"\n          }\n        ]\n      },\n      {\n        \"+and\": [\n          {\n            \"vcpus\": {\n              \"+gte\": 12\n            }\n          },\n          {\n            \"vcpus\": {\n              \"+lte\": 20\n            }\n          }\n        ]\n      }\n    ]\n  }'\n```\n\n# CLI (Command Line Interface)\n\nThe <a href=\"https://github.com/linode/linode-cli\" target=\"_top\">Linode CLI</a> allows you to easily\nwork with the API using intuitive and simple syntax. It requires a\n[Personal Access Token](#section/Personal-Access-Token)\nfor authentication, and gives you access to all of the features and functionality\nof the Linode API that are documented here with CLI examples.\n\nEndpoints that do not have CLI examples are currently unavailable through the CLI, but\ncan be accessed via other methods such as Shell commands and other third-party applications.\n"


def test_info_x_logo(openapi3_content):
    c: Info = parse(openapi3_content, DATA_DICT_INFO)

    # X-Logo
    assert isinstance(c.x_logo, InfoXLogo)
    assert c.x_logo.url == "/api/v4/linode-logo.svg"
    assert c.x_logo.backgroundColor == "#fafafa"


# -------------------------------------------------------------------------
# Servers
# -------------------------------------------------------------------------
def test_servers(openapi3_content):
    c: Servers = parse(openapi3_content, DATA_DICT_SERVERS)

    # X-Logo
    assert isinstance(c.url, list)
    assert all([isinstance(url, dict) for url in c.url])
    assert c.url[0]["url"] == "https://api.linode.com/v4"


# -------------------------------------------------------------------------
# Components
# -------------------------------------------------------------------------
def test_components(openapi3_content):
    #c: Servers = parse(openapi3_content, DATA_DICT_COMPONENTS)
    pass
