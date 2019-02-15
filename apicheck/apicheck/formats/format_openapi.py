import yaml

from openapi3 import OpenAPI
from openapi3.errors import SpecError

import apicheck.model as m


def openapi(content: str) -> m.BaseAPICheck:
    if not content:
        return None
    try:
        parsed = yaml.load(content)
        api = OpenAPI(parsed)
        return m.BaseAPICheck()
    except SpecError:
        # better return some own data
        return None
