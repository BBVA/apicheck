ac-y2j
======

.. _ac_y2j:

This command converts a file in YAML format to JSON, optionally indenting the output.

Usage examples:

.. code-block:: console

    > ac-y2j petstore-swagger.yaml
    [ ... JSON CONTENT ... ]

.. code-block:: console

    > ac-y2j petstore-swagger.yaml > petstore-swagger.json

.. code-block:: console

    > cat petstore-swagger.json | ac-j2y -P
    [ ... INDENTED JSON CONTENT ... ]


ac-j2y
======

.. _ac_j2y:

This command converts a file in JSON format to YAML.

Usage examples:

.. code-block:: console

    > ac-j2y petstore-swagger.json
    [ ... YAML CONTENT ... ]

.. code-block:: console

    > ac-j2y petstore-swagger.json > petstore-swagger.yaml

.. code-block:: console

    > cat petstore-swagger.json | ac-j2y  > petstore-swagger.yaml


ac-replay
=========

.. _ac_replay:

This command replays saved proxy logs to network.

Usage examples:

.. code-block:: console

    > ac-replay -C sqlite:///proxy.sqlite3
    [ ... JSON CONTENT ... ]

.. code-block:: console

    > ac-replay -C sqlite:///proxy.sqlite3 --multiplier 10  # Ten times faster
    [ ... JSON CONTENT ... ]
