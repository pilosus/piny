import os
import re
from typing import Pattern

import yaml


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
