---
layout: post
author: cr0hn
author_link: https://twitter.com/ggdaniel
title:  "Chaining BurpSuite and OWASP ZAP"
---

BurpSuite is a nice tool but not OpenSource, so not all their features are free. OWASP ZAP is an Open Source alternative but, sadly, it's not so powerful as BurpSuite in some cases. But... why not to use both at the same time? 
<!--more-->

Ok, ok, It's true that you can configure BurpSuite to output to another proxy but... why not to use APICheck for that? It's easier and transparent.

Conceptually we will do:
    
    +-------------------+          +------------------------+        +--------------------------+       +-----------------+
    |  APICheck Proxy   |--------->| APICheck Send-to-Proxy |-+----->| APICheck Send-to-Proxy   |------>|   OWASP ZAP     |
    +-------------------+          +------------------------+ |      +--------------------------+       +-----------------+
                                                              |
                                                              |      +--------------------------+
                                                              +----->|    BurpSuite             |
                                                                     +--------------------------+

All we need to do is:

```bash
$ pip install apicheck-package-manager
$ acp install send-to-proxy
$ docker run --rm -it -p 9001:9001 bbvalabs/apicheck-proxy http://127.0.0.1:9000 | send-to-proxy http://127.0.0.1:9000 | send-to-proxy http://127.0.0.1:8080
```

A brief explanation: 

First command starts `APICheck proxy`. Each request you do in your browser will be send to the first `APICheck send-to-proxy` command. This one, in turn, after sending received request to the first proxy (BurpSuite) it will send the original request (from Proxy, do you remember?) to next `APICheck send-to-proxy` command that sends same request to the second proxy (OWASP Zap).

Easy, but useful, right?  
