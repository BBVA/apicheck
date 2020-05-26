---
layout: doc
title: Apicheck from CURL
type: apicheck
permalink: /tools/apicheck/acurl
---

Apicheck from CURL
==================

This tool provide a binray curl command (acurl) that will be translated into a
valid reqres object. 

*Tool type:* generator

## Tool description

You can use this way:

The binary curl command accept the same parameters than the curl command. For 
further documentation you can check curl man:

```bash
$ man curl
```

This tool add curl_log field to the _meta data. You can find all curl internal
log info in this field.

## Quick start

As simple as use curl:

```bash
$ apc install acurl
$ acurl www.google.com
```

You can use to retrieve also ssl protected urls:

```bash
$ acurl https://www.google.com
```

