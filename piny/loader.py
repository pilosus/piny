import os
import re
from typing import Any, Pattern, Type

import yaml

#
# Matchers
#


class Matcher(yaml.SafeLoader):
    """
    Base class for matchers (i.e. yaml loaders)
    """

    matcher: Pattern[str] = re.compile("")

    @staticmethod
    def constructor(loader, node):
        raise NotImplementedError


class StrictMatcher(Matcher):
    """
    Expand an environment variable of form ${VAR} with its value

    If value is not set return None.
    """

    matcher = re.compile(r"\$\{([^}^{^:]+)\}")

    @staticmethod
    def constructor(loader, node):
        match = StrictMatcher.matcher.match(node.value)
        return os.environ.get(match.groups()[0])  # type: ignore


class MatcherWithDefaults(Matcher):
    """
    Expand an environment variable with its value

    Forms supported: ${VAR}, ${VAR:-default}
    If value is not set and no default value given return None.
    """

    matcher = re.compile(r"\$\{([a-zA-Z_$0-9]+)(:-.*)?\}")

    @staticmethod
    def constructor(loader, node):
        match = MatcherWithDefaults.matcher.match(node.value)
        variable, default = match.groups()  # type: ignore

        if default:
            # lstrip() is dangerous!
            # It can remove legitimate first two letters in a value starting with `:-`
            default = default[2:]

        return os.environ.get(variable, default)


#
# Main
#


class YamlLoader:
    """
    Load YAML configuration file
    """

    def __init__(self, path: str, matcher: Type[Matcher] = MatcherWithDefaults) -> None:
        self.path = path
        self.matcher = matcher

    def _init_resolvers(self):
        self.matcher.add_implicit_resolver("!env", self.matcher.matcher, None)
        self.matcher.add_constructor("!env", self.matcher.constructor)

    def load(self) -> Any:
        """
        Return Python object loaded from the YAML-file
        """
        self._init_resolvers()
        with open(self.path) as fh:
            load = yaml.load(fh, Loader=self.matcher)
        return load
