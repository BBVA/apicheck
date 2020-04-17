---
layout: doc
title: Send to proxy
permalink: /tools/send-to-proxy
---

# Send to proxy

This tool send stdin request to a remote proxy.

## Install

### Generic

```bash
> ./INSTALL
```

### Python mode


```bash
> python setup.py install
```

## Usage

### Getting help

After install you can type this to use:

```bash
> ac-sentoproxy -h
```

### Usage example

```bash
> cat examples/valid-request.json | ac-sendtoproxy -q http://127.0.0.1:9999
```