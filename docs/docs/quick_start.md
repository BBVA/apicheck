---
layout: doc
title: Quick Start
permalink: /docs/quick-start
---

<a id="requirements"></a>
# Requirements

APICheck, under the hoods, runs inside Docker. So you must be installed Docker to run it. 

Although you can run APICheck tools by running each Docker Image We'll recommend use the **APICheck Package Manager**. This document will explain how to run APICheck by them. 

<a id="installation"></a>
# Installation

To install package manager you need Python >= 3.5. Then installation is easy.

```console
$ pip install apicheck-package-manager
``` 

<a id="the-first-run"></a>
# The First Run

The package manager runs after installation by the command *acp*.

```console
$ acp
[!] Invalid action name

usage: acp [-h] [-H DOCKER_HOST] {list,info,install,activate,describe,envs,version} ...

APICheck Manager

positional arguments:
  {list,info,install,activate,describe,envs,version}
                        available actions
    list                search in A
    info                show expanded tool info
    install             install an APICheck tool
    activate            activate an environment
    describe            show info of environment
    envs                show available environments
    version             displays version

optional arguments:
  -h, --help            show this help message and exit
  -H DOCKER_HOST, --docker-host DOCKER_HOST
                        docker url. default: tcp://127.0.0.1:2375
``` 

## Listing available tools 

As any other package manager, you can list available tools, install an so on. 

For listing available tools in APICheck repository you can run:

```console
$ acp list
+--------------------------------------------------+
| Name           | Version                         |
+--------------------------------------------------+
| replay         | 1.0.0                           |
+--------------------------------------------------+
| sensitive-json | 1.0.0                           |
+--------------------------------------------------+
| send-to-proxy  | 1.0.0                           |
+--------------------------------------------------+
````
If you want more info about some tool you can run:

```console
$ acp info sensitive-json
+---------------------------------------------------------------------------+
| Tool name 'sensitive-json'                                                |
+---------------------------------------------------------------------------+
| name                       | sensitive-json                               |
+---------------------------------------------------------------------------+
| short-command              | asej                                         |
+---------------------------------------------------------------------------+
| version                    | 1.0.0                                        |
+---------------------------------------------------------------------------+
| description                | Find sensitive data in JSON content in HTTP  |
|                            | / Response                                   |
+---------------------------------------------------------------------------+
| home                       | https://github.com/BBVA/apicheck             |
+---------------------------------------------------------------------------+
| author                     | BBVA Labs Security                           |
+---------------------------------------------------------------------------+
```

## Installing a new tool

The tool installing process, under the hoods, does the follows:

1. Download tool Docker Image
2. Register installed tool
3. Create environment with alias

As example will install *sensitive-json* tool:

```console
$ acp install sensitive-json
[*] Fetching Docker image for tool 'sensitive-json'

    Using default tag: latest
    latest: Pulling from bbvalabs/sensitive-json
    aad63a933944: Already exists
    f229563217f5: Already exists
    d999dd4b9386: Already exists
    d40444ccd481: Already exists
    d7d60c647873: Already exists
    3912dac2b2dd: Already exists
    d516a946534e: Already exists
    60a000e25e76: Already exists
    625097242e3f: Pulling fs layer
    a80b3111c615: Pulling fs layer
    8b22d3755c28: Pulling fs layer
    3d69e0c89189: Pulling fs layer
    3d69e0c89189: Waiting
    a80b3111c615: Verifying Checksum
    a80b3111c615: Download complete
    8b22d3755c28: Verifying Checksum
    8b22d3755c28: Download complete
    625097242e3f: Verifying Checksum
    625097242e3f: Download complete
    625097242e3f: Pull complete
    a80b3111c615: Pull complete
    3d69e0c89189: Verifying Checksum
    3d69e0c89189: Download complete
    8b22d3755c28: Pull complete
    3d69e0c89189: Pull complete
    Digest: sha256:0455f43f6032eaaad8c40a2681ffe83ec259e710ade45f6271fdcc4c4ca9adc6
    Status: Downloaded newer image for bbvalabs/sensitive-json:latest
    docker.io/bbvalabs/sensitive-json:latest

