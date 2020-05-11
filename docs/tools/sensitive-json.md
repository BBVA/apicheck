---
layout: doc
title: APICheck Sensitive JSON
permalink: /tools/sensitive-json
---

# APICheck Sensitive JSON

This tool analyzes a Request / Response object and tries to find sensitive data
in both the request and the response.

**Tool type**: action

## Tool description

Some times APIs can return sensitive data for some entry-points. Sensitive data
could be user information, some data of business logic, internal IPs or os on.

Detect this data is a hard task as it depends of the business application logic.
With `APICheck Sensitive JSON` you can configure a set of rules for analyzing
the Request / Response object of an application.

Rules are provided in a simple `YAML` file that could be hosted in a remote
place or in local filesystem.

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

then install the APICheck tools:

- sensitive-json
- apicheck-curl

```bash
$ acp install sensitive-json
[*] Fetching Docker image for tool 'sensitive-json'

    Using default tag: latest
    latest: Pulling from bbvalabs/sensitive-json
    cbdbe7a5bc2a: Already exists
    26ebcd19a4e3: Already exists
    35acdcbeccf1: Already exists
    ...
    Status: Downloaded newer image for bbvalabs/sensitive-json:latest
    docker.io/bbvalabs/sensitive-json:latest

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

Finally activate default environment and run the tools:

```bash
$ eval $(acp activate)
(APICheck) $ acurl http://my-company.com/api/entry-point | sensitive-json

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

## Using Docker

Pull the Docker images for the tools:

- sensitive-json
- apicheck-curl

```bash
$ docker pull bbvalabs/sensitive-json
Using default tag: latest
latest: Pulling from bbvalabs/sensitive-json
cbdbe7a5bc2a: Already exists
26ebcd19a4e3: Already exists
...
Status: Image is up to date for bbvalabs/sensitive-json:latest
docker.io/bbvalabs/sensitive-json:latest

$ docker pull bbvalabs/apicheck-curl
Using default tag: latest
latest: Pulling from bbvalabs/apicheck-curl
cbdbe7a5bc2a: Already exists
26ebcd19a4e3: Already exists
35acdcbeccf1: Already exists
...
Status: Downloaded newer image for bbvalabs/apicheck-curl:latest
docker.io/bbvalabs/apicheck-curl:latest
```

Running launching Docker:

```console

$ docker run --rm -i bbvalabs/apicheck-curl http://my-company.com/api/entry-point | docker run --rm -i bbvalabs/sensitive-json

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

# Rules format

Rules are provided in a YAML file with the following format:

```yaml
- id: core-001
  description: Find plain text password in HTTP responses
  regex: '([pP][aA][sS][sS][wW][oO][rR][dD])'
  severity: Medium
  searchIn: Both  # Allowed values: Response, Request, Both
  includeKeys: true  # Search in Json keys. Values always are inspected
```

The above example is from the core rules file: `core.yaml`:

- Severity values allowed are: High, Medium, Low
- searchIn: Allows to search in the HTTP Request, in the Response or in Both.
- includeKeys: Set if you want to search also in JSON keys.

# Running as Service

`APIcheck Sensitive JSON` can be run as a service, but only when running as a
standalone docker container

```bash
$ docker run --rm -p 9000:9000 bbvalabs/sensitive-json --server 0.0.0.0:9000
[2020-05-08 10:18:01 +0000] [1] [INFO] Goin' Fast @ http://0.0.0.0:9000
[2020-05-08 10:18:01 +0000] [1] [INFO] Starting worker [1]
```

It provides only one entry-point (`/apicheck/sensitive-data`) that can be
accessed by using the HTTP POST method.

POST data must be a valid APICheck data object.

Example:

```bash
$ acurl http://myservice.com > query.json
$ curl -X POST -H "Content-Type: application/json" -X POST --d @query.json http://localhost:9000/apicheck/sensitive-data
```

# Examples

## Common examples

You can run this examples by using both the `APICheck Package Manager` or
directly with Docker.

### Core rules

By default, the tool has a set of embedded rules: **core rules**. Unless you
provide a rules file by the use of the `-r` parameter, these core rules will be
used:

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

### With a remote rules file

You can also use rules stored remote files, `APICheck Sensitive JSON` will
download the rules file prior to execution.

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive -r http://127.0.0.1:9999/rules/rules.yaml

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> myrules-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

### With many rules files

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive -r http://127.0.0.1:9999/rules/java.yaml -r http://127.0.0.1:9999/rules/credentials.yaml

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> java-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

### Filtering false positives

Some times rules generate false positives, in these cases we can remove them by
using the `-i` parameter and a comma separated list of `rule ID` or by
providing an ignore file, containing one `rule ID` by line, with the `-F`:

For the example:

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive -r http://127.0.0.1:9999/rules/rules2.yaml

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> myrules2-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> value
 > sensitiveData  -> creditcard

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> myrules2-002
 > where          -> response
 > path           -> /
 > keyOrValue     -> value
 > sensitiveData  -> other-password

```

If you want to remove the errors generated by **myrules2-002** and **core-001**
rules you can do so with the `-i` parameter:

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive -r http://127.0.0.1:9999/rules/rules2.yaml -i core-001,myrules2-002

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

Or using a ignore file:

```bash
$ cat ignore-file
core-001
myrules2-002
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive -r http://127.0.0.1:9999/rules/rules2.yaml -F ignore-file

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

## Running with Docker

You can also use `APICheck Sensitive JSON` by running by hand with Docker:

### Running without parameters

```console

$ apicheck-curl http://my-company.com/api/entry-point | docker run --rm -i bbvalabs/sensitive-json

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

### Running with parameters

```console

$ apicheck-curl http://my-company.com/api/entry-point | docker run --rm -i bbvalabs/sensitive-json -r http://127.0.0.1:9999/rules/credentials.yaml

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> credentials-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

### Defining rules in env vars

```console

$ apicheck-curl http://my-company.com/api/entry-point | docker run --rm -i -e RULES=/home/john/rules.yaml bbvalabs/sensitive-json

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> john-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password

```

## Mixing with other APICheck tools

When `APICheck Sensitive JSON` detects an output pipe, it writes a compatible APICheck output data to allow the connection with other APICheck tools.

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive | send-to-proxy http://my-proxy-addr:9000

http://my-company.com/api/entry-point
-------------------------------------

 > rule           -> core-001
 > where          -> request
 > path           -> /
 > keyOrValue     -> key
 > sensitiveData  -> password
```

In this case is useful the `-quiet` flag:

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive -q | send-to-proxy http://my-proxy-addr:9000
```
