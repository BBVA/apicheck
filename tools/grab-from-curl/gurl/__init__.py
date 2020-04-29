from functools import reduce
import io

import httptools
import hexdump

from gurl.RequestResponseCallbacks import RequestResponseCallbacks


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


def parse_binary(raw_request):
    """
    Parse need binary string input from burl to parse
    """
    if not raw_request:
        return None

    parts = raw_request.split(b"\r\n\r\n")
    if len(parts) < 3:
        return None
    
    request_raw = parts[0]+b"\r\n\r\n"
    response_raw = b"\r\n\r\n".join(parts[1:])

    request_data, request_meta = _request(request_raw)
    response_data, response_meta = _response(response_raw)
    meta = reduce(_dict_reducer, [request_meta, response_meta], {})

    return {
        "_meta": meta,
        "request": request_data,
        "response": response_data
    }


def parse_curl_trace(curl_trace_content):
    if not curl_trace_content:
        return None

    buffers = [io.BytesIO(), io.BytesIO()]
    current = None
    content = io.BytesIO()
    for line in curl_trace_content.read().split(b'\n'):
        if line.startswith(b'=> Send header'): #Send header
            if current:
                h = hexdump.restore(content.getvalue().decode("utf-8"))
                buffers[current].write(h+b'\n')
                content = io.BytesIO()
            current = 1
        elif line.startswith(b'=> Send data'): #Send data
            if current:
                h = hexdump.restore(content.getvalue().decode("utf-8"))
                buffers[current].write(h+b'\n')
                content = io.BytesIO()
            current = 1
        elif line.startswith(b'<= Recv header'): #Recv header
            if current:
                h = hexdump.restore(content.getvalue().decode("utf-8"))
                buffers[current].write(h+b'\n')
                content = io.BytesIO()
            current = 2
        elif line.startswith(b'<= Recv data'): #Recv data
            if current:
                h = hexdump.restore(content.getvalue().decode("utf-8"))
                buffers[current].write(h+b'\n')
                content = io.BytesIO()
            current = 2
        elif line.startswith(b'=>'): #Send other stuff
            if current:
                h = hexdump.restore(content.getvalue().decode("utf-8"))
                buffers[current].write(h+b'\n')
                content = io.BytesIO()
            current = None
        elif line.startswith(b'<='): #Recv other stuff
            if current:
                h = hexdump.restore(content.getvalue().decode("utf-8"))
                buffers[current].write(h+b'\n')
                content = io.BytesIO()
            current = None
        elif line.startswith(b'=='): #Meta info
            continue
        elif current is not None:
            content.write(line+b'\n')
    request = hexdump.restore(buffers[0].getvalue().decode("utf-8"))
    response = hexdump.restore(buffers[1].getvalue().decode("utf-8"))
    print(buffers[0].getvalue())
