Creating a new tool
===================

Before writing new commands, check the :ref:`Commands & Tools <commands_reference>` to be sure you understand the :samp:`tool` concept adequately.

What is a tool?
---------------

A tool is a utility integrated into the ``APICheck`` suite. Tools are not as simple as commands.

Scaffolding
-----------

Usually, a tool has three files:

- Command Line Interface contents: :samp:`cli.py`.
- Tool configuration structures: :samp:`config.py`.
- Actions definitions file: :samp:`run.py`.

.. note::

   The only mandatory file is :samp:`cli.py`; the others can be omitted.

Building New tool
-----------------

``APICheck`` has an integrated management tool to help us develop new tools. To create a new tool you can run :samp:`create-tool` action.

.. code-block:: console

   > at-manage create-tool my_new_tool

This command will create the required scaffolding. Each file is self-documented.
