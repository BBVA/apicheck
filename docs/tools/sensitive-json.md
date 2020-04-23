---
layout: doc
title: APICheck Sensitive Data Finder
permalink: /tools/sensitive-json
---

# APICheck Sensitive Data Finder

## Usage through Kapow!

```bash
> docker build -t ac-sd .
> docker run -p 8080:8080 --rm -d ac-sd
> curl --data-raw '{"password": "sss"}' -v http://localhost:8080/apicheck/sensitive-data
[{"where": "response", "path": "/", "keyOrValue": "key", "sensitiveData": "password"}]
```

## Usage cli

For the following examples *data.json* is a APICheck format file with a Request / Response info.

### With remote rules

```bash
> cat data.json | ac-sensitive -r http://127.0.0.1:9999/rules/rules.yaml
```

### With local rules

Using core rules:

```bash
> cat data.json | ac-sensitive
```

### With many rules files

```bash
> cat data.json | ac-sensitive -r rules/java.yaml -r rules/credentials.yaml
```

### Passing rules by Environment var

```bash
> export RULES=/home/john/rules.yaml
> cat data.json | ac-sensitive -r rules/java.yaml -r rules/credentials.yaml
```

**Environ var must named 'RULES'**

### Export results as json

```bash
> cat data.json | ac-sensitive -o results.json -r rules/java.yaml -r rules/credentials.yaml
```

### Quiet mode

Don't output nothing into console

```bash
> cat data.json | ac-sensitive -q
```

### Filtering false positives

**By ignore file**

Dockerfile-sec allows to ignore rules by using a file that contains the rules you want to ignore.

```bash
> cat data.json | ac-sensitive -F ignore-rules
```

Ignore file format contains the *IDs* of rules you want to ignore. **one ID per line**. Example:

```bash
core-001
core-007
```

**By cli**

You also can use cli to ignore specific *IDs*:

```bash
> cat data.json | ac-sensitive -i core-001,core007
```

### Using as pipeline

You also can use ac-sensitive as UNIX pipeline.

Loading Dockerfile from stdin:

```bash
> cat data.json | ac-sensitive -i core-001,core007
```

Exposing results via pipe:

```bash
> cat data.json | ac-sensitive -i core-001,core007 | jq
```

### Output formats

JSON Output format
++++++++++++++++++

```json
[
  {
    "where": "response",
    "path": "/",
    "keyOrValue": "key",
    "sensitiveData": "password"
  }
]
```