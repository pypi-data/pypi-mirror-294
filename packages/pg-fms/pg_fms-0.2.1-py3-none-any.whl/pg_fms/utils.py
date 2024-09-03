from builtins import BaseException, BaseExceptionGroup


def get_utf8_string(value: str) -> str:
    """
    Get a UTF-8 encoded string.
    """
    return value.encode("utf-8").decode("utf-8")


class CliException(BaseException):
    """A CLI exception."""


class CliExceptionGroup(BaseExceptionGroup):
    """A CLI exception group."""


class CliError(CliException):
    """A CLI error."""


class CliWarning(CliException):
    """A CLI warning."""


class CliInfo(CliException):
    """A CLI info."""
