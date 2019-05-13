Creating a new tools
====================

Before start writing new tool check the :ref:`Command & tools <commands_reference>` to be sure to understand the :samp:`tool` concept.

What's a tool?
--------------

Tool is an utility integrated into ``API-Check`` suite. It does some complex thing.

Scaffolding
-----------

Usually, a tool have these three files:

- Command Line Interface contents: :samp:`cli.py`.
- Tool configuration structures :samp:`config.py`.
- Actions definitions file :samp:`run.py`.

.. note::

   These 3 files are not mandatory. The only required file is the :samp:`cli.py`

Building New tool
-----------------

``API-Check`` has an integrated manage tool to help us to develop new tools. To create new tool you can run :samp:`create-tool` action.

.. code-block:: console

   > at-manage create-tool my_new_tool

This command will create a new scaffolding. Each file is self-documented.