import re
from pathlib import Path
from unittest import mock

import pytest

from piny import Matcher, MatcherWithDefaults, StrictMatcher, YamlLoader

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
def test_strict_matcher_values_undefined(name):
    config = YamlLoader(
        path=CONF_DIR.joinpath("{}.yaml".format(name)), matcher=StrictMatcher
    ).load()
    assert config[name]["password"] is None


@pytest.mark.parametrize("name", ["db", "mail"])
def test_strict_matcher_values_set(name):
    with mock.patch("piny.loader.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = CONFIG_MAP[name]
        config = YamlLoader(
            path=CONF_DIR.joinpath("{}.yaml".format(name)), matcher=StrictMatcher
        ).load()
        assert config[name]["password"] == CONFIG_MAP[name]


def test_strict_matcher_default_do_not_matched():
    config = YamlLoader(
        path=CONF_DIR.joinpath("defaults.yaml"), matcher=StrictMatcher
    ).load()
    assert config["db"]["password"] is None
    assert (
        config["mail"]["password"] == "${MAIL_PASSWORD:-My123~!@#$%^&*())_+Password!}"
    )
    assert config["logging"]["password"] == "${LOGGING_PASSWORD:-:-test:-}"
    assert config["sentry"]["password"] == "${SENTRY_PASSWORD:-}"


def test_matcher_with_defaults_values_undefined():
    config = YamlLoader(
        path=CONF_DIR.joinpath("defaults.yaml"), matcher=MatcherWithDefaults
    ).load()
    assert config["db"]["password"] is None
    assert config["mail"]["password"] == "My123~!@#$%^&*())_+Password!"
    assert config["logging"]["password"] == ":-test:-"
    assert config["sentry"]["password"] == ""


def test_matcher_with_defaults_values_set():
    with mock.patch("piny.loader.os.environ.get") as expand_mock:
        expand_mock.side_effect = lambda v, _: CONFIG_MAP[v.split("_")[0].lower()]
        config = YamlLoader(
            path=CONF_DIR.joinpath("defaults.yaml"), matcher=MatcherWithDefaults
        ).load()
        assert config["db"]["password"] == CONFIG_MAP["db"]
        assert config["mail"]["password"] == CONFIG_MAP["mail"]
        assert config["sentry"]["password"] == CONFIG_MAP["sentry"]
        assert config["logging"]["password"] == CONFIG_MAP["logging"]


def test_base_matcher():
    """
    WATCH OUT! Black magic of Pytest in action!

    When placed at the beginning of test module this test make all other tests fail.
    Make sure this test is at the bottom!
    """
    with pytest.raises(NotImplementedError):
        with mock.patch(
            "piny.loader.Matcher.matcher", new_callable=mock.PropertyMock
        ) as matcher_mock:
            matcher_mock.return_value = re.compile("")
            YamlLoader(path=CONF_DIR.joinpath("defaults.yaml"), matcher=Matcher).load()
