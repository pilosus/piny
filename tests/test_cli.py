from unittest import mock

import pytest
import yaml
from click.testing import CliRunner

from piny import LoadingError
from piny.cli import cli

from . import config_directory


def test_cli_input_stdin_output_stdout():
    runner = CliRunner()
    with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = "MySecretPassword"
        result = runner.invoke(cli, input="password: ${DB_PASSWORD}")

        assert result.exit_code == 0
        assert result.stdout == "password: MySecretPassword\n"


def test_cli_input_file_output_file():
    runner = CliRunner()
    with open(config_directory.joinpath("db.yaml"), "r") as f:
        input_lines = f.readlines()

    with runner.isolated_filesystem():
        with open("input.yaml", "w") as input_fd:
            input_fd.writelines(input_lines)

        with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
            expand_mock.return_value = "MySecretPassword"
            result = runner.invoke(cli, ["input.yaml", "output.yaml"])

            with open("output.yaml", "r") as output_fd:
                output_lines = output_fd.readlines()

            assert result.exit_code == 0
            assert "password: MySecretPassword" in map(
                lambda x: x.strip(), output_lines
            )


def test_cli_fail():
    runner = CliRunner()
    with mock.patch("piny.loaders.yaml.load") as loader_mock:
        loader_mock.side_effect = yaml.YAMLError("Oops!")
        result = runner.invoke(cli, input="password: ${DB_PASSWORD}")
        assert result.exit_code == 1
        assert type(result.exception) == LoadingError
