apitest
=======

![Logo](doc/images/logo.jpg)

*apitest: Testing your API for security*

Code | https://github.com/cr0hn/apitest
---- | ----------------------------------------------
Issues | https://github.com/cr0hn/apitest/issues/
Python version | Python 3.5 and above

What's apitest
--------------

Long description

What's new?
-----------

This apitest version, add a lot of new features and fixes, like:

Version 1.0.0
+++++++++++++

- First version released

You can read entire list in CHANGELOG file.

Installation
------------

Simple
++++++

Install apitest is so easy:

```
$ python -m pip install apitest
```

With extra performance
++++++++++++++++++++++

Apitest also includes some optional dependencies to add extra performance but requires a bit different installation, because they (usually) depends of C extensions.

To install the tool with extra performance you must do:

```
$ python -m pip install 'apitest[performance]'
```

**Remember that apitest only runs in Python 3.5 and above**.

Quick start
-----------

You can display inline help writing:

From cloned project
+++++++++++++++++++

```bash

python apitest.py -h
```

From pip installation
+++++++++++++++++++++

```bash

apitest -h
```