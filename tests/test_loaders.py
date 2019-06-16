import re
import pytest
from unittest import mock
from piny import Matcher, MatcherWithDefaults, StrictMatcher, YamlLoader
from . import config_directory, config_map


@pytest.mark.parametrize("name", ["db", "mail"])
def test_strict_matcher_values_undefined(name):
    config = YamlLoader(
        path=config_directory.joinpath("{}.yaml".format(name)), matcher=StrictMatcher
    ).load()
    assert config[name]["password"] is None


@pytest.mark.parametrize("name", ["db", "mail"])
def test_strict_matcher_values_set(name):
    with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = config_map[name]
        config = YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)), matcher=StrictMatcher
        ).load()
        assert config[name]["password"] == config_map[name]


def test_strict_matcher_default_do_not_matched():
    config = YamlLoader(
        path=config_directory.joinpath("defaults.yaml"), matcher=StrictMatcher
    ).load()
    assert config["db"]["password"] is None
    assert (
        config["mail"]["password"] == "${MAIL_PASSWORD:-My123~!@#$%^&*())_+Password!}"
    )
    assert config["logging"]["password"] == "${LOGGING_PASSWORD:-:-test:-}"
    assert config["sentry"]["password"] == "${SENTRY_PASSWORD:-}"


def test_matcher_with_defaults_values_undefined():
    config = YamlLoader(
        path=config_directory.joinpath("defaults.yaml"), matcher=MatcherWithDefaults
    ).load()
    assert config["db"]["password"] is None
    assert config["mail"]["password"] == "My123~!@#$%^&*())_+Password!"
    assert config["logging"]["password"] == ":-test:-"
    assert config["sentry"]["password"] == ""


def test_matcher_with_defaults_values_set():
    with mock.patch("piny.matchers.os.environ.get") as expand_mock:
        expand_mock.side_effect = lambda v, _: config_map[v.split("_")[0].lower()]
        config = YamlLoader(
            path=config_directory.joinpath("defaults.yaml"), matcher=MatcherWithDefaults
        ).load()
        assert config["db"]["password"] == config_map["db"]
        assert config["mail"]["password"] == config_map["mail"]
        assert config["sentry"]["password"] == config_map["sentry"]
        assert config["logging"]["password"] == config_map["logging"]


def test_base_matcher():
    """
    WATCH OUT! Black magic of Pytest in action!

    When placed at the beginning of test module this test make all other tests fail.
    Make sure this test is at the bottom!
    """
    with pytest.raises(NotImplementedError):
        with mock.patch(
            "piny.matchers.Matcher.matcher", new_callable=mock.PropertyMock
        ) as matcher_mock:
            matcher_mock.return_value = re.compile("")
            YamlLoader(path=config_directory.joinpath("defaults.yaml"), matcher=Matcher).load()
