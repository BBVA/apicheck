---
layout: post
author: cr0hn
author_link: https://twitter.com/ggdaniel
title: "Checking connections to suspicious sites while we are browsing"
---

Every day we visit a lot of sites on the Internet. Each of these sites have a lot of resources and do a lot of connections to external servers, but... how can we check for connections for suspicious sites? And how can we script some actions?
<!--more-->

You can install an Antivirus. You can use some additional software that try to "protect" you against this type of sites but you can't launch any custom action (or shell script!) when you detect them. Why not use `APICheck` for that?

OK, we must follow these steps:
 
- first, we need a list of suspicious sites or IPs. You have a complete list of resources at [MalwareDomainList](https://www.malwaredomainlist.com). For this post we downloaded a list with [suspicious IPs](http://www.malwaredomainlist.com/hostslist/ip.txt).
- Then we'll need [APICheck Proxy](https://bbva.github.io/apicheck/tools/apicheck/apicheck-proxy) to intercept and launch actions each time a request arrives.
- Make sure you have installed [JQ](https://stedolan.github.io/jq/)

![MalwareDomainList](https://i.ibb.co/Xsg2wCp/malwaredomainlist.png)

Finally we need to configure our browser with *http://127.0.0.1:8080* proxy and write this command:

```console
$ docker run --rm -i -p 8080:8080 bbvalabs/apicheck-proxy | jq --unbuffered -r '.request.url' |  grep -f ~/Downloads/ip.txt -F
https//103.14.120.121:443
https//200.58.114.51/fake.php
``` 

Where:

- ip.txt is the list of malicious IP downloaded from MalwareDomainList
