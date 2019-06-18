from pydantic import BaseModel
from piny import PydanticValidator, StrictMatcher, YamlLoader


class DBModel(BaseModel):
    login: str
    password: str


class ConfigModel(BaseModel):
    db: DBModel


config = YamlLoader(
    path="database.yaml",
    matcher=StrictMatcher,
    validator=PydanticValidator,
    schema=ConfigModel,
).load()
