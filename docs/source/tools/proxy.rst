Proxy
=====

.. _proxy:

Launches a local proxy and stores all the intercepted navigation traffic into the database.

.. note::
        The proxy tool uses `MITM Proxy <https://mitmproxy.org>`_. Be sure to follow their `installation steps <https://docs.mitmproxy.org/stable/overview-installation/>`_.

Basic usage
-----------

For the simplest proxy use case, you should pass a database connection string. If you don't want lo launch a database server, you can use the SQLite connector.

.. code-block:: console

    > at-proxy -C sqlite:///mydb.sqlite3

.. note::

    The connections strings for different databases follow the SQL `Alchemy format <https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls>`_
