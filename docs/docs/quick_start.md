---
layout: doc
title: Quick Start
permalink: /docs/quick-start
---

<a id="requirements"></a>
# Requirements

APICheck relies heavily on Docker, so you must have the Docker daemon installed
in order to use it.

Although you can run APICheck tools by directly pulling and running each Docker
image, We recommend that you use the ***APICheck Package Manager***. This
document will explain how to use it to run APICheck.

<a id="installation"></a>
# Installation

*Package Manager* needs Python >= 3.5 installed. To install it just type in
your console:

```bash
pip install apicheck-package-manager
```

<a id="add-config-to-path"></a>
# Add APICheck config to PATH

You need to include `APICheck` binary path to your global `$PATH` var. So, add this line to your shell profile:

```bash
export PATH="$HOME/.apicheck_manager/bin:$PATH"
```

<a id="the-first-run"></a>

# The First Run

Once installed, you can run the *Package Manager* by using the command *acp*.

```console
$ acp
[!] Invalid action name

usage: acp [-h] [-w] {list,info,install,version} ...

APICheck Manager

positional arguments:
  {list,info,install,version}
                        available actions
    list                search in A
    info                show expanded tool info
    install             install an APICheck tool
    version             displays version

optional arguments:
  -h, --help            show this help message and exit
  -w, --disable-warning
                        disable check of RC Shell File
```

*Package Manager* allows you to list the available tools, install them and so on.

## Listing available tools

The *list* command shows what are the available tools in the APICheck
repository:

```console
$ acp list
+--------------------------------------------------+
| Name           | Version                         |
+--------------------------------------------------+
| apicheck-proxy | 1.0.2                           |
+--------------------------------------------------+
| jwt-checker    | 1.0.0                           |
+--------------------------------------------------+
| send-to-proxy  | 1.0.2                           |
+--------------------------------------------------+
| acurl          | 1.0.0                           |
+--------------------------------------------------+
| replay         | 1.0.0                           |
+--------------------------------------------------+
| sensitive-data | 1.0.1                           |
+--------------------------------------------------+
| openapiv2-lint | 1.0.0                           |
+--------------------------------------------------+
| openapiv3-lint | 1.0.0                           |
+--------------------------------------------------+
````

To get more info about any tool, use the *info* command:

```console
$ acp info sensitive-data

+---------------------------------------------------------------------------+
| Tool name 'sensitive-data'                                                |
+---------------------------------------------------------------------------+
| name                       | sensitive-data                               |
+---------------------------------------------------------------------------+
| display-name               | Sensitive data detector                      |
+---------------------------------------------------------------------------+
| version                    | 1.0.1                                        |
+---------------------------------------------------------------------------+
| description                | Find sensitive data in HTTP Request /        |
|                            | / Headers                                    |
+---------------------------------------------------------------------------+
| home                       | https://github.com/BBVA/apicheck             |
+---------------------------------------------------------------------------+
| author                     | BBVA Labs Security                           |
+---------------------------------------------------------------------------+
| type                       | apicheck                                     |
+---------------------------------------------------------------------------+
```

## Installing a new tool

`APICheck` uses Docker under the hoods. So when to install a new tool, Docker image fetch will be displayed.

```console
$ acp install sensitive-data
[*] Creating path for storing apicheck tools at : /Users/Dani/.apicheck_manager/bin
[*] Fetching Docker image for tool 'sensitive-data'

    1.0.1: Pulling from bbvalabs/sensitive-data
    cbdbe7a5bc2a: Already exists
    26ebcd19a4e3: Already exists
    a29d43ca1bb4: Pulling fs layer
    979dbbcf63e0: Pulling fs layer
    30beed04940c: Pulling fs layer
    7ac3561504a8: Pulling fs layer
    3619e044d33d: Pulling fs layer
    d3c293fd2442: Pulling fs layer
    d0feb92e4bbc: Pulling fs layer
    7ac3561504a8: Waiting
    3619e044d33d: Waiting
    d3c293fd2442: Waiting
    d0feb92e4bbc: Waiting
    979dbbcf63e0: Verifying Checksum
    979dbbcf63e0: Download complete
    30beed04940c: Verifying Checksum
    30beed04940c: Download complete
    7ac3561504a8: Verifying Checksum
    7ac3561504a8: Download complete
    a29d43ca1bb4: Verifying Checksum
    a29d43ca1bb4: Download complete
    d0feb92e4bbc: Verifying Checksum
    d0feb92e4bbc: Download complete
    d3c293fd2442: Verifying Checksum
    d3c293fd2442: Download complete
    3619e044d33d: Verifying Checksum
    3619e044d33d: Download complete
    a29d43ca1bb4: Pull complete
    979dbbcf63e0: Pull complete
    30beed04940c: Pull complete
    7ac3561504a8: Pull complete
    3619e044d33d: Pull complete
    d3c293fd2442: Pull complete
    d0feb92e4bbc: Pull complete
    Digest: sha256:be66ed12618ce5786e7a8d234ddbf0116e466180e02ef5dd75b09c830b6687dc
    Status: Downloaded newer image for bbvalabs/sensitive-data:1.0.1
    docker.io/bbvalabs/sensitive-data:1.0.1

[*] Making launch scripts
[*] Updating configuration file
```

<a id="running-tools"></a>

# Running tools

Once you have installed a tool and added [APICheck binary path](https://bbva.github.io/apicheck/docs/quick-start#add-config-to-path) you will have available a tool command with the name of the tool: 

```console
$ sensitive-data -h
usage: sensitive-data [-h] [-q] [-F IGNORE_FILE] [-i IGNORE_RULE]
                      [-r RULES_FILE] [--server SERVER] [-C] [-D]

Analyze a HTTP Request / Response searching for sensitive data

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           quiet mode
  -F IGNORE_FILE, --ignore-file IGNORE_FILE
                        file with ignores rules
  -i IGNORE_RULE, --ignore-rule IGNORE_RULE
                        rule to ignore
  -r RULES_FILE, --rules-file RULES_FILE
                        rules file. One rule ID per line
  --server SERVER       launch in server mode listening at localhost:8000

Server mode options:
  -C, --show-in-console
                        show results in console
  -D, --dont-check      always returns OK although a rule matches
```

Some tools can have an alias (*short-command*, you can see it with the *acp info*
command), so you can also run the command by using its alias.

APICheck has a repository of tools from which you can download them and access to their documentation in order to get usage information, [APICheck documentation](https://bbva.github.io/apicheck/docs).

<a id="tools-and-pipelines"></a>

# Tools & Pipelines

The power of APICheck resides in its capability of chaining tools by using
*NIX-like pipelines.

In this example we'll use a **.json** file that contains a message (in [APICheck format](https://bbva.github.io/apicheck/docs/building-new-tools#apicheck-data-format)) for searching sensitive data within the body of the Request (You can find this file at [demo .json file](https://raw.githubusercontent.com/BBVA/apicheck/master/tools/sensitive-data/examples/request-password-in-response.json))  

```console
$ cat demo-request.json | sensitive-data

http://my-company.com
---------------------

 > rule           -> core-001
 > where          -> request
 > url            -> http://my-company.com/api/entry-point
 > description    -> Find 'password' keyword in flow data
 > sensitiveData  -> password
```
