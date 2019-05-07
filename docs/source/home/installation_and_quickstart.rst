Installation & Quick start
==========================

``API-Check`` uses `MITM Proxy <https://mitmproxy.org>`_ then you must install all the dependencies inherited from them. It's easy to install them. You can `follow their documentation <https://docs.mitmproxy.org/stable/overview-installation/>`_.

.. _installation:

Installation
------------

Using Pip
+++++++++

.. code-block:: console

    > pip install apicheck


.. note::

    **MySQL Support**: If you want to install ``API-Check`` with Mysql Support you must install as follows:

    .. code-block:: console

        > pip install apicheck[mysql]

Using Docker
++++++++++++

.. code-block:: console

    > docker run --rm bbvalabs/apicheck -h

Using interactive CLI
+++++++++++++++++++++

If you want to open an interactive CLI for testing an API you can run:

.. code-block:: console

    > docker run --rm -it bbvalabs/apicheck

Quick Start
-----------

Use ``API-Check`` is very easy. After :ref:`install <installation>` you can type cli commands.

``API-Check`` has a lot of commands. You can find the complete reference in :doc:`/command_reference_index` and you also can check grouped commands by the purpose of you want to use ``API-Check`` in the :doc:`/uses_cases/uses_cases_overview`.

Learning by examples: Discovering non-documented APIs
-----------------------------------------------------

One of the more complex things you can find when try to test an API is the missing documentation. Most of the REST API have not the *auto-discover* option. For this reason ``API-Check`` has the **proxy** working mode.

1 - Launching the proxy
+++++++++++++++++++++++

**Proxy** working mode launches an local proxy that track all request for a specific domain. ``API-Check`` stores this request in a database. With this information, ``API-Check`` can perform a lot of operations with the API, one of them: derive the API definition and test it.

To start the proxy mode we must execute the following command:

.. code-block:: console

    > at-proxy

2 - Configuring proxy and browsing
+++++++++++++++++++++++++++++++++++

Once we have been launched the proxy, we must `configure it into the browser <https://www2.aston.ac.uk/library/staff/mozillaproxy/index>`_.

In this step we must browsing in the web site we want to extract the REST API.

.. note::

    Currently ``API-Check`` only can take actions with these APIs that was pass throught the proxy. Then we must be thorough in the browsing in the web site.

3 - Perform actions recovered information
+++++++++++++++++++++++++++++++++++++++++

Once we have the API browsing information, we can perform actions to them:

**Send information to hacking tool**

The most simple action is to replay API endpoint to hacking tools that works as a proxies. This means: `OWASP ZAP <https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project>`_, `Burp Suite <https://portswigger.net/burp>`_ or whatever you want.

.. code-block::

    > at-sendproxy 127.0.0.1:8080


Listing actions
---------------

For helping the usage, you can list all ``API-Check`` actions using the command ``ap-help``. This command will display the complete list of commands.

.. code-block:: console

    > at-help
