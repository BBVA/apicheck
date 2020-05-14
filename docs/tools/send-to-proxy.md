---
layout: doc
title: APICheck Send to proxy
type: apicheck
permalink: /tools/apicheck/send-to-proxy
---

# APICheck Send to proxy

This tool sends the APICheck Request to a remote proxy.

**Tool type**: generator


## Quick start

## Using APICheck Package Manager

First install `APICheck Package Manager`:

```console
$ pip install apicheck-package-manager
Collecting apicheck-package-manager
  Using cached apicheck_package_manager-0.0.14-py3-none-any.whl (5.7 kB)
Installing collected packages: apicheck-package-manager
Successfully installed apicheck-package-manager-0.0.14
```

Then install the APICheck tools:

- send-to-proxy
- apicheck-curl

```bash
$ acp install send-to-proxy
[*] Fetching Docker image for tool 'send-to-proxy'

    Using default tag: latest
    latest: Pulling from bbvalabs/send-to-proxy
    cbdbe7a5bc2a: Already exists
    26ebcd19a4e3: Already exists
    35acdcbeccf1: Already exists
    ...
    Status: Downloaded newer image for bbvalabs/send-to-proxy:latest
    docker.io/bbvalabs/send-to-proxy:latest

[*] filling environment alias file

$ acp install apicheck-curl
[*] Fetching Docker image for tool 'apicheck-curl'

    Using default tag: latest
    latest: Pulling from bbvalabs/apicheck-curl
    cbdbe7a5bc2a: Already exists
    26ebcd19a4e3: Already exists
    35acdcbeccf1: Already exists
    ...
    Status: Downloaded newer image for bbvalabs/apicheck-curl:latest
    docker.io/bbvalabs/apicheck-curl:latest

[*] filling environment alias file
```

Finally activate default environment and running the tool:

```bash
$ eval $(acp activate)
(APICheck) $ acurl http://my-company.com/api/entry-point | send-to-proxy http://localproxy:9000
[*] Request sent: 'http://my-company.com/api/entry-point'
```

## Using Docker

Pull the Docker images for the tools:

- sensitive-json
- apicheck-curl

```bash
$ docker pull bbvalabs/send-to-proxy
Using default tag: latest
latest: Pulling from bbvalabs/send-to-proxy
cbdbe7a5bc2a: Already exists
26ebcd19a4e3: Already exists
...
Status: Image is up to date for bbvalabs/send-to-proxy:latest
docker.io/bbvalabs/send-to-proxy:latest

$ docker pull bbvalabs/apicheck-curl
Using default tag: latest
latest: Pulling from bbvalabs/apicheck-curl
cbdbe7a5bc2a: Already exists
26ebcd19a4e3: Already exists
35acdcbeccf1: Already exists
...
Status: Downloaded newer image for bbvalabs/apicheck-curl:latest
docker.io/bbvalabs/send-to-proxy:latest
```

And then launch the Docker containers:

```console

$ docker run --rm -i bbvalabs/apicheck-curl http://my-company.com/api/entry-point | docker run --rm -i bbvalabs/send-to-proxy http://localproxy:9000
[*] Request sent: 'http://my-company.com/api/entry-point'
```

## Using the quiet mode

`Send-to-proxy` accepts a parameter containing the URL of the proxy to send requests to and the `-q` (`--quiet`) option to supress output data.

```bash
(APICheck) $ acurl http://my-company.com/api/entry-point | send-to-proxy -q http://localproxy:9000
```
