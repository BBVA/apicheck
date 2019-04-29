Overview
========

This document contains a index reference for ``API-Check`` supported commands.

Command are grouped in the two types supported by ``API-Check``:

- :ref:`Tools <tools_reference>`
- :ref:`Commands <commands_reference>`

Tools
=====

Dataset
+++++++

- Description: Builds a dataset, analise it and create behavior graphs from user navigations stored in database.
- Examples:
- Usage:

.. code-block:: console

    > at-dataset -h


Proxy
+++++

- Description: Launches a local proxy and tracks navigation through it into a database.
- Examples:

    - :doc:`/home/quickstart`

- Usage:

.. code-block:: console

    > at-proxy -h

Send-Proxy
+++++++++++++

- Description: Sends proxy information, from previous navigation data or from OpenAPI definition, to output proxy.
- Examples:

    - :doc:`/home/quickstart`

- Usage:

.. code-block:: console

    > at-sendproxy -h


Commands
========

Commands are small specific purpose commands. They follow the \*NIX philosophy.

ac-j2y
++++++

- Description: JSON to YAML converter
- Command documentation: :ref:`J2Y <ac_j2y>`


ac-y2j
++++++

- Description: YAML to JSON with indent option
- Command documentation: :ref:`J2Y <ac_y2j>`
