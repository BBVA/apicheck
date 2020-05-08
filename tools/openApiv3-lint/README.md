# openApiv3-lint

Lint the endpoint provided using OpenAPI v3 specification. It will lint from
the file passed as first parameter otherwise it will read the endpoint
definition to lint from standard input.

This tool accepts an endpoint definition written using OpenAPI v3 as input and
will output the same definition, if no errors are encountered, or the list of
errors detected.

In case of error a code of 1 is returned, 0 otherwise.

## Examples

You have an endpoint which definition is in
https://mydomain.com/apis/endpoint.yml. In order to check if it satisfies the
OpenAPI v3 specification you have to invoke the openApiv3-lint tool this way:

curl https://mydomain.com/apis/endpoint.yml | \
     docker run --rm -i openapiv3-lint:1.0.0
