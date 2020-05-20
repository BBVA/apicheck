---
layout: doc
title: Replay
type: apicheck
permalink: /tools/apicheck/replay
---

# Replay

This tool re-sends the requests read from stdin again capturing the new 
responses.

It outputs the same pair but sustituting the old responses with the new ones.
And storing the old request on _meta for further processess.

# Quick start

## Using APICheck Package Manager

Install replay tool:

```bash
$ apc install replay
```

You need an valid request response object as input in json line format. You can
grab it from curl:

```bash
$ eval $(acp activate)
(ApiCheck)$ acurl www.google.com | replay
```

This will generate an output with to responses, the original response made by
curl in _meta/original field; and the new response made by replay in response
field.

## Using Docker

It's very easy, because replay has no paramas. Just replay the request.

```bash
docker run --rm -it bbvalabs/apicheck-curl http://my-company.com/api/entry-point | docker run -i --rm bbvalabs/replay
```
