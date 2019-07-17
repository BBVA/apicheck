For Developers
==============

Acceptance tests
----------------



Navigation Flow Checking
------------------------

Some steps imply complex navigation flows. Instead of writing long test code cases or opening a browser. Navigate through ``APICheck`` proxy, save the session and re-run it infinite times.


API Version Tracking
--------------------

``APICheck`` can be used as an additional step in CI pipelines, just before promoting code to production environments, launch an APICheck instance to capture the real API definition.

This way you would have all API versions promoted to production stored.


Find low level bugs
-------------------

Navigate using ``APICheck``'s proxy. Then analyze with *dataset*. This tool allows you to discover strange http headers, or unusual endpoints used during the navigation. Also Cookie or JWT Token size growth.


API Diff
--------

Find differences between two API versions.


Real World vs Definition
------------------------

Find differences between your API definition and the real API implementation.
