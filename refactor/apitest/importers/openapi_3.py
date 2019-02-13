import os
import yaml
import logging

from slugify import slugify
from openapi3 import OpenAPI
from typing import Iterable, List
from urllib.parse import urlparse

from . import APIImporter
from ..model_maps import EndPoint, EndPointParam, APITestModel, APIMetadata, \
    EndPointBody, EndPointResponse, APIDeployments

log = logging.getLogger(__name__)


class OpenAPISource(APIImporter):

    def __init__(self, path_file: str):
        self.path_file: str = path_file
        self._metadata: APIMetadata = None
        self._open_api_class: OpenAPI = None
        self._end_points: List[str] = None
        self._api_model: APITestModel = None

    @property
    def open_api_class(self) -> OpenAPI:
        if not self._open_api_class:
            # load the spec file and read the yaml
            log.debug("Loading OpenAPI file")
            with open(self.path_file) as f:
                # spec = yaml.safe_load(f.read())
                spec = yaml.load(f.read())
                self._open_api_class = OpenAPI(spec)

        return self._open_api_class

    @property
    def metadata(self) -> APIMetadata:

        if not self._open_api_class:
            servers = getattr(self.open_api_class, "servers", [])
            scheme = domain = api_path = port = None
            if len(servers) > 0:
                s_url = getattr(servers[0], "url", None)
                if s_url:
                    scheme, domain, api_path, *_ = urlparse(s_url)

                    if ":" in domain:
                        domain, port = domain.split(":")

            api_info = getattr(self.open_api_class, "info")

            api_info_version = getattr(api_info, "version")
            if not api_info_version:
                api_info_version = "1.0.0"

            api_info_title = getattr(api_info, "title")
            if api_info:
                api_info_title = slugify(api_info_title.lower())
            else:
                api_info_title, _ = os.path.splitext(os.path.basename(
                    self.path_file)
                )

            self._metadata = APIMetadata(
                name=api_info_title,
                base_api_path=api_path,
                version=api_info_version,
                deployments=[APIDeployments(
                    domain=domain,
                    scheme=scheme,
                    port=port
                )]
            )

        return self._metadata

    def _get_scheme_object(self, object_name: str) -> dict:
        return self.open_api_class.components.schemas[object_name]

    @property
    def end_points(self) -> Iterable[EndPoint]:

        if not self._end_points:

            self._end_points = []

            log.debug("Discovering API paths")
            for path_name, path_content in self.open_api_class.paths.items():

                #
                # Getting each verb
                #
                for verb in ("delete", "get", "post", "put",
                             "head", "options", "patch", "trace"):

                    log.debug(f"Discovered path for verb '{verb.upper()}'")

                    verb_content = getattr(path_content, verb, None)
                    if not verb_content:
                        continue

                    #
                    # Path information
                    #
                    description = getattr(verb_content, "description", "")

                    end_point = EndPoint(
                        uri=path_name,
                        description=description,
                        verb=verb
                    )

                    #
                    # Extract params
                    #
                    self.__extract_params(verb_content, end_point)

                    #
                    # Extract body
                    #
                    self.__extract_body(verb_content, end_point)

                    #
                    # Extract Responses
                    #
                    self.__extract_responses(verb_content, end_point)

                    #
                    # Add endpoint to internal cache
                    #
                    self._end_points.append(end_point)

                    yield end_point

        return self._end_points.__iter__

    @property
    def api_model(self) -> APITestModel:
        log.debug("Building API Model")
        if not self._api_model:
            self._api_model = APITestModel(
                metadata=self.metadata,
                endpoints=self.end_points
            )

        return self._api_model

    def __extract_params(self, verb, end_point):

        for param in getattr(verb, "parameters", []):

            if getattr(param, "in_", "") != "query":
                continue

            #
            # Query params data
            #
            p_name = getattr(param, "name")
            p_description = getattr(param, "description", None)
            p_type = getattr(param, "schema", {}).get("type", None)
            p_minimum = getattr(param, "schema", {}).get("minimum",
                                                         None)
            p_default = getattr(param, "schema", {}).get("default",
                                                         None)

            end_point.query_params.append(EndPointParam(
                name=p_name,
                param_type=p_type,
                description=p_description,
                minimum_value=p_minimum,
                default=p_default
            ))

    def __extract_body(self, content: str, end_point: EndPoint):
        body = getattr(content, "requestBody")

        if not body:
            return

        #
        # Check if boyd has more than one content-type
        #
        if len(body.content) > 1:
            raise ValueError(f"RequestBody for end-point '{body.path[1]}' "
                             f"has more than one content-type")

        content_type, *_ = set(body.content.keys())

        end_point.body = EndPointBody(
            description=getattr(body, "description", None),
            required=getattr(body, "required", None),
            content_type=content_type
        )

        #
        # Body parameters
        #
        schema = getattr(body.content[content_type], "schema")
        end_point.body.params.extend(list(self.__extract_schema_properties(
            schema)
        ))

    def __extract_responses(self, content: str, end_point: EndPoint):
        responses = getattr(content, "responses")

        if not responses:
            return

        for response_code, response_value in responses.items():

            #
            # Check if boyd has more than one content-type
            #
            if len(response_value.content) > 1:
                raise ValueError(f"RequestBody for end-point '{end_point.uri}'"
                                 f" has more than one content-type")

            if response_code == "default":
                log.info(f"Default response without HTTP code for end-point: "
                         f"'{end_point.uri}'. Omitting")
                continue

            content_type, *_ = set(response_value.content.keys())

            schema = getattr(response_value.content[content_type], "schema")
            if schema and schema.properties:
                end_point.responses.append(EndPointResponse(
                    http_code=response_code,
                    content_type=content_type,
                    description=getattr(response_value, "description", None),
                    params=list(self.__extract_schema_properties(schema))
                ))

    def __extract_schema_properties(self, schema):
        if schema and schema.properties:
            for param_name, value in schema.properties.items():
                    yield EndPointParam(
                        name=param_name,
                        param_type=getattr(value, "type", None),
                        description=getattr(value, "description", None),
                        default=getattr(value, "default", None),
                        max_length=getattr(value, "maxLength", None),
                        minimum_value=getattr(value, "minimumValue", None),
                        maximum_value=getattr(value,"maximumValue", None),
                    )


__all__ = ("OpenAPISource", )
