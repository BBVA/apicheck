Proxy
=====

.. _proxy:

Launches local proxy and stores all the navigation browsing info into a database.

Proxy tool uses `MITM Proxy <https://mitmproxy.org>`_, then be sure to follow their `installation steps <https://docs.mitmproxy.org/stable/overview-installation/>`_.

Basic usage
-----------

To basic launch of only needs to specify the database connection string. If you don't want lo launch a database server, you can use the SQLite connector.

.. code-block:: console

    > at-proxy -C sqlite:///mydb.sqlite3

.. note::

    The connections strings for different databases follows the SQL `Alchemy format <https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls>`_

