---
layout: doc
title: APICheck Proxy
permalink: /tools/apicheck-proxy
---

# APICheck Proxy

With `APICheck proxy` launch a local proxy.

**Tool type**: generator

## Tool description

APICheck Proxy tool under the hoods runs the popular `MITM Proxy` with a custom *addon* to add APICheck functionality.



## Quick start

```console
$ docker run --rm -p 8080:8080 -it bbvalabs/apicheck-proxy
Loading script /addons/apicheck_addon.py
Proxy server listening at http://*:8080
```