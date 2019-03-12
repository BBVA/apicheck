import json
import logging

from typing import Tuple


from .model import OpenAPI3
from .helpers import yaml_loader

logger = logging.getLogger("apicheck")


def load_openapi3(content, from_cache: bool = False) -> Tuple[str, OpenAPI3]:

    logger.info("Parsing OpenAPI information")

    if from_cache:
        parsed = return_json = content
    else:
        parsed = yaml_loader(content)
        return_json = json.dumps(parsed)

    return return_json, OpenAPI3(None)
