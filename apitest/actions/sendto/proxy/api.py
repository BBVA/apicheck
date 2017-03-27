import logging
import aiohttp
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from collections import namedtuple
from apitest import APITestEndPoint, APITest, transform_apitest_body_to_queryable

ProxyConfig = namedtuple("ProxyConfig", ("url", "user", "password"))
RequestResponse = namedtuple("RequestResponse", ("status", "content", "headers"))

log = logging.getLogger("apitest")


async def _coro_make_request(*,
                             endpoint: APITestEndPoint,
                             proxy: ProxyConfig = None,
                             download_content: bool = False,
                             accept_selfsigned_certs: bool = True):
    """
    A coroutine that makes the requests
     
    :param endpoint: APITestEndPoint object instance
    :type endpoint: APITestEndPoint
    
    :param proxy: ProxyConfig object instance
    :type proxy: ProxyConfig
    
    :return: the
    :rtype:
    """
    assert isinstance(endpoint, APITestEndPoint)
    assert isinstance(proxy, ProxyConfig)
    
    # Proxy needs authentication?
    proxy_auth = None
    if proxy.user is not None:
        proxy_auth = aiohttp.BasicAuth(proxy.user, proxy.password)
    
    # Extract info
    url = endpoint.request.url
    body = transform_apitest_body_to_queryable(endpoint.request.body)
    method = endpoint.request.method
    headers = {header.key: header.value for header in endpoint.request.headers}

    # Check SSL?
    conn = None
    if accept_selfsigned_certs:
        conn = aiohttp.TCPConnector(verify_ssl=False)
    
    # Do the Requests
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.request(method=method,
                                   url=url,
                                   headers=headers,
                                   data=body,
                                   proxy=proxy.url,
                                   proxy_auth=proxy_auth) as resp:
            
            if resp.status == 200:
                log.console("    - Response OK for URL: '{}'".format(url))
            else:
                log.console("    - Non-200 response for URL: '{}'".format(url))
                log.console("      \_ HTTP status code: '{}'".format(resp.status))
                
            # Download content?
            content = None
            if download_content:
                content = await resp.text()
                log.console("      \_{}".format(content))

            return RequestResponse(status=resp.status,
                                   content=content,
                                   headers=resp.headers)


def make_request(*, endpoint: APITestEndPoint, proxy: ProxyConfig = None):
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(_coro_make_request(endpoint=endpoint,
                                               proxy=proxy))


def make_all_requests(*, apitest_obj: APITest, proxy: ProxyConfig = None):
    
    loop = asyncio.get_event_loop()
    
    tasks = []
    
    for collections in apitest_obj.collections:
        for endpoint in collections.end_points:
            tasks.append(_coro_make_request(endpoint=endpoint, proxy=proxy))
    
    loop.run_until_complete(asyncio.wait(tasks))


__all__ = ("make_request", "make_all_requests", "ProxyConfig")