[*] filling environment alias file
```

<a id="apicheck-environments"></a>
# APICheck environments 

Depending of tests you're doing probability you may want to use different tools and **different version** of them.

APICheck work with the concept of **environments**. An environment can contain a custom list of tools installed and you can *activate* or *move* between different environments.

## List environments

You can list available environments typing: 

```console
$ acp envs
+------------------------------------------------------------+
| Environment Name | Number of installed tools               |
+------------------------------------------------------------+
| default          | 1                                       |
+------------------------------------------------------------+
```  

&#9888; The environment *default* is activated if not other choice was indicated.

## Environments content

You can check tools installed in an environment doing:

```console
$ acp describe
```
+------------------------------------------------------------+
| Environment | default                                      |
+------------------------------------------------------------+
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
+------------------------------------------------------------+
| Tool name      | Version                                   |
+------------------------------------------------------------+
| sensitive-json | 1.0.0                                     |
+------------------------------------------------------------+

&#9888; If not environment is passed as parameter, default envs will be listed

## Activating an environment

Enter in an environment means that all the tools installed will be available as regular commands. 

To activate an environment you must type:

```console
$ eval $(acp activate)
(APICheck) $ 
``` 

For exit of environment:

```console
(APICheck) $ deactivate
$
```

&#9888; Using eval idea was taken form ![Docker Machine](https://docs.docker.com/machine/reference/create/#specifying-configuration-options-for-the-created-docker-engine)

<a id="running-tools"></a>
# Running tools

Once you're in a environment you can run tool (finally!).

Remember that for this *Quickstart* document we were installed *sensitive-json* tool. So we'll available the command: **sensitive-json**:

```console
(APICheck) $ sensitive-json -h
usage: __main__.py [-h] [-F IGNORE_FILE] [-i IGNORE_RULE] [-r RULES_FILE]
                   [-o OUTPUT_FILE] [-q] [--server SERVER]

Analyze a HTTP Request / Response for sensitive data

optional arguments:
  -h, --help            show this help message and exit
  -F IGNORE_FILE, --ignore-file IGNORE_FILE
                        file with ignores rules
  -i IGNORE_RULE, --ignore-rule IGNORE_RULE
                        rule to ignore
  -r RULES_FILE, --rules-file RULES_FILE
                        rules file. One rule ID per line
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file path
  -q, --quiet           quiet mode
  --server SERVER       launch a as server mode at localhost:8000
```

Remember that some tools also have short-commands (you can check it with *acp info* command). You also can run it if you want short version of command:

```console
(APICheck) $ asej -h
usage: __main__.py [-h] [-F IGNORE_FILE] [-i IGNORE_RULE] [-r RULES_FILE]
                   [-o OUTPUT_FILE] [-q] [--server SERVER]

Analyze a HTTP Request / Response for sensitive data

optional arguments:
  -h, --help            show this help message and exit
  -F IGNORE_FILE, --ignore-file IGNORE_FILE
                        file with ignores rules
  -i IGNORE_RULE, --ignore-rule IGNORE_RULE
                        rule to ignore
  -r RULES_FILE, --rules-file RULES_FILE
                        rules file. One rule ID per line
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file path
  -q, --quiet           quiet mode
  --server SERVER       launch a as server mode at localhost:8000
```

For usage of each tool, you can check their documentation at ![APICheck documentation](https://bbva.github.io/apicheck/docs).

<a id="tools-and-pipelines"></a>

<a id="tools-and-pipelines"></a>
# Tools & Pipelines

The power of APICheck is the capability to chain tools by using UNIX-like pipelines.

For this example we'll use a **.json** file that contains a message (in APICheck format) for a query with sensitive data at the body of the Request (You can find this file at: ![demo .json file](https://github.com/BBVA/apicheck/blob/master/tools/sensitive-json/examples/valid-request-user-password-one-line.json))  

```console
(APICheck) $ cat demo-request.json | asej
[{"where": "request", "path": "/", "keyOrValue": "key", "sensitiveData": "password"}, {"where": "response", "path": "/", "keyOrValue": "key", "sensitiveData": "password"}]  
```
