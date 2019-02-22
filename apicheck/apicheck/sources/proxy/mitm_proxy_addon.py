import re
import json
import uuid
import asyncio

from urllib.parse import urlparse

from apicheck.sources.proxy import ProxyConfig
from apicheck.db import get_engine, ProxyLogs, APIRequests, APIResponses, \
    APIDefinitionMetadata

VALID_CONTENT_TYPES = (
    "text/html", "application/json", "application/javascript",
    "application/xml", "text/xml", "text/plain", "text/css",
    "application/x-javascript"
)

REGEX_VERSION_FINDER = re.compile(r"""(\/)(v[0-9]{1,20})(\/)""")


class APICheckProxyMode:

    def __init__(self):
        self._connection = None
        self._metadata_id = None
        self._loop = asyncio.get_event_loop()
        self.proxy_config = ProxyConfig()
        self.proxy_session_id = str(uuid.uuid4())

    def response(self, flow):
        """This functions overwrites the MITM Proxy event 'response'"""
        #
        # Only if proxy is set as 'learning mode' will storage the definitions.
        # In this case, after save the definition, 'save_definition' method
        # will call the save 'save_into_log' method with the just saved Id of
        # Request object. Then the method stores the log and links with the
        # request object.
        #
        # If not 'learning mode' is set, only stores the log
        #
        if self.proxy_config.learning_mode:
            asyncio.get_event_loop().create_task(self.save_definition(flow))
        else:
            asyncio.get_event_loop().create_task(self.save_into_log(flow))

    # -------------------------------------------------------------------------
    # Lazy methods
    # -------------------------------------------------------------------------
    async def db_connection(self):
        """This coroutine returns a valid database connection"""
        if not self._connection:
            print("[*] Connecting to database")
            self._connection = await get_engine().connect()
        return self._connection

    async def metadata(self, flow):
        """This coroutine returns the API metadata database object"""
        if not self._metadata_id:
            connection = await self.db_connection()

            #
            # currently the API Name will be the value of md5 hash of domain
            #
            api_name = flow.request.host

            #
            # The version will be got by URL:
            # /api/v1/...
            # /api/v2/...
            found = REGEX_VERSION_FINDER.match(flow.request.path)

            # In case It couldn't find the version in URL, version will be the
            # proxy sequential
            if found:
                api_version = found.group(1)
            else:
                api_version = "v1"

            print("[*] Building metadata")
            try:
                ret = await connection.execute(
                    APIDefinitionMetadata.insert().values(
                        api_name=api_name,
                        api_version=api_version
                ))
                self._metadata_id = ret.inserted_primary_key[0]

            except Exception as e:

                #
                # If already exits this metadata
                #
                if " unique constraint" in str(e).lower():
                    ret = await connection.execute(
                        APIDefinitionMetadata.select(
                            APIDefinitionMetadata.c.api_name==api_name
                        ))
                    # results = await ret.fetchone()
                    self._metadata_id, *_ = await ret.fetchone()
                else:
                    print("ERROR BUILDING METADATA: ", e)

        return self._metadata_id

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def clean_content(self, content: dict, exclude: str = None) -> dict:
        data = content["data"]

        ret = {}
        for x, y in data.__dict__.items():
            if x == "headers" or x.startswith("_"):
                continue

            if exclude and x == exclude:
                continue

            try:
                ret[x] = y.decode("UTF-8")
            except (AttributeError, UnicodeDecodeError):
                ret[x] = y

        ret["headers"] = {
            x.decode("UTF-8"): y.decode("UTF-8")
            for x, y in data.headers.fields
        }

        return ret

    def bytes_dict_to_string(self, bytes_dict: dict) -> dict:
        return dict(bytes_dict.items())

    # -------------------------------------------------------------------------
    # Main saving methods
    # -------------------------------------------------------------------------
    async def save_into_log(self, flow, request_id: int = None):
        """Save request / response into ProxyLog database table"""

        #
        # Doesn't store assets content, by default
        #
        exclude = None
        if not self.proxy_config.store_assets_content:
            content_type = flow.response.data.headers[b"content-type"]
            if content_type not in VALID_CONTENT_TYPES:
                exclude = "content"

        plain_request = json.dumps(self.clean_content(flow.request.__dict__))
        plain_response = json.dumps(self.clean_content(
            flow.response.__dict__, exclude=exclude
        ))

        #
        # Store into logs
        #
        try:
            connection = await self.db_connection()

            await connection.execute(ProxyLogs.insert().values(
                proxy_session_id=self.proxy_session_id,
                request=plain_request,
                response=plain_response,
                request_id=request_id))
        except Exception as e:
            print("!" * 20, "ERROR SAVING LOG: ", e)

    async def save_definition(self, flow):
        # -------------------------------------------------------------------------
        # Extract request
        # -------------------------------------------------------------------------
        request_headers = json.dumps(self.bytes_dict_to_string(
            flow.request.headers
        ))
        request_uri = urlparse(flow.request.pretty_url).path
        request_http_version = flow.request.http_version
        request_body = flow.request.content.decode("utf-8")

        # -------------------------------------------------------------------------
        # Extract response
        # -------------------------------------------------------------------------
        response = flow.request
        response_headers = json.dumps(self.bytes_dict_to_string(
            response.headers
        ))
        response_http_code = flow.response.status_code
        response_http_message = flow.response.reason
        response_body = flow.response.content.decode("utf-8")

        inserted_request_id = None
        try:
            connection = await self.db_connection()
            metadata_id = await self.metadata(flow)

            #
            # Store request
            #
            _req_query = await connection.execute(APIRequests.insert().values(
                uri=request_uri,
                http_version=request_http_version,
                headers=request_headers,
                body=request_body,
                metadata_id=metadata_id
            ))
            inserted_request_id = _req_query.inserted_primary_key[0]

            #
            # Store response
            #
            await connection.execute(APIResponses.insert().values(
                http_code=response_http_code,
                http_message=response_http_message,
                headers=response_headers,
                body=response_body,
                requests_id=inserted_request_id
            ))
        except Exception as e:
            print("!" * 20, "ERROR SAVING DEFINITION: ", e)

        # ---------------------------------------------------------------------
        # Now start the flow to store query into ProxyLog
        # ---------------------------------------------------------------------
        await self.save_into_log(flow, inserted_request_id)


addons = [
    APICheckProxyMode()
]
