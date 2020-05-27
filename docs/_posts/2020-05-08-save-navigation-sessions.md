---
layout: post
author: cr0hn
author_link: https://twitter.com/ggdaniel
title: "Saving navigation session"
---

Sometimes, you need to store a navigation session in a simple but standard format. [APICheck proxy](https://bbva.github.io/apicheck/tools/apicheck/apicheck-proxy) intercepts your navigation traffic and outputs it to the console. Then, you only need to redirect it to a file.
<!--more-->

```bash
docker run --rm -it -p 8080:8080 -e APICHECK_PROXY_ALLOWED_HOST=cr0hn.com bbvalabs/apicheck-proxy >> sessions.data
```

Proxy listens in HTTP port 8080. Then we only need to configure our browser to use it:

![Firefox Proxy](https://i.ibb.co/2kPCKTT/Preferencias-firefox.png)

You can check that `sessions.data` file contains a one-per-line [APICheck Data Objects](https://bbva.github.io/apicheck/docs/building-new-tools#apicheck-data-format) like JSON objects.

```json
{"request": {"url": "https://cr0hn.com:443/", "method": "GET", "version": "HTTP/2.0", "headers": {":authority": "cr0hn.com", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "accept-language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3", "accept-encoding": "gzip, deflate", "dnt": "1", "upgrade-insecure-requests": "1", "pragma": "no-cache", "cache-control": "no-cache", "te": "trailers", "cookie": "_ga=GA1.2.909075303.1551881907; _hjIncludedInSample=1; __cfduid=da5cc0bbb2c60d20283d8a844b37faff21589884526; _hjid=01db2950-2118-413a-9f47-77fd8b7478b7; _gid=GA1.2.1142604146.1590064671"}, "body": ""}, "response": {"status": 200, "reason": "", "headers": {"date": "Thu, 21 May 2020 13:12:08 GMT", "content-type": "text/html; charset=UTF-8", "vary": "Accept-Encoding", "x-powered-by": "ASP.NET 4.8", "link": "<https://cr0hn.com/>; rel=shortlink", "cf-cache-status": "DYNAMIC", "expect-ct": "max-age=604800, report-uri=\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\"", "server": "cloudflare", "cf-ray": "596e8c1aed73ff48-MAD", "content-encoding": "gzip", "cf-request-id": "02d8f5e4ce0000ff48233d6200000001"}, "body": "..."}}
{"request": {"url": "https://cr0hn.com:443/wp-includes/css/dist/block-library/style.min.css", "method": "GET", "version": "HTTP/2.0", "headers": {":authority": "cr0hn.com", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0", "accept": "text/css,*/*;q=0.1", "accept-language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3", "accept-encoding": "gzip, deflate", "dnt": "1", "referer": "https://cr0hn.com/", "pragma": "no-cache", "cache-control": "no-cache", "te": "trailers", "cookie": "_ga=GA1.2.909075303.1551881907; _hjIncludedInSample=1; __cfduid=da5cc0bbb2c60d20283d8a844b37faff21589884526; _hjid=01db2950-2118-413a-9f47-77fd8b7478b7; _gid=GA1.2.1142604146.1590064671"}, "body": ""}, "response": {"status": 200, "reason": "", "headers": {"date": "Thu, 21 May 2020 13:12:09 GMT", "content-type": "text/css", "last-modified": "Sat, 30 Nov 2019 09:30:02 GMT", "vary": "Accept-Encoding", "etag": "W/\"5de2369a-a1fb\"", "x-powered-by": "ASP.NET 4.8", "expires": "Sun, 16 May 2021 12:16:20 GMT", "cache-control": "public, max-age=31536000", "content-encoding": "gzip", "cf-cache-status": "HIT", "age": "182199", "expect-ct": "max-age=604800, report-uri=\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\"", "server": "cloudflare", "cf-ray": "596e8c22aa86ff48-MAD", "cf-request-id": "02d8f5e9ab0000ff4823031200000001"}, "body": "...."}}
...
```
