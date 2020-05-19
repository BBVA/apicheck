# APICheck Proxy

This tool launches a local proxy.

**Tool type**: generator

## Tool description

APICheck Proxy tool runs the popular `MITM Proxy` under the hoods with a custom
*addon* to add APICheck functionality.

## Quick start

```console
$ docker run --rm -p 8080:8080 -it bbvalabs/apicheck-proxy
Loading script /addons/apicheck_addon.py
Proxy server listening at http://*:8080
```
