Format Spec
===========

Api check rely on spefecific data format to be used among all the tools. You
can write your own Api Check tool just stick to that format.

Api check has three tools type:

 * Producers
 * Transformers
 * Actions

Producers can connect Api Check to other tools o generate their own data; they
must have a valid formatted output. Transformers can change data or metadata;
they must have an input and output. Actions do things but they are terminal;
they have input only.

Data format
-----------

A valid data format for ApiCheck must contain the request. Optionally can
contain metadata and also a response.

In this repository we have a json-schema validators to check your format.

Multiple request must be encoded as json lines.

Data process
------------

Api check can be running for a long time, o can process a lot of data, so you
must process data line by line allways.

