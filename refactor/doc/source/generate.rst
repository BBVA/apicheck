Generate
========

Generate has the actions:

- load
- unittest

You can see this actions typing:

.. code-block:: bash

    $ apitest-generate -h
    Usage: apitest-generate [OPTIONS] COMMAND [ARGS]...

    Options:
      -v           Verbose output
      -q, --quiet  Minimal output
      -h, --help   Show this message and exit.

    Commands:
      load      Load an ApiTest JSON file and display summary...
      unittest  Build unittest-like for testing the API

.. note::

    You can find API-Test and APITest examples files at project home, in directory :samp:`example/`

.. note::

    We can increase the verbosity setting multiple times the -v flag:

    .. code-block:: bash

        $ apitest-generate -vvv load ...

    **Be careful** to put the -v flag **before** command:

    **WRONG**:

    .. code-block:: bash

        $ apitest-generate load -vvv ...

    **GOOD**:

    .. code-block:: bash

        $ apitest-generate -vvv load ...

Load
----

Brief
+++++

This command load an API-Test file and show an information summary.

Invocation
++++++++++

This action could be invoked as:

.. code-block:: bash

    $ apitest-generate -vvvv analyze examples/Postman_Echo.postman_collection.json
    [*] File format is OKs
    [*] Summary:
        - Total collections: 6
        - Total end-points: 21
          > DigestAuth Success   -     2 endpoints
          > Hawk Auth            -     3 endpoints
          > Get Cookies          -     3 endpoints
          > Response Headers     -     2 endpoints
          > DELETE EndPointRequest       -     5 endpoints
          > Deflate Compressed Response -     6 endpoints

Unittest
--------

Brief
+++++

API-Test could generates black-box test cases for a HTTP API and build them as a unittest cases.

TestS organization
++++++++++++++++++

Test are made in a specified output folder. In this folder it follow this structure:

\\_ output folder
    \\_ collection name
        \\_ end point group
            \\_ end point
                \\_ unittest_case_xxx.py

How test cases are made
+++++++++++++++++++++++

Black-box as unittest cases means that API-Test will generate a unittest for:

- Each end-point
- Each parameter of each end-point
- Each type of test that API-Test knows

This is:

If we have a REST API with 2 end-points:

1. :samp:`/api/v1/users/login`: With :samp:`user` / :samp:`password` as input parameters.
2. :samp:`/api/v1/users/edit`: With 4 user personal parameters as input data.

Tests cases generated:

- End-points: 2
- Parameters for:

    - End-point 1: 2
    - End-point 2: 4

- API-Tests type of cases: 3

Total of test generated:

.. math::

    totalCases = (2 * 3) + (3 * 4)

TestS cases format
++++++++++++++++++

The test cases are made in Python language and the uses the py.test framework to build the test.

An example of test case generated could be this code:

.. code-block:: python

    def test_http_methods_case_trace(make_requests):

        response, original, _ = make_requests("https://echo.getpostman.com/delay/3",
                                              method="TRACE",
                                              build_fuzzed_response=False)

        assert response.status_code != 200

This code are generated dinamically using API-Test definition file.

Cases types
+++++++++++

API-Test is focused in security test and at this moment only implement security test.

Currently API-Test has tests for this types security tests:

- Cross-Site Scripting (XSS)
- SQL Injection
- HTTP Method testing

Running the test
++++++++++++++++

**Requirements**

To run the tests you need to install:

- Pytest
- Pytest-xdist (optional)
- Requests

You can install the requirements you could running:

.. code-block:: bash

    $ pip install -r requirements-runtest.txt

**Run test**

Go to the root test folder and then run the py.test

.. code-block:: bash

    $ cd build_unittest/
    $ py.test
    ========================================== test session starts ==========================================
    platform darwin -- Python 3.5.1, pytest-3.0.2, py-1.4.31, pluggy-0.3.1
    rootdir: /Users/Dani/Documents/Projects/apitest, inifile:
    plugins: asyncio-0.5.0, xdist-1.15.0
    collected 153 items

    build_unittest/postman_echo/deflate_compressed_response/deflate_compressed_response/test_http_methods_deflate_compressed_response.py FFFF
    build_unittest/postman_echo/deflate_compressed_response/deflate_compressed_response/test_sqli_deflate_compressed_response.py F
    build_unittest/postman_echo/deflate_compressed_response/delay_response/test_http_methods_delay_response.py FFFF
    build_unittest/postman_echo/deflate_compressed_response/delay_response/test_sqli_delay_response.py F
    build_unittest/postman_echo/deflate_compressed_response/get_utf_encoded_response/test_http_methods_get_utf_encoded_response.py FFFF
    ...

**Run test in Parallel**

Pytest support running the test parallelly and, even, in multiple hosts.

To run in localhost, but parallelly, we can run:

.. code-block:: bash

    $ cd build_unittest/
    $ py.test -n 5
    ========================================== test session starts ==========================================
    platform darwin -- Python 3.5.1, pytest-3.0.2, py-1.4.31, pluggy-0.3.1
    rootdir: /Users/Dani/Documents/Projects/apitest, inifile:
    plugins: asyncio-0.5.0, xdist-1.15.0
    gw0 [153] / gw1 [153] / gw2 [153] / gw3 [153] / gw4 [153]
    scheduling tests via LoadScheduling
    ....

Where **5** is the number of concurrently that we want.

Config file format
++++++++++++++++++

.. code-block:: yaml

    test_cases:
    - xss
    - sqli
    - http-methods