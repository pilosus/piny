from typing import Any


class PinyErrorMixin:
    msg_template: str

    def __init__(self, origin: Exception = None, **context: Any) -> None:
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
    pass


class LoadingError(ConfigError):
    msg_template = "Loading YAML file failed: {reason}"


class ValidationError(ConfigError):
    msg_template = "Validation failed: {reason}"
