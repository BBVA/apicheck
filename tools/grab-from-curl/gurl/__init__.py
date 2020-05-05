from functools import reduce
import io

import httptools
import hexdump

from gurl.RequestResponseCallbacks import RequestResponseCallbacks
import gurl.curlparse as cp
import gurl.hexdealer as hd


def _parse_raw_http(parser_builder, raw_http, parser_extract=None):
    callbacks = RequestResponseCallbacks()
    parser = parser_builder(callbacks)
    parser.feed_data(raw_http)
    callbacks.data["version"] = parser.get_http_version()
    if parser_extract:
        parser_data, parser_meta = parser_extract(parser)
        data = reduce(_dict_reducer, [callbacks.data, parser_data], {})
        meta = reduce(_dict_reducer, [callbacks.meta, parser_meta], {})
        return data, meta
    return callbacks.data, callbacks.meta


def _request(req):
    def _build_parser(callbacks):
        return httptools.HttpRequestParser(callbacks)
    def _extract_from_parser(parser):
        return {"method": parser.get_method().decode("utf-8")}, {}
    request_data, request_meta = _parse_raw_http(
            _build_parser, req, _extract_from_parser)

    return request_data, request_meta


def _response(res):
    def _build_parser(callbacks):
        return httptools.HttpResponseParser(callbacks)
    def _extract_from_parser(parser):
        return {"status": parser.get_status_code()}, {}
    request_data, request_meta = _parse_raw_http(
        _build_parser, res, _extract_from_parser
    )

    return request_data, request_meta


def _dict_reducer(x, acc):
    acc.update(x)
    return acc


def parse_binary(raw_request, raw_response):
    if not raw_request or not raw_response:
        return None

    request_data, request_meta = _request(raw_request)
    response_data, response_meta = _response(raw_response)
    meta = reduce(_dict_reducer, [request_meta, response_meta], {})

    return {
        "_meta": meta,
        "request": request_data,
        "response": response_data
    }


def parse_curl_trace(curl_trace_content):
    if not curl_trace_content:
        return None
    
    def block_to_bytes(block):
        no_header = b'\n'.join(block.split(b'\n')[1:])
        hex_part = hd.extract_hex_from_curl(no_header)
        return bytes.fromhex(hex_part.decode("utf-8"))

    log = []
    req = bytearray()
    res = bytearray()
    
    for block in cp.curl_trace_block_iterator(curl_trace_content):
        if block.startswith(b"=="):
            msg = block.decode("utf-8")
            msg = msg.replace("== ", "")
            log.append(msg)
        elif block.startswith(b'=> Send header'): #Send header
            req.extend(block_to_bytes(block))
        elif block.startswith(b'=> Send data'): #Send data
            req.extend(block_to_bytes(block))
        elif block.startswith(b'<= Recv header'): #Recv header
            res.extend(block_to_bytes(block))
        elif block.startswith(b'<= Recv data'): #Recv data
            res.extend(block_to_bytes(block))
        else: # not my bussiness
            pass

    reqres = parse_binary(req, res)
    reqres["_meta"]["curl_log"] = log
    return reqres
