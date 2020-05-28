---
layout: post
author: cr0hn
author_link: https://twitter.com/ggdaniel
title:  "Validating JWT Tokens in shell scripts"
---

JWT Tokens are very popular as SSO authentication mechanism and for Microservices paradigm. But have we really pay attention if JWT token are valid?
<!--more-->

Of course you can use awesome validator of [JWT.io](https://jwt.io/#debugger-io) but it's not useful if you want integrate validation in a script or in an shell execution pipeline. 

![JWT.io screenshot](https://i.ibb.co/rZHdF6y/jwt-io-validator.png)

It's easy check if a JWT Token is valid with [APICheck JWT Validator](https://bbva.github.io/apicheck/tools/apicheck/jwt-checker) and take the advantage of chain with other [APICheck tools](https://bbva.github.io/apicheck/docs).

```bash
$ acp install jwtchk
$ acp install acurl
$ acurl http://my-company.com/api/entry-point | jwtchk -allowAlg HS256 -allowAlg HS384 -issuer bbva-iam -subject subject-id -secret bXlTZWNyZXRQYXNzd29yZG15U2VjcmV0UGFzc3dvcmQK

Issuer claim doesn't match. Expected: bbva-iam, got: other-iam
Subject claim doesn't match. Expected: subject-id, got: other-id
```
