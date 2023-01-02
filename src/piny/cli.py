from typing import Any

import click
import yaml

from .loaders import YamlStreamLoader
from .matchers import MatcherWithDefaults, StrictMatcher

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("input", required=False, type=click.File("r"))
@click.argument("output", required=False, type=click.File("w"))
@click.option(
    "--strict/--no-strict", default=True, help="Enable or disable strict matcher"
)
def cli(input, output, strict) -> Any:
    """
    Substitute environment variables with their values.

    Read INPUT, find environment variables in it,
    substitute them with their values and write to OUTPUT.

    INPUT and OUTPUT can be files or standard input and output respectively.
    With no INPUT, or when INPUT is -, read standard input.
    With no OUTPUT, or when OUTPUT is -, write to standard output.

    Examples:

    \b
    piny input.yaml output.yaml
    piny - output.yaml
    piny input.yaml -
    tail -n 12 input.yaml | piny > output.yaml
    """
    stdin = click.get_text_stream("stdin")
    stdout = click.get_text_stream("stdout")

    config = YamlStreamLoader(
        stream=input or stdin, matcher=StrictMatcher if strict else MatcherWithDefaults
    ).load()

    yaml.dump(config, output or stdout)
