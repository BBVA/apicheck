---
layout: doc
title: Grab from CURL
type: apicheck
permalink: /tools/apicheck/acurl
---

Grab from CURL
==============

This tool provide a binray curl command (acurl) that will be translated into a
valid reqres object. You can use this way:

```bash
$ acurl www.google.com
```

The binary curl command accept the same parameters than the curl command. For 
further documentation you can check curl man:

```bash
$ man curl
```

You can use to retrieve also ssl protected urls:

```bash
$ acurl https://www.google.es
```

This tool add curl_log field to the _meta field. You can find all curl internal
log info in this field.
