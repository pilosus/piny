from marshmallow import fields, Schema
from pydantic import BaseModel
from typing import Optional
from unittest import mock

from piny import PydanticValidator, MarshmallowValidator, YamlLoader, StrictMatcher, ValidationError
from . import config_directory, config_map

import pytest

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


#
# Tests
#


@pytest.mark.parametrize("name", ["db", ])
def test_pydantic_validator_success(name):
    with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = config_map[name]
        config = YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=PydanticValidator,
            validator_schema=PydanticConfig
        ).load()

        assert config[name]["host"] == "db.example.com"
        assert config[name]["login"] == "user"
        assert config[name]["password"] == config_map[name]


@pytest.mark.parametrize("name", ["db", ])
def test_pydantic_validator_fail(name):
    with pytest.raises(ValidationError, match=r"db -> password"):
        YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=PydanticValidator,
            validator_schema=PydanticConfig
        ).load()


@pytest.mark.parametrize("name", ["db", ])
def test_marshmallow_validator_success(name):
    with mock.patch("piny.matchers.StrictMatcher.constructor") as expand_mock:
        expand_mock.return_value = config_map[name]
        config = YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=MarshmallowValidator,
            validator_schema=MarshmallowConfig
        ).load()

        assert config[name]["host"] == "db.example.com"
        assert config[name]["login"] == "user"
        assert config[name]["password"] == config_map[name]


@pytest.mark.parametrize("name", ["db", ])
def test_marshmallow_validator_fail(name):
    with pytest.raises(ValidationError, match=r"\{'db': \{'password': \['Field may not be null.'\]\}\}"):
        YamlLoader(
            path=config_directory.joinpath("{}.yaml".format(name)),
            matcher=StrictMatcher,
            validator=MarshmallowValidator,
            validator_schema=MarshmallowConfig,
            validator_params=dict(strict=True)
        ).load()
