APICheck Sensitive Data Finder
==============================

**PYTHON 3.8 needed**

Usage through Kapow!
--------------------

.. code-block:: console

    > docker build -t ac-sd .
    > docker run -p 8080:8080 --rm ac-sd -d
    > curl --data-raw '{"password": "sss"}' -v http://localhost:8080/apicheck/sensitive-data
    [{"where": "response", "path": "/", "keyOrValue": "key", "sensitiveData": "password"}]

Usage cli
---------

For the following examples *data.json* is a APICheck format file with a Request / Response info.

With remote rules
+++++++++++++++++

.. code-block:: console

    $ cat data.json | ac-sensitive -r http://127.0.0.1:9999/rules/rules.yaml

With local rules
++++++++++++++++

Using core rules:

.. code-block:: console

    $ cat data.json | ac-sensitive

With many rules files
+++++++++++++++++++++

.. code-block:: console

    $ cat data.json | ac-sensitive -r rules/java.yaml -r rules/credentials.yaml

Export results as json
++++++++++++++++++++++

.. code-block:: console

    $ cat data.json | ac-sensitive -o results.json -r rules/java.yaml -r rules/credentials.yaml

Quiet mode
++++++++++

Don't output nothing into console

.. code-block:: console

    $ cat data.json | ac-sensitive -q

Filtering false positives
+++++++++++++++++++++++++

**By ignore file**

Dockerfile-sec allows to ignore rules by using a file that contains the rules you want to ignore.

.. code-block:: console

    $ cat data.json | ac-sensitive -F ignore-rules

Ignore file format contains the *IDs* of rules you want to ignore. **one ID per line**. Example:

.. code-block:: console

    core-001
    core-007

**By cli**

You also can use cli to ignore specific *IDs*:

.. code-block:: console

    $ cat data.json | ac-sensitive -i core-001,core007

Using as pipeline
+++++++++++++++++

You also can use ac-sensitive as UNIX pipeline.

Loading Dockerfile from stdin:

.. code-block:: console

    $ cat data.json | ac-sensitive -i core-001,core007

Exposing results via pipe:


.. code-block:: console

    $ cat data.json | ac-sensitive -i core-001,core007 | jq

Output formats
--------------

JSON Output format
++++++++++++++++++

.. code-block:: json

    [
      {
        "where": "response",
        "path": "/",
        "keyOrValue": "key",
        "sensitiveData": "password"
      }
    ]