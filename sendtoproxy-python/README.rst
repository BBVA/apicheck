Send to proxy
=============

This tool send stdin request to a remote proxy.

Install
-------

Generic
+++++++

./INSTALL

Python mode
+++++++++++

python setup.py install

Usage
-----

Getting help
++++++++++++

After install you can type this to use:

.. code-block:: console

    $ ac-sentoproxy -h

Usage example
+++++++++++++

.. code-block:: console

    $ cat examples/valid-request.json | ac-sendtoproxy -q http://127.0.0.1:9999
