Installation
============

``API-Check`` uses `MITM Proxy <https://mitmproxy.org>`_ then you must install all the dependencies inherited from them. It's easy to install them. You can `follow their documentation <https://docs.mitmproxy.org/stable/overview-installation/>`_.

Using Pip
---------

.. code-block:: console

    > pip install apicheck

Using Docker CLI
----------------

.. code-block:: console

    > docker run --rm bbvalabs/apicheck -h

Using interactive CLI Docker
----------------------------

If you want to open an interactive CLI for testing an API you can run:

.. code-block:: console

    > docker run --rm -it bbvalabs/apicheck
