class ApitestError(Exception):  # noqa
    pass


class ApitestMissingDataError(Exception):
    pass


class ApitestInvalidFormatError(Exception):
    pass


class ApitestValueError(ValueError):
    pass


class ApitestTypeError(TypeError):
    pass


class ApitestUnknownTypeError(TypeError):
    pass


class ApitestConnectionError(ConnectionError):
    pass


class ApitestNotFoundError(FileNotFoundError):
    pass


__all__ = ("ApitestError", "ApitestValueError", "ApitestTypeError",
           "ApitestUnknownTypeError", "ApitestConnectionError", "ApitestInvalidFormatError",
           "ApitestNotFoundError", "ApitestMissingDataError")
