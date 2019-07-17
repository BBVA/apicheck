Creating a new tool
===================

Before start writing new commands check the :ref:`Command & tools <commands_reference>` to be sure you understand the :samp:`command` concept properly.

What is a tool?
---------------

A tool is an utility integrated into the ``APICheck`` suite. Tools are not as simple as commands.

Scaffolding
-----------

Usually, a tool have these three files:

- Command Line Interface contents: :samp:`cli.py`.
- Tool configuration structures: :samp:`config.py`.
- Actions definitions file: :samp:`run.py`.

.. note::

   The only mandatory file is :samp:`cli.py`; the others can be left out.

Building New tool
-----------------

``APICheck`` has an integrated management tool to help us in the development of new tools. To create a new tool you can run :samp:`create-tool` action.

.. code-block:: console

   > at-manage create-tool my_new_tool

This command will create the needed scaffolding. Each file is self-documented.
