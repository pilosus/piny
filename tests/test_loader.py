from pathlib import Path
from unittest import mock

import pytest

from piny import MatcherWithDefaults, StrictMatcher, YamlLoader

#
# Constants
#

CONF_DIR = Path(__file__).resolve().parent.joinpath("configs")

CONFIG_MAP = {
    "db": "my_db_password",
    "mail": "my_mail_password",
    "sentry": "my_sentry_password",
    "logging": "my_logging_password",
}


#
# Tests
#


@pytest.mark.parametrize("name", ["db", "mail"])
def test_env_loader_values_undefined(name):
    config = YamlLoader(
        path=CONF_DIR.joinpath("{}.yaml".format(name)), matcher=StrictMatcher
    ).load()
    assert config[name]["password"] is None


@pytest.mark.parametrize("name", ["db", "mail"])
def test_env_loader_values_set(name):
    with mock.patch("piny.loader.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = CONFIG_MAP[name]
        config = YamlLoader(
            path=CONF_DIR.joinpath("{}.yaml".format(name)), matcher=StrictMatcher
        ).load()
        assert config[name]["password"] == CONFIG_MAP[name]


def test_env_loader_defaults_values_undefined():
    config = YamlLoader(
        path=CONF_DIR.joinpath("defaults.yaml"), matcher=MatcherWithDefaults
    ).load()
    assert config["db"]["password"] is None
    assert config["mail"]["password"] == "My123~!@#$%^&*())_+Password!"
    assert config["logging"]["password"] == ":-test:-"
    assert config["sentry"]["password"] == ""


def test_env_loader_defaults_values_set():
    with mock.patch("piny.loader.os.environ.get") as expand_mock:
        expand_mock.side_effect = lambda v, _: CONFIG_MAP[v.split("_")[0].lower()]
        config = YamlLoader(
            path=CONF_DIR.joinpath("defaults.yaml"), matcher=MatcherWithDefaults
        ).load()
        assert config["db"]["password"] == CONFIG_MAP["db"]
        assert config["mail"]["password"] == CONFIG_MAP["mail"]
        assert config["sentry"]["password"] == CONFIG_MAP["sentry"]
        assert config["logging"]["password"] == CONFIG_MAP["logging"]
