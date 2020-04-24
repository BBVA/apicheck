---
layout: doc
title: Quick Start
permalink: /docs/quick-start
---

<a id="requirements"></a>
# Requirements

APICheck, under the hoods, runs inside Docker. So you must have the Docker
daemon installed to run it.

Although you can run APICheck tools by directly downloading and running each
Docker image, We recommend you to use the ***APICheck Package Manager***. This
document will explain how to use it to run APICheck.

<a id="installation"></a>
# Installation

*Package Manager* needs Python >= 3.5 installed. To install it just type in
your console:

```console
$ pip install apicheck-package-manager
```

<a id="the-first-run"></a>
# The First Run

Once installed you can run the *Package Manager* by using the command *acp*.

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

*Package Manager* allows you to list available tools, install them and so on.

## Listing available tools

In order to list all available tools in APICheck repository you can run the list
subcommand:

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
If you want more info about some tool use the info subcommand:

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

In order to use a tool you have to install it by using the install subcommand.
Under the hoods, the installation process is as follows:

1. Download the Docker image
2. Register the tool in the environment
3. Create the alias

As an example, this is how you can install *sensitive-json* tool:

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

Depending on the projects you're working on, probably you may want to use
different tools and, even, *different versions* of those tools. In order to help
coping with this scenarios APICheck has the concept of *Environments*.

An environment contains its own set of tools installed, and you can *activate*
(move) between the existing environments.

## List environments

You can list available environments with the *envs* subcommand:

```console
$ acp envs
+------------------------------------------------------------+
| Environment Name | Number of installed tools               |
+------------------------------------------------------------+
| default          | 1                                       |
+------------------------------------------------------------+
```  

&#9888; The *default* environment always exist and it is activated by default.

## Activating an environment

Activating an environment means that you can use all the installed tools will
as regular commands. To activate an environment use the activate subcommand:

```console
$ eval $(acp activate myenvironment)
(APICheck) $
```

If you want to leave the environment use the deactivate subcommand:

```console
(APICheck) $ deactivate myenvironment
$
```

&#9888; The idea of using *eval* idea was taken from [Docker Machine](https://docs.docker.com/machine/reference/create#specifying-configuration-options-for-the-created-docker-engine)

## Environments content

In order to know the tools currently installed iin the environment use the
describe subcommand:

```console
$ acp describe

+------------------------------------------------------------+
| Environment | default                                      |
+------------------------------------------------------------+
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
+------------------------------------------------------------+
| Tool name      | Version                                   |
+------------------------------------------------------------+
| sensitive-json | 1.0.0                                     |
+------------------------------------------------------------+
```

&#9888; If no environment is given to the command, the *default* environment
will be used.

<a id="running-tools"></a>
# Running tools

Once you're in an active environment you can run the tools you need (finally!).

Remember that for this *Quickstart* document we have installed the
*sensitive-json* tool, that it is available as the command: ***sensitive-json***:

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

Some tools can have alias (*short-command*, you can check it with the *acp info* command), so you can also run them by using their alias:

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

For getting usage information about tools, you can check their documentation at [APICheck documentation](https://bbva.github.io/apicheck/docs).

<a id="tools-and-pipelines"></a>

<a id="tools-and-pipelines"></a>
# Tools & Pipelines

The power of APICheck resides in its capability of chaining tools by using
UNIX-like pipelines.

In this example we'll use a **.json** file that contains a message (in [APICheck format](/docs/developers)) for a query with sensitive data at the body of the Request (You can find this file at: [demo .json file](https://github.com/BBVA/apicheck/blob/master/tools/sensitive-json/examples/valid-request-user-password-one-line.json))  

```console
(APICheck) $ cat demo-request.json | asej
[{"where": "request", "path": "/", "keyOrValue": "key", "sensitiveData": "password"}, {"where": "response", "path": "/", "keyOrValue": "key", "sensitiveData": "password"}]  
```
