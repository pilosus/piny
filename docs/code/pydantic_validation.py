from pydantic import BaseModel
from piny import PydanticV2Validator, StrictMatcher, YamlLoader

# Watch out!
# Pydantic V2 deprecated some model's methods:
# https://docs.pydantic.dev/2.0/migration/
#
# For Pydantic v2 use `PydanticV2Validator`
# For Pydantic v1 use `PydanticValidator`

class DBModel(BaseModel):
    login: str
    password: str


class ConfigModel(BaseModel):
    db: DBModel


config = YamlLoader(
    path="database.yaml",
    matcher=StrictMatcher,
    validator=PydanticV2Validator,
    schema=ConfigModel,
).load()
