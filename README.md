---
title: Title



summary: "summary"
---
<!--

#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: README.ipynb
# command to build the docs after a change: nbdev_build_docs

-->


# Proxy Manager - Python

The package is intended to manage a set of proxies, rotating through at random, to prevent blocking. Proxies are dropped from the rotation if they fail multiple times in a row.

VERY EARLY STAGE


### Installation
`pip install ProxyManager`

### Basic usage


```python
PROXY_LIST = [
         '70.45.80.236:4602',
         '70.45.80.236:4603',
         '70.45.80.236:4604'
        ]

URL = 'http://www.myurl.com'

from ProxyManager.core import ProxyManager, Proxy

proxies = [i for i in PROXY_LIST] # OR [Proxy(i) for i in PROXY_LIST]
response = proxies.make_request(URL)
```


### Free Proxies

If you don't bring your own proxies, which is HIGHLY recommended, I have written a function that scrapes https://free-proxy-list.net/ to obtain a set of proxies.

```python
from ProxyManager.free_proxies import get_free
FREE_PROXIES = get_free(10)
proxies = [Proxy('{}:{}'.format(i['ip'], i['port'])) for i in FREE_PROXIES]

```
