---
layout: post
author: cr0hn
author_link: https://twitter.com/ggdaniel
title:  "Validating JWT Tokens in shell scripts"
---

JWT Tokens are very popular as SSO authentication mechanism, for authorization and widely used in the Microservices paradigm. But have we really pay attention if JWT tokens are valid?
<!--more-->

There are many amazing online validators out there, like [JWT.io](https://jwt.io/#debugger-io) but they're not useful if you want to integrate the validation process into a script or into an shell execution pipeline.

![JWT.io screenshot](https://i.ibb.co/rZHdF6y/jwt-io-validator.png)

It's really easy to check if a JWT Token is valid with [APICheck JWT Validator](https://bbva.github.io/apicheck/tools/apicheck/jwt-checker) and take the advantage of chaining with other validations by using [APICheck tools](https://bbva.github.io/apicheck/docs).

```bash
$ acp install jwtchk
$ acp install acurl
$ acurl http://my-company.com/api/entry-point | jwtchk -allowAlg HS256 -allowAlg HS384 -issuer bbva-iam -audience my-api-id -secret bXlTZWNyZXRQYXNzd29yZG15U2VjcmV0UGFzc3dvcmQK

Issuer claim doesn't match. Expected: bbva-iam, got: other-iam
Audience claim doesn't match. Expected: my-api-id, got: other-id
```

You have several others options available in order to check if the JWT token was generated following the best practices.
