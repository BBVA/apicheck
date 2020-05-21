# APICheck Sensitive data service

This service analyzes a Request / Response object and tries to find sensitive
data in both the request and the response (including body and headers) according
to the set of rules provided.

It exposes one entry-point (`/apicheck/sensitive-data`) that can be accessed by
using the HTTP POST method, POST data must be a valid APICheck data object.

# APICheck data object

The object accepted by the service as a JSON payload allows to specify the data
of both request and response for an HTTP request. Here is an full example of
the object.

```json
{
  "_meta": {
    "host": "example.com",
    "schema": "https"
  },
  "request": {
    "url": "https://example.com/echo",
    "version": "1.1",
    "method": "get",
    "headers": {
      "User-Agent": "curl/7.54.0",
      "Accept": "*/*"
    },
    "body": "ewogICAgInVzZXJuYW1lIjogIm1lQG1lLmNvbSIsCiAgICAicGFzc3dvcmQiOiAia3NrbGFzZGYiCn0K"
  },
  "response": {
    "status": 200,
    "reason": "Ok",
    "headers": {},
    "body": "ewogICAgInVzZXJuYW1lIjogIm1lQG1lLmNvbSIsCiAgICAicGFzc3dvcmQiOiAia3NrbGFzZGYiCn0K"
  }
}
```

The body key, in both request and response, must be a string containing the
base64 encoded body (or null if not body is present).


# Rules format

Rules are provided in a YAML file with the following format:

```yaml
- id: core-001
  description: Find plain text password in HTTP responses
  regex: '([pP][aA][sS][sS][wW][oO][rR][dD])'
  severity: Medium
  searchIn: Both  # Allowed values: Response, Request, Both
  includeKeys: true  # Search in Json keys. Values always are inspected
```

The above example is from the core rules file: `core.yaml`:

- Severity values allowed are: High, Medium, Low
- searchIn: Allows to search in the HTTP Request, in the Response or in Both.
- includeKeys: Set if you want to search also in JSON keys.

# Configuration

APICheck Sensitive data comes with a default set of rules, but it can be
replaced by another of your convenience. The *configRuleSet* key allows you to
set an URL pointing to the new set of rules you want to use.

If you encounter problems with false positives you can provide to the server
with a list of rule IDs to be ignored. The *configIgnoreRules* key allows you
to provide this list.
