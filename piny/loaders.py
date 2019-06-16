from typing import Any, Dict, Type

import yaml

from .errors import LoadingError
from .matchers import Matcher, MatcherWithDefaults
from .validators import Validator

#
# Types
#

Params = Dict[str, Any]


#
# Loader
#


class YamlLoader:
    """
    Load YAML configuration file
    """

    def __init__(
        self,
        path: str,
        matcher: Type[Matcher] = MatcherWithDefaults,
        validator: Type[Validator] = None,
        validator_schema: Any = None,
        validator_params: Params = None,
    ) -> None:
        self.path = path
        self.matcher = matcher
        self.validator = validator
        self.validator_schema = validator_schema
        self.validator_params = validator_params

    def _init_resolvers(self):
        self.matcher.add_implicit_resolver("!env", self.matcher.matcher, None)
        self.matcher.add_constructor("!env", self.matcher.constructor)

    def load(self, params: Params = None) -> Any:
        """
        Return Python object loaded from the YAML-file
        """
        self._init_resolvers()
        try:
            with open(self.path) as fh:
                load = yaml.load(fh, Loader=self.matcher)
        except (yaml.YAMLError, FileNotFoundError) as e:
            raise LoadingError(origin=e, reason=str(e))

        # Optional validation
        if (self.validator is not None) and (self.validator_schema is not None):
            # Make sure default params is a mapping
            self.validator_params = self.validator_params or {}
            params = params or {}
            return self.validator(self.validator_schema, **self.validator_params).load(
                data=load, **params
            )
        return load
