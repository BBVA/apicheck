Internals
=========

Pipelines & data flow
---------------------

Pipelines
+++++++++

As \*NIX like you can chain :samp:`commands` and :samp:`tools`. Imagine this \*NIX *pipeline* execution:

.. image:: /_static/apicheck_unix_pipeline.png
   :align: center

You can build the ``API-Check``-like *pipeline* doing:

.. image:: /_static/apicheck_unix_pipeline.png
   :align: center

Data follow
+++++++++++

::samp:`commands` and ::samp:`tools` receives from input and output information that allow to build pipelines (as we learnt in the previous section). To do that, they may share *speak* the same data format. The chosen data format for ``API-Check`` is ::samp:`JSON`.

Commands and Tools

.. image:: /_static/apicheck_002_json_flow.png
   :width: 300px
   :align: center


Commands & tools
----------------

``API-Check`` has 2:

- Commands
- Tools

.. _commands_reference:

Commands
++++++++

Commands are a small programs that have more specific things. These commands follow the \*NIX philosophy: a lot os small pieces, but that can be connected between them.

You can imagine this commands as a ``awk`` or ``grep`` commands. Small, but powerful.

.. _tools_reference:

Tools
+++++

Tools does more complex things that a command. You also can chain with commands.

.. _data_generation:

Data generation
---------------

All data generation tools are placed into apicheck.core.generator. Inside this
package you can find apicheck.core.generator.open_api_strategy with the default
strategy for open api files.

.. note::
    By the moment string format it's not supported.

The generator will use the Faker package to generate data, following the
openapi specification.

Request definition
++++++++++++++++++

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
+++++++++++++++

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

Definition hierarchy
++++++++++++++++++++

If software find several definition for the same element the last readed will
remain. The following is the typical order or reading:

    - Open Api 3 File
    - Rules files (readed in search order)
    - Global tag inside rule
    - Request definition inside endpoint
    - Request definition inside method

Definition override
+++++++++++++++++++

If we want to start from scratch a type definition, we must use de override
keyword. By default this keyword has the false value. If we find the true
value then the generator will use only our specification and will ignore
the Open Api specification.

OpenApi 3 override Example
++++++++++++++++++++++++++

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
            get:
                override: true

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

Just below this section we found the endpoints. We can define the rules for
some endpoints. In the next example you can read a typical endpoint.

.. code-block:: yaml

    endpoints:
        /{userId}/books:

And if you need some rule for several endpoints you can use the * wildcard.

.. code-block:: yaml

    endpoints:
        /{userId}/*

Inside the endpoint you can add the request definition, see avobe what items
you can specify.
Every thing that you add just below the endpoint will affect to every method
inside the endpoint.

You can define a path parameter, in this case we need to generate requests
only for the user with id 500, like this:

.. code-block:: yaml

    /{userId}/books:
        pathParams:
            userId: 500

Then we want to change the body of the post call declared inside the
openapi 3, so we must specify the post keyword. And you can add another
request definition.

.. code-block:: yaml

    body:
        name:
            override: true
            type: string
                maxLength: 40

Inside the name of the example we can see another addition to Open Api
specification, the override keyword. This keyword is false by default,
and when it's value is true, then will ignore the complete definition
of the Open Api file.

Another addition to the Open Api specification is the dictionary type.
This type expect to find a values keyword, and will peek one random
element each time that generate a new value:

.. code-block:: yaml

    genre:
        type: dictionary
        values:
            - mistery
            - fiction
            - suspense

If we want to override all settings of the Open Api file you can override
a method and not provide any new rules. This will attend only to your
definition file.

.. code-block:: yaml

    get:
        override: true