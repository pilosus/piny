from typing import Any, Optional


class PinyErrorMixin:
    """
    Mixin class to wrap and format original exception
    """

    msg_template: str

    def __init__(self, origin: Optional[Exception] = None, **context: Any) -> None:
        """
        Mixing for wrapping original exception

        :param origin: original exception,
               may be helpful when special method invocation needed
        :param context: mapping used for exception message formatting
        """
        self.origin = origin
        self.context = context or None
        super().__init__()

    def __str__(self) -> str:
        return self.msg_template.format(**self.context or {})


class ConfigError(PinyErrorMixin, Exception):
    """
    Base class for Piny exceptions
    """

    pass


class LoadingError(ConfigError):
    """
    Exception for reading or parsing configuration file errors
    """

    msg_template = "Loading YAML file failed: {reason}"


class ValidationError(ConfigError):
    """
    Exception for data validation errors
    """

    msg_template = "Validation failed: {reason}"
