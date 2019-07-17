Tool & Command index
======================

This document contains a index reference for ``APICheck`` supported commands.

Command are grouped in two types ``APICheck``:

- :ref:`Tools <tools_reference>`
- :ref:`Commands <commands_reference>`

Tools
=====

Dataset
+++++++

- Description: Builds a dataset, analyzes it and creates behavior graphs based on the user navigations stored in the database.
- Command documentation: :ref:`Dataset tool <dataset>`

Proxy
+++++

- Description: Launches a local proxy and stores all the intercepted navigation traffic into the database.
- Command documentation: :ref:`Proxy tool <proxy>`

Send-To
+++++++

- Description: Send the given HTTP API traffic. Optionally you can specify a proxy to pass through.
- Command documentation: :ref:`Send-to tool <send_to>`


Commands
========

Commands are small components with a small & fix purpose. They follow the \*NIX philosophy.

ac-j2y
++++++

- Description: JSON to YAML converter
- Command documentation: :ref:`J2Y <ac_j2y>`


ac-y2j
++++++

- Description: YAML to JSON with indent option
- Command documentation: :ref:`J2Y <ac_y2j>`
