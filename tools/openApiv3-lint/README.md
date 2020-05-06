# openApiv3-lint

Lint the endpoint provided using OpenAPI v3 spec. It will lint from the file
passed as first parameter otherwise it will read the endpoint specification to
lint from standard input.

This tool accepts an endpoint specification written using OpenAPI v3 as input
and outputs the same specification, if no erros are encounterd, or the list of
errors deteted.

In case of error an error code of 1 is returned, 0 otherwise.
