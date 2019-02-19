import sys
import socket
import asyncio
import logging

from typing import Callable

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser

BUFFER_SIZE = 65536
CONNECT_TIMEOUT_SECONDS = 5


def create_logger():
    logger = logging.getLogger('proxy')
    logger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(threadName)s - %(message)s')
    consoleHandler.setFormatter(formatter)

    logger.addHandler(consoleHandler)

    return logger


logger = create_logger()

#
# def client_connection_string(writer):
#     return '{} -> {}'.format(
#         writer.get_extra_info('peername'),
#         writer.get_extra_info('sockname'))
#
#
# def remote_connection_string(writer):
#     return '{} -> {}'.format(
#         writer.get_extra_info('sockname'),
#         writer.get_extra_info('peername'))


async def proxy_data(reader, writer, connection_string):
    try:
        while True:
            data = await reader.read(BUFFER_SIZE)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception as e:
        logger.info('proxy_data_task exception {}'.format(e))
    finally:
        writer.close()
        logger.info('close connection {}'.format(connection_string))


# async def accept_client(client_reader, client_writer, remote_address,
#                         remote_port):
async def accept_client(client_reader, client_writer):

    # client_string = client_connection_string(client_writer)
    # logger.info('accept connection {}'.format(client_string))
    try:
        data = await client_reader.read()
        print("REQUEST:")
        print(data)
        method, target, query = data.decode("UTF-8").split(" ", maxsplit=2)

        if method.lower() != "connect":
            logger.error("Connection is not a proxy query")

        try:
            remote_address, remote_port = target.split(":")
        except ValueError:
            remote_address = target
            remote_port = 80

        remote_reader, remote_writer = await asyncio.wait_for(
            asyncio.open_connection(host=remote_address, port=remote_port),
            timeout=CONNECT_TIMEOUT_SECONDS)

        remote_writer.write(query.encode("UTF-8"))

        response_data = await remote_reader.read()
        print("RESPONSE:")
        print(response_data)

    except asyncio.TimeoutError:
        logger.info('connect timeout')
        client_writer.close()
    except Exception as e:
        logger.info('error connecting to remote server: {}'.format(e))
        client_writer.close()
    else:
        raise ValueError("XXXXX")
        # asyncio.ensure_future(
        #     proxy_data(client_reader, remote_writer, remote_string))
        # asyncio.ensure_future(
        #     proxy_data(remote_reader, client_writer, client_string))


def recover_response_for_proxy(host: str,
                               port: int,
                               request: bytes,
                               callback: Callable) -> bytes:
    """

    callback format:

        callback(RESPONSE_HTTP_CODE,
                 RESPONSE_MESSAGE,
                 RESPONSE_BODY,
                 RESPONSE_HEADERS)

    """
    p = HttpParser()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    body = []
    body_append = body.append
    try:
        s.connect((host, port))
        s.send(request)

        while True:
            data = s.recv(1024)
            if not data:
                break

            recved = len(data)
            nparsed = p.execute(data, recved)
            assert nparsed == recved

            if p.is_headers_complete():
                print(p.get_headers())

            if p.is_partial_body():
                body_append(p.recv_body())

            if p.is_message_complete():
                break

    finally:
        s.close()

    # -------------------------------------------------------------------------
    # Callback calling
    # -------------------------------------------------------------------------
    callback(p.get_status_code(),
             None,
             body=b"".join(body),
             headers=dict(p.get_headers()))


if __name__ == "__main__":
    def hello(http_code, http_message, body, headers):
        print("HTTP RESPONSE CODE: ", http_code)
        print("HTTP RESPONSE MESSAGE: ", http_message)
        print("HTTP RESPONSE BODY: ", body)
        print("HTTP RESPONSE HEADERS: ", headers)

    listen_addr = "0.0.0.0:9000"

    # try:
    #     local_address_port_list = map(parse_addr_port_string, sys.argv[1:-1])
    #     (remote_address, remote_port) = parse_addr_port_string(sys.argv[-1])
    # except:
    #     print_usage_and_exit()

    def handle_client(client_reader, client_writer):
        asyncio.ensure_future(accept_client(
            client_reader=client_reader, client_writer=client_writer))

    loop = asyncio.get_event_loop()
    local_address, local_port = "127.0.0.1", 8000

    try:
        server = loop.run_until_complete(
            asyncio.start_server(handle_client,
                                 host=local_address,
                                 port=local_port))
    except Exception as e:
        logger.error('Bind error: {}'.format(e))
        sys.exit(1)

    for s in server.sockets:
        logger.info('listening on {}'.format(s.getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # start_proxy(
    #     'gunicorn.org',
    #     80,
    #     b"GET / HTTP/1.1\r\nHost: gunicorn.org\r\n\r\n",
    #     hello
    # )
