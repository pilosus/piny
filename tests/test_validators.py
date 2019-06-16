from typing import Optional
from unittest import mock

import pytest
import trafaret
from marshmallow import Schema, fields
from pydantic import BaseModel

from piny import (
    MarshmallowValidator,
    PydanticValidator,
    StrictMatcher,
    TrafaretValidator,
    ValidationError,
    YamlLoader,
)

from . import config_directory, config_map

#
# Const
#


class PydanticDB(BaseModel):
    host: str
    login: str
    password: str


class PydanticConfig(BaseModel):
    db: PydanticDB


class MarshmallowDB(Schema):
    host = fields.String(required=True)
    login = fields.String(required=True)
    password = fields.String(required=True)


class MarshmallowConfig(Schema):
    db = fields.Nested(MarshmallowDB, required=True)


TrafaretDB = trafaret.Dict(
    host=trafaret.String, login=trafaret.String, password=trafaret.String
)
TrafaretConfig = trafaret.Dict(db=TrafaretDB)


#
# Tests
#


@pytest.mark.parametrize("name", ["db"])
def test_pydantic_validator_success(name):
    with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = config_map[name]
        config = YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=PydanticValidator,
            validator_schema=PydanticConfig,
        ).load()

        assert config[name]["host"] == "db.example.com"
        assert config[name]["login"] == "user"
        assert config[name]["password"] == config_map[name]


@pytest.mark.parametrize("name", ["db"])
def test_pydantic_validator_fail(name):
    with pytest.raises(ValidationError, match=r"db -> password"):
        YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=PydanticValidator,
            validator_schema=PydanticConfig,
        ).load()


@pytest.mark.parametrize("name", ["db"])
def test_marshmallow_validator_success(name):
    with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = config_map[name]
        config = YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=MarshmallowValidator,
            validator_schema=MarshmallowConfig,
        ).load()

        assert config[name]["host"] == "db.example.com"
        assert config[name]["login"] == "user"
        assert config[name]["password"] == config_map[name]


@pytest.mark.parametrize("name", ["db"])
def test_marshmallow_validator_fail(name):
    with pytest.raises(
        ValidationError, match=r"\{'db': \{'password': \['Field may not be null.'\]\}\}"
    ):
        YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=MarshmallowValidator,
            validator_schema=MarshmallowConfig,
            validator_params=dict(strict=True),
        ).load(params=dict(many=False))


@pytest.mark.parametrize("name", ["db"])
def test_trafaret_validator_success(name):
    with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = config_map[name]
        config = YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=TrafaretValidator,
            validator_schema=TrafaretConfig,
        ).load()

        assert config[name]["host"] == "db.example.com"
        assert config[name]["login"] == "user"
        assert config[name]["password"] == config_map[name]


@pytest.mark.parametrize("name", ["db"])
def test_trafaret_validator_fail(name):
    with pytest.raises(
        ValidationError,
        match=r"\{'db': DataError\(\{'password': DataError\(value is not a string\)\}\)\}",
    ):
        YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=TrafaretValidator,
            validator_schema=TrafaretConfig,
        ).load()
