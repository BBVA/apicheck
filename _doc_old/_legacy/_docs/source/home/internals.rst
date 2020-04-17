Internals
=========

Pipelines & data flow
---------------------

Pipelines
+++++++++

In \*NIX, you can chain multiple commands together in a *pipeline*. Consider this one:

.. image:: /_static/images/apicheck_unix_pipeline.png
   :align: center


In a similar fashion you can build ``APICheck`` *pipelines* chaining :samp:`commands` and :samp:`tools`. For example:

.. image:: /_static/images/apicheck_unix_pipeline.png
   :align: center

.. _data_format:

Data format
+++++++++++

To allow interoperation among :samp:`commands` and :samp:`tools`, all of them share a common :samp:`JSON` data format. In other words, ``APICheck`` commands output :samp:`JSON`, and accept it as input, too. This allows to build pipelines (as we showed in the previous section).

Commands and Tools

.. image:: /_static/images/apicheck_002_json_flow.png
   :width: 300px
   :align: center


Commands & tools
----------------

``APICheck`` components fall into two categories:

- Commands
- Tools

.. _commands_reference:

Commands
++++++++

Commands are programs with well-defined small jobs. Commands follow the \*NIX philosophy: multiple small elements that can be connected together.

You can compare those commands to ``awk`` or ``grep``. Small, but powerful.

.. _tools_reference:

Tools
+++++

Tools are more complex than plain commands. The problems they tackle are harder. You also can chain them together along with commands.

.. _data_generation:

Data generation
---------------

Data generation tools are placed inside the `apicheck.core.generator` package. For instance, `apicheck.core.generator.open_api_strategy`, that implements the default data generation strategy for OpenAPI files.

.. note::
    At the moment, string formating is not supported.

The generator uses a Python package named ``Faker`` to generate fake data following the OpenAPI specification.

Request definition
++++++++++++++++++

A request definition describes, in a very simple terms, how the request will look like.
This definition always have the same fields:

.. code-block:: yaml

    headers:
        [value or type]
    pathParams:
        [value or type]
    queryParams:
        [value or type]
    body:
        [value or type]

The headers are a set of key-values that can hold two types of values, either a fixed
value or a type definition.

The fixed value looks like the following:

.. code-block:: yaml

    userId: 500

Type definition
+++++++++++++++

The type used in ``APICheck`` is a direct copy of the type definition of OpenAPI 3
specification.
Every item can be defined as an OpenAPI type. You can use custom
types created for ``APICheck`` also. One of the allowed types is *dictionary*, that looks like:

.. code-block:: yaml

    type: dictionary
    values:
        - A
        - B
        - C

The definition of the *userName* field would look like:

.. code-block:: yaml

    userName:
        type: dictionary
        values:
            - A
            - B
            - C

Definition hierarchy
++++++++++++++++++++

If several definitions for the same element are found, the last one read will
remain in effect. The default precedence order when reading is:

    - Open Api 3 File
    - Rules files (read in search order)
    - Global tag inside rule
    - Request definition inside endpoint
    - Request definition inside method

Definition override
+++++++++++++++++++

When starting a type definition from scratch, we must use the *override* keyword. The value of this keyword is *false* by default. When set to *true*, the generator will use only our specification and ignore the OpenAPI specification.

OpenAPI 3 override Example
++++++++++++++++++++++++++

You can override OpenAPI 3 type definitions using your own file like this:

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

The first part is metadata. You can query ``APICheck`` to get the set of
rules that apply to this data. Name and version are required, any other datum is
optional.

.. code-block:: yaml

    name: "my library api"
    description: "my awesome library api"
    version: "0.9-RC"
    tags:
        - books
        - users

The global section defines a request used as a template for all other rules.
When you include a header in this section, all requests regarding these rules
will include this value.

.. code-block:: yaml

    global:
        headers:
            Authorization: Basic YWxhZGRpbjpvcGVuc2VzYW1l

Just below this section we find the endpoints. We can define rules for
the endpoints. In the next example you can see a typical endpoint
definition.

.. code-block:: yaml

    endpoints:
        /{userId}/books:

If you need a single rule to affect multiple endpoints at the same time, you can use the \* *wildcard*.

.. code-block:: yaml

    endpoints:
        /{userId}/*

Below the endpoint you can add a request definition. The items you can set
are listed above.
Everything you add just below the endpoint will affect every method
inside the endpoint.

A path parameter can also be defined. For instance, in this example we want to generate requests only for the user whose id is 500:

.. code-block:: yaml

    /{userId}/books:
        pathParams:
            userId: 500

And if we wanted to change the body of the POST call declared inside the
OpenAPI 3, we should specify the ``post`` keyword. After which you can add another
request definition.

.. code-block:: yaml

    body:
        name:
            override: true
            type: string
                maxLength: 40

If we want to override all settings of the OpenAPI file, you can override
a method and not provide any new rules. This will only affect that
definition file.

.. code-block:: yaml

    get:
        override: true
