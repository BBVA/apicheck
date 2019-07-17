Installation & Quick start
==========================

``APICheck`` levarages `MITM Proxy <https://mitmproxy.org>`_ so you must install all its dependencies (don't worry, it's easy, just `follow their documentation <https://docs.mitmproxy.org/stable/overview-installation/>`_).

.. _installation:

Installation
------------

Using Pip
+++++++++

.. code-block:: console

    > pip install apicheck


.. note::

    **MySQL Support**: If you want to install ``APICheck`` with MySQL Support use this command instead:

    .. code-block:: console

        > pip install apicheck[mysql]

Using Docker
++++++++++++

.. code-block:: console

    > docker run --rm bbvalabs/apicheck -h

Using interactive CLI
+++++++++++++++++++++

Use this command to open an interactive CLI for API testing:

.. code-block:: console

    > docker run --rm -it bbvalabs/apicheck

Quick Start
-----------

The usage of ``APICheck`` is quite simple. After :ref:`installation <installation>` you'll have all **tools** and **commands** available as shell commands.

``APICheck`` has a lot of commands. You can find the complete reference in :doc:`/command_reference_index` and a list of curated recipes grouped by use case in :doc:`/uses_cases/uses_cases_overview`.

Learning by example: Discovering non-documented APIs
----------------------------------------------------

One of the biggest problems you'll face while testing an API is the lack of documentation. The majority of REST API are not designed to be *auto-discoverable*. For this reason ``APICheck`` provides the **proxy** command.

1 - Launching the proxy
+++++++++++++++++++++++

``APICheck``'s **proxy** command is a local proxy that track all request for a specific domain. ``APICheck`` stores this requests into a database. With this data, ``APICheck`` can perform tons of operations with the API, one of them: derive the API definition and test it.

To start the proxy we execute:

.. code-block:: console

    > at-proxy

2 - Configuring proxy and browsing
+++++++++++++++++++++++++++++++++++

Once we have the proxy running, we must `configure the browser to use it <https://www2.aston.ac.uk/library/staff/mozillaproxy/index>`_.

At this stage we must browse the website we want to extract the REST API from.

.. note::

    Currently ``APICheck`` only can take actions with these APIs that was pass throught the proxy. Therefore we must be thorough browsing the website.

3 - Perform actions with the recovered information
++++++++++++++++++++++++++++++++++++++++++++++++++

Once we have the API browsing information, we can perform actions:

**Send information to hacking tool**

The most simple action is to replay the browsing history to other hacking tools that work as proxies. For instance: `OWASP ZAP <https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project>`_, `Burp Suite <https://portswigger.net/burp>`_ or whatever you want.

.. code-block::

    > at-sendproxy 127.0.0.1:8080


Listing actions
---------------

To assist in the usage, you can list all ``APICheck`` commands using the ``ap-help`` command. This command will display a complete list of commands.

.. code-block:: console

    > at-help
