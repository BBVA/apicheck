# jwt-checker

Chech that JWT tokens (only, does not support JWS or JWE yet) have been issued
following the best practices.

This tool accepts a JWT token provided as an argument and passes some check
over it. It supports checks over the header and standard claims fields in
addition to signature verification. It supports the following parameters:

- -h                 show help message and exit
- -V                 show version info and exit
- -unsig             don't raise an error if token is unsigned (algorithm "none")
- -allowAlg value    raise an error if token has different signing algorithm. Provide several options if you want to allow more than one algorithm
- -audience string   raise an error if token has different audience
- -expiresAt string  raise an error if the expiration date is after this. Format: YYYY-MM-DDThh:mm:ss
- -issuer string     raise an error if token has different issuer
- -notBefore string  raise an error if the not before date is priot to this. Format: YYYY-MM-DDThh:mm:ss
- -secret string     use this secret to validate the sign. Base64 encoded (mandatory when validating signed tokens)
- -subject string    raise an error if token has different subject

In case of error an error code of 1 is returned, 0 otherwise.
