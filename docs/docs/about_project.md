---
layout: doc
title: About APICheck project
permalink: /docs/about-project
---

# What's APICheck

`APICheck` is a complete toolset designed and created for testing REST APIs.

# Why another REST APIs tool?

APICheck aims to be a universal toolset for testing REST APIs, allowing you to
mix and match the tools it provides, while allowing interoperability with third
party tools. This way we hope that it will be useful to a wide spectrum of
users that need to deal with REST APIs.

# Who is APICheck for?

APICheck focuses not only in the security testing and hacking use cases, the
goal of the project is to become a complete toolset for DevSecOps cycles. The
tools are aimed to different users profiles:

- Developers
- System Administrators
- Security Engineers & Penetration Testers

# Pipelines & data flow

## Pipelines

In *NIX, you can chain multiple commands together in a pipeline. Consider this one:

![Pipeline model](/apicheck/assets/images/apicheck_unix_pipeline.png)

In a similar way you can build *APICheck* pipelines by chaining the different
tools.

## Data format

To allow interoperability among commands and tools, all of them share a common
JSON data format. In other words, *APICheck* commands output JSON documents, and
accept them as input too. This allows you to build pipelines (as we showed in
the previous section).

<div style="text-align: center">
    <img width="300px" src="/apicheck/assets/images/data_format.png" alt="APICheck data format">
</div>
