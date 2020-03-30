For Developers
==============

Acceptance tests
----------------

.. todo::

   Acceptance tests proper.


Navigation Flow Checking
------------------------

Some steps imply complex navigation flows. Instead of writing long test code cases or opening a browser, navigate through ``APICheck`` proxy, save the session, and re-run it as many times as you want.


API Version Tracking
--------------------

``APICheck`` can be used as an additional step in CI pipelines; just before promoting code to production environments, launch an ``APICheck``'s proxy instance to capture the real API definition.

This way you will be able to store all API versions that have been promoted to production.


Find low level bugs
-------------------

Navigate using ``APICheck``'s proxy. Then cli_analyze it with *dataset*. This tool allows you to discover strange http headers, or unusual endpoints used during the navigation. Also Cookie or JWT Token size growth.


API Diff
--------

Find differences between two API versions.


Real World vs. Definition
-------------------------

Find differences between your API definition and the actual API implementation.
