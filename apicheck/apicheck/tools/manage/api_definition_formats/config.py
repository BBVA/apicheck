from enum import Enum
from dataclasses import dataclass

from apicheck.config import CommonConfig


class DefinitionsFormats(Enum):
    RAML = 1
    OPENAPI_3 = 2
    SWAGGER = 3


@dataclass
class RunningConfig(CommonConfig):
    FORMAT_CHOICES = (
        (DefinitionsFormats.RAML.name, "RAML"),
        (DefinitionsFormats.OPENAPI_3.name, "OpenAPI 3"),
        (DefinitionsFormats.SWAGGER.name, "Swagger")
    )

    format: str
    file_path: str
    api_name: str = None
    api_version: str = None
    append_to_metadata: str = None



