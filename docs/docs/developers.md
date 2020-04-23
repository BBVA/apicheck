---
layout: doc
title: Building new tools
permalink: /docs/building-new-tools
---

<a id="why-create-new-a-tool"></a>
# Why create a new tool

APICheck is a tool set that working together can be used for many different results.

APICheck not only integrates self-developed tools, it's can also integrate existing tools into their ecosystem to take the advantage of the rest of tools.

You may want to add a new cool tool (self-developed or already existing) to the tool set. If you're at this point this is the document you need to read.

<a id="tools-philosophy"></a>
# Tools philosophy

## Tools packaging

Each tool of APICheck is a packaged Docker Image. This mind that a tools is really a *black box* that receive some information from the standard input and put the results in the standard outputs: console output and console error.

Inside the Docker Image the developer are free to install or add any tool they think it's necessary.

## Meta information

Once the logic of a tool is inside packaged, it's necessary to provide some information that helps users to know what our tools does. Needed information are things like:

- tool nane
- version
- description
- ...

## Automating the integration of new tools

APICheck was developed following automation mechanism. Each time a tool developer add or modify something in any tool, building process will be raised and build releases the new version for the tool.  

<a id="what-do-you-need"></a>
<a id="steps-for-creating-a-new-tool"></a>
# Steps for creating a new tool

Well, if you're here this mind that you're interested in how to create a new tool. You must follow these steps:

## Steps summary:

In summary we'll need to do these things:

1. Fork APICheck repo
2. Clone forked repo
3. Creates a new folder in */tools* directory.
4. Add files: META, README.md and Dockerfile
5. Push the repo to our account in Github
6. Send us a Pull Request

## Step 1 - fork Github repo

This step don't need more explanation :)

## Step 2 - clone your forked repo

```console
$ git clone https://github.com/[YOUR-GITHUB-USER]/apicheck 
```

It was the easy part :)

## Step 3 - create a the tool folder

APICheck tools are inside */tools* folder. Each tool has their own folder. 

Folders names can contain: numbers, letters and "_" or "-".

Then, we create a new folder for your tool:

```console
$ cd tools/
$ mkdir hello-world-tool
```

## Step 4 - Include Meta information

Meta information is contained in a file called *META*. Format of this file is a key, value with a "=" symbol.

You must include **all** of these fields for a valid META file:

- *name*: tools name. This name will be used for catalog, Docker image and for installing the tool. **Must be unique**.
- *short-command* (optional): some times tool name is too long. short command is easy to typing alias. when you'r tool was intalled by the package-manage, it will creates 2 commands name. One of them will be the name of the tool and the other command will be a short command for the tool. **Must be unique**. 
- *version*: version of the tool. It's recommendable to follow semantic format, but you're free to put use you're version format
- *description*: a description of your tool. Try to be descriptive. There's not limit for description long, but we recommend not more than 150 characters.
- *home*: author can include a link of the tool home, their profile os something else. This field is open.
- *author*: author name or team

You must put the *META* file in the root of the folder we just created for our tool:

```console
$ cd tools/
$ cd hello-world-tool/
$ cat META
name = hello-world-tool
short-command = ac-hwt
version = 1.0.0
description = All good tutorials must include a Hello World example! :) 
home = https://github.com/BBVA/apicheck
author = BBVA Labs Security
```

## Step 5 - Include tool documentation

Each tool must include their own documentation file. This is very important part of your tool. 

Documentation must be write in Markdown format. It must be included in the root of your folder tool and must be called **README.md**:

```console
$ cd tools/
$ cd hello-world-tool/
$ cat README.md
# Hello Word Tool Documentation

Wellcome to the demo tool of APICheck tutorial

## How to install
....
```

:warning: Be careful with the name of file, the name must be in upper case and the extension in lower case.

## Step 6 - Include the Dockefile

As we said a tool will be packed as a Docker Image, so we need a Dockerfile.

You can write the Dockerfile you need to package your tool but if you minimize the resulting Docker Image will be useful for users.

```console
$ cd tools/
$ cd hello-world-tool/
$ cat Dockerfile
FROM python:3.8-alpine

RUN apk update \
    && apk add --no-cache build-base
...
```

## Step 7 - Push your new plugin to Github

At this point we only need to commit and push the new plugin to Github:

```console
$ git add tools/hello-world-tool/
$ git commit -am "my first APICheck tool!"
$ git push
``` 

### Step 8 - Send us a Pull Request

Only "click" in the "New pull request" button at Github:

![Send us a Pull Request](/apicheck/assets/images/doc_develop_pull_request.png)


<a id="tool-scaffolding"></a>

<a id="faq"></a>
# F.A.Q.

## I need to develop in a specific language?

Absolutely no! You can develop in your favorite code language. Some member os the APICheck team loves Bash and some tools was integrade without codding any line.

Have in mind that each tool are packaged in a Docker Image. Inside this Docker Image you're the king/Queen. You can install all you need to build your tools. 

## Is there any good practice for building tools?

- Build small docker images as you can
- Don't use tool name that already exits as part of APICheck ecosystem 

## I updated my tool, but no new release was published

As the building process is automated it only raises if you modify something at the *META* file. 

If you're releasing a new tool version, be sure you update the version number in *META* file. 