API Check
=========

This it's a first glympse of a bright future.


Sources
=======

Proxy mode
----------

API-Check can start as a HTTP proxy and try to derive the server API, and store request/response in a database.

Required params
+++++++++++++++

Running proxy mode need, at least, 2 parameters:

- **Connection string**: database connection string
- **domain**: Only stores information for an specific domain

Usage examples
++++++++++++++

.. code-block:: console

    > python -m apicheck.cli.importers proxy -C sqlite:///mydatabase.sqlite3 www.google.es

Also can configure listen port / address using parameter `-l` / `-p`:

.. code-block:: console

    > python -m apicheck.cli.importers proxy -l 0.0.0.0 -p 9000 -C sqlite:///mydatabase.sqlite3 www.google.es

By default, API-Check proxy mode doesn't stores assets content (images, videos, etc) into database. If you want to do that (be aware with that, your database can growth a lot!) you can use `--store-assets` param:

.. code-block:: console

    > python -m apicheck.cli.importers proxy --store-assets -C sqlite:///mydatabase.sqlite3 www.google.es


Using a server-oriented database
++++++++++++++++++++++++++++++++

API-Checks supports all of the database supported by `SQLAlchemy <https://docs.sqlalchemy.org/en/latest/core/engines.html>`_.

**Example using Mysql**

.. code-block:: console

    > docker run --name apicheck-mysql -e MYSQL_DATABASE=apicheck -e MYSQL_ROOT_PASSWORD=my-secret-pw -d -p 3306:3306 mysql:5.5
    > python -m apicheck.cli.importers pro

**Example using PostgresSQL**

.. code-block:: console

    > docker run --name apicheck-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=apicheck -d -p 5432:5432 postgres
    > python -m apicheck.cli.importers proxy --store-assets -C postgresql+pg8000://postgres:mysecretpassword@localhost/apicheck www.google.es