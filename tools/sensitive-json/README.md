# APICheck Sensitive JSON

This tool analyzes a Request / Response HTTP and try to find sensitive data.

**Tool type**: action

## Tools description

Some times APIs can return sensitive data in some entry-points. Sensitive data could be user information, some data of bossiness logic, internal IPs or os on.

Detect this data is complicated and depends of the bossiness application logic. So with `APICheck Sensitive JSON` you can configure a set of rules for analyzing the Request / Response of an application.

Rules is a simple `YAML` file that could be hosted in a remote place or in a local.

## Quick start

## Using APICheck Package Manager

Installing `APICheck Package Manager`:

```console
$ pip install apicheck-package-manager
Collecting apicheck-package-manager
  Using cached apicheck_package_manager-0.0.14-py3-none-any.whl (5.7 kB)
Installing collected packages: apicheck-package-manager
Successfully installed apicheck-package-manager-0.0.14
```

Install APICheck tools: 

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

Activate default environment and running the tool:

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

Get Docker images for tools:

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

Rules are an YAML file with this format:

Core rules file: `core.yaml`:

```yaml
- id: core-001
  description: Find plain text password in HTTP responses
  regex: '([pP][aA][sS][sS][wW][oO][rR][dD])'
  severity: Medium
  searchIn: Both  # Allowed values: Response, Request, Both
  includeKeys: true  # Search in Json keys. Values always are inspected
```

- Severity values allowed are: High, Medium, Low
- searchIn: Set if you want to search in HTTP Request, in Response or Both.
- includeKeys: Set if you want to search also in JSON keys.

# Running as Service

`APIcheck Sensitive JSON` can runs as a service. Only Docker mode currently allow to run this way:

```bash
$ docker run --rm -p 9000:9000 bbvalabs/sensitive-json --server 0.0.0.0:9000
[2020-05-08 10:18:01 +0000] [1] [INFO] Goin' Fast @ http://0.0.0.0:9000
[2020-05-08 10:18:01 +0000] [1] [INFO] Starting worker [1]
```

There's only one entry-point: `/apicheck/sensitive-data` and accept HTTP POST method.

POST data is a valid APICheck data object.

Example of calling:

```bash
$ acurl http://myservice.com > query.json
$ curl -X POST -H "Content-Type: application/json" -X POST --d @query.json http://localhost:9000/apicheck/sensitive-data
```

# Examples

## Common examples

This examples could be used when you have been installed by `APICheck Package Manager` or running directly with Docker

### Core rules

By default, the tool has a set of embedded rules: **core rules**. If you omit `-r` parameters, these core rules will be used:

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

### With remote rules

You also can set rules files by remote files. `APICheck Sensitive JSON` will download rules file.

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

Some times rules and alert for issues but it could be a false positive. In these cases we can remove it by using the `rule ID`:

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

You can remove the second rules **myrules2-002** and **core-001** inline:

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

You also can call `APICheck Sensitive JSON` by running manually with Docker:

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

When `APICheck Sensitive JSON` detect an output pipe, it send the a compatible APICheck data to allow to connect with other APICheck tools.

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

In this case is useful the `quiet` param:

```bash
$ apicheck-curl http://my-company.com/api/entry-point | ac-sensitive -q | send-to-proxy http://my-proxy-addr:9000
```
