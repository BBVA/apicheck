APITest
=======

APITest has the actions:

- analyze
- parse

You can see this actions typing:

.. code-block:: bash

    $ apitest-postman -h
    Usage: apitest-postman [OPTIONS] COMMAND [ARGS]...

    Options:
      -v           Verbose output
      -q, --quiet  Minimal output
      -h, --help   Show this message and exit.

    Commands:
      analyze  Extract information from APITest collection
      parse    Parse APITest collection and export...

.. note::

    You can find API-Test and APITest examples files at project home, in directory ::samp:`example/`

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

Analyze
-------

Brief
+++++

This command analyzes a APITest file and show information summary.

Invocation
++++++++++

This action could be invoked as:

.. code-block:: bash

    $ apitest_postman -vvvv analyze examples/Postman_Echo.postman_collection.json
    [*] Analyzing postman file: 'examples/Postman_Echo.postman_collection.json'
    [*] File format is OKs
    [*] Summary:
        - Total collections: 6
        - Total end-points: 21
          > DigestAuth Success   -     2 endpoints
          > Hawk Auth            -     3 endpoints
          > Get Cookies          -     3 endpoints
          > Response Headers     -     2 endpoints
          > DELETE Request       -     5 endpoints
          > Deflate Compressed Response -     6 endpoints

Parse
-----

Brief
+++++

Parse a APITest collection and generates an apitest file format.

Invocation
++++++++++

This action could be invoked as:

.. code-block:: bash

    $ apitest-postman -vvvv parse examples/Postman_Echo.postman_collection.json -o apitest_file.json
    [*] Analyzing postman file: 'examples/Postman_Echo.postman_collection.json'
    [*] File format is OKs
    [*] Exporting to: 'apitest_file.json'

This command only accept one flag: :samp:`-o` that indicates the output file name of API-Test generated file.