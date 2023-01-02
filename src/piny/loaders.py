from typing import IO, Any, Type, Union

import yaml

from .errors import LoadingError
from .matchers import Matcher, MatcherWithDefaults
from .validators import Validator

#
# Loader
#


class YamlLoader:
    """
    YAML configuration file loader
    """

    def __init__(
        self,
        path: str,
        *,
        matcher: Type[Matcher] = MatcherWithDefaults,
        validator: Union[Type[Validator], None] = None,
        schema: Any = None,
        **schema_params,
    ) -> None:
        """
        Initialize YAML loader

        :param path: string with path to YAML-file
        :param matcher: matcher class
        :param validator: validator class for one of the supported validation libraries
        :param schema: validation schema for the validator of choice
        :param schema_params: named arguments used as optional validation schema params
        """
        self.path = path
        self.matcher = matcher
        self.validator = validator
        self.schema = schema
        self.schema_params = schema_params

    def _init_resolvers(self):
        self.matcher.add_implicit_resolver("!env", self.matcher.matcher, None)
        self.matcher.add_constructor("!env", self.matcher.constructor)

    def load(self, **params) -> Any:
        """
        Return Python object loaded (optionally validated) from the YAML-file

        :param params: named arguments used as optional loading params in validation
        """
        self._init_resolvers()
        try:
            with open(self.path) as fh:
                load = yaml.load(fh, Loader=self.matcher)
        except (yaml.YAMLError, FileNotFoundError) as e:
            raise LoadingError(origin=e, reason=str(e))

        if (self.validator is not None) and (self.schema is not None):
            return self.validator(self.schema, **self.schema_params).load(
                data=load, **params
            )
        return load


class YamlStreamLoader(YamlLoader):
    """
    YAML configuration loader for IO streams, e.g. file objects or stdin
    """

    def __init__(
        self,
        stream: Union[str, IO[str]],
        *,
        matcher: Type[Matcher] = MatcherWithDefaults,
        validator: Union[Type[Validator], None] = None,
        schema: Any = None,
        **schema_params,
    ) -> None:
        self.stream = stream
        self.matcher = matcher
        self.validator = validator
        self.schema = schema
        self.schema_params = schema_params

    def load(self, **params) -> Any:
        self._init_resolvers()
        try:
            load = yaml.load(self.stream, Loader=self.matcher)
        except yaml.YAMLError as e:
            raise LoadingError(origin=e, reason=str(e))

        if (self.validator is not None) and (self.schema is not None):
            return self.validator(self.schema, **self.schema_params).load(
                data=load, **params
            )
        return load
