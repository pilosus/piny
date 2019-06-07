import os
import re
from typing import Any, Type

import yaml

#
# Helpers
#


class EnvLoader(yaml.SafeLoader):
    matcher = re.compile(r"\$\{([^}^{]+)\}")

    @staticmethod
    def constructor(loader, node):
        """
        Expand an environment variable of form ${VAR} with its value

        If value is not set return variable name as a string.
        """
        return os.path.expandvars(node.value)


class EnvDefaultsLoader(EnvLoader):
    matcher = re.compile(r"\$\{([a-zA-Z_$0-9]+)(:-.*)?\}")

    @staticmethod
    def constructor(loader, node):
        """
        Expand an environment variable with its value

        Forms supported: ${VAR}, ${VAR:-default}
        If value is not set and no default value given return None.
        """
        match = EnvDefaultsLoader.matcher.match(node.value)
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

    def __init__(self, path: str, loader: Type[EnvLoader] = EnvDefaultsLoader) -> None:
        self.path = path
        self.loader = loader

    def _init_resolvers(self):
        self.loader.add_implicit_resolver("!env", self.loader.matcher, None)
        self.loader.add_constructor("!env", self.loader.constructor)

    def load(self) -> Any:
        """
        Return Python object loaded from the YAML-file
        """
        self._init_resolvers()
        with open(self.path) as fh:
            load = yaml.load(fh, Loader=self.loader)
        return load
