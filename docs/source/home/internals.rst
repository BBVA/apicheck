Internals
=========

Structure and basic Concepts
----------------------------

.. _apicheck_structure:

``API-Check`` is a toolset. This means that the project itself is a set of tools grouped in project.

.. image:: /_static/apicheck_001_structure.png
   :align: center

Commands & tools
----------------

``API-Check`` has 2:

- Commands
- Tools

.. _commands_reference:

Commands
++++++++

Commands are a small programs that have more specific things. These commands follow the \*NIX philosophy: a lot os small pieces, but that can be connected between them.

You can imagine this commands as a ``awk`` or ``grep`` commands. Small, but powerful.

.. _tools_reference:

Tools
+++++

Tools does more complex things that a command. You also can chain with commands.

Chaining
--------

As \*NIX like, you can chain :samp:`commands` and :samp:`tools`. Probably, you will build something like:

.. image:: /_static/apicheck_unix_pipeline.png
   :align: center


Data follow
-----------

Commands and Tools

.. image:: /_static/apicheck_002_json_flow.png
   :width: 300px
   :align: center