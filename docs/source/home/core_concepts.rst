Core Concepts
=============


Command types
-------------

``API-Check`` has 2 kind of commands:

- Commands
- Tools

.. _commands_reference:

Commands
+++++++++++++

Commands are a small executables that have more specific things. These commands follow the \*NIX philosophy: a lot os small pieces, but that can be connected between them.

You can imagine this commands as a ``awk`` or ``grep`` commands. Small, but powerful.

.. _tools_reference:

Tools
+++++

Tools are high level commands that join some small functionality in more *complete* command.

You can think of that as a chain of some \*NIX calls, grouped in an unique high level command. I.e:

.. code-block:: console

    > cat file.text | grep -v "MyString" | awk '{print "$2"}' | tee nmap -PN -p 443,80 -v | grep -i "Apache 2"

This example command could grouped in an *Super Command*

.. code-block:: console

    > ac-banner


What API-Check an do?
---------------------

With API-Check can extract API definition from a standard definition file, or run as a proxy and extract the API.


.. image:: ../_static/apicheck_diagram.png

