from pathlib import Path
from unittest import mock

import pytest

from piny import EnvDefaultsLoader, EnvLoader, YamlLoader

#
# Constants
#

CONF_DIR = Path(__file__).resolve().parent.joinpath("configs")

CONFIG_MAP = {
    "db": ("my_db_password", "${DB_PASSWORD}"),
    "mail": ("my_mail_password", "${MAIL_PASSWORD}"),
    "sentry": ("my_sentry_password", "${SENTRY_PASSWORD}"),
    "logging": ("my_logging_password", "${LOGGING_PASSWORD}"),
}

CONIG_REVERSE = {
    "DB_PASSWORD": "my_db_password",
    "MAIL_PASSWORD": "my_mail_password",
    "SENTRY_PASSWORD": "my_sentry_password",
    "LOGGING_PASSWORD": "my_logging_password",
}


#
# Tests
#


@pytest.mark.parametrize("name", ["db", "mail"])
def test_env_loader_values_undefined(name):
    config = YamlLoader(
        path=CONF_DIR.joinpath("{}.yaml".format(name)), loader=EnvLoader
    ).load()
    assert config[name]["password"] == CONFIG_MAP[name][1]


@pytest.mark.parametrize("name", ["db", "mail"])
def test_env_loader_values_set(name):
    with mock.patch("piny.loader.EnvLoader.constructor") as expand_mock:
        expand_mock.return_value = CONFIG_MAP[name][0]
        config = YamlLoader(
            path=CONF_DIR.joinpath("{}.yaml".format(name)), loader=EnvLoader
        ).load()
        assert config[name]["password"] == CONFIG_MAP[name][0]


def test_env_loader_defaults_values_undefined():
    config = YamlLoader(
        path=CONF_DIR.joinpath("defaults.yaml"), loader=EnvDefaultsLoader
    ).load()
    assert config["db"]["password"] is None
    assert config["mail"]["password"] == "My123~!@#$%^&*())_+Password!"
    assert config["logging"]["password"] == ":-test:-"
    assert config["sentry"]["password"] == ""


def test_env_loader_defaults_values_set():
    with mock.patch("piny.loader.os.environ.get") as expand_mock:
        expand_mock.side_effect = lambda v, _: CONIG_REVERSE[v]
        config = YamlLoader(
            path=CONF_DIR.joinpath("defaults.yaml"), loader=EnvDefaultsLoader
        ).load()
        assert config["db"]["password"] == CONIG_REVERSE["DB_PASSWORD"]
        assert config["mail"]["password"] == CONIG_REVERSE["MAIL_PASSWORD"]
        assert config["sentry"]["password"] == CONIG_REVERSE["SENTRY_PASSWORD"]
        assert config["logging"]["password"] == CONIG_REVERSE["LOGGING_PASSWORD"]
