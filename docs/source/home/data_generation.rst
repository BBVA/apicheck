Data generation
===============

All data generation tools are placed into apicheck.core.generator. Inside this
package you can find apicheck.core.generator.open_api_strategy with the default
strategy for open api files.

.. note::
    By the moment string format it's not supported.

The generator will use the Faker package to generate data, following the 
openapi specification.

Request definition
------------------

The overall definition used across the file is the request definition. A request
definition describe, in a very simple terms, how the request will look like.
This definition allways have the same fields:

.. code-block:: yaml

    headers:
        [value or type]
    pathParams:
        [value or type]
    queryParams:
        [value or type]
    body:
        [value or type]

The headers are a set of key values that can hold two type of values. A fixed
value or a type definition.

The fixed value looks like the following:

.. code-block:: yaml

    userId: 500

Type definition
---------------

The type used in apicheck is a direct copy of the type definition of open api 3
specification.
Every item can be defined as an open api type. You can use also some custom 
type created for apicheck. One of this is dictionary, that looks like:

.. code-block:: yaml

    type: dictionary
    values:
        - A
        - B
        - C

Used to define the userName field will look like:

.. code-block:: yaml

    userName:
        type: dictionary
        values:
            - A
            - B
            - C


OpenApi 3 override Example
--------------------------

You can override openapi 3 type definition using your own file, like this:

.. code-block:: yaml

    name: "my library api"
    description: "my awesome library api"
    version: "0.9-RC"
    tags:
        - books
        - users
    global:
        headers:
            Authorization: Basic YWxhZGRpbjpvcGVuc2VzYW1l
    endpoints:
        /{userId}/books:
            methods:
                - get
                - post
            pathParams:
                userId: 500
            post:
                body:
                    name:
                        override: true
                        type: string
                        maxLength: 40
                    author: Edgar Alan Poe
                    pages:
                        type: number
                        minimum: 100
                        maximum: 300
                    genre:
                        type: dictionary
                        values:
                            - mistery
                            - fiction
                            - suspense

The first part is about metadata. You can query apicheck to find a set of 
rules using this data. Name and version are required, all other data is 
optional.

.. code-block:: yaml

    name: "my library api"
    description: "my awesome library api"
    version: "0.9-RC"
    tags:
        - books
        - users



The global part is a request definition used as a template of all other rules.
When you include a header in this section, all requests regarding this rules 
will include this value.

.. code-block:: yaml

    global:
        headers:
            Authorization: Basic YWxhZGRpbjpvcGVuc2VzYW1l