import marshmallow as ma
from piny import MarshmallowValidator, StrictMatcher, YamlLoader


class DBSchema(ma.Schema):
    login = ma.fields.String(required=True)
    password = ma.fields.String()


class ConfigSchema(ma.Schema):
    db = ma.fields.Nested(DBSchema)


config = YamlLoader(
    path="database.yaml",
    matcher=StrictMatcher,
    validator=MarshmallowValidator,
    schema=ConfigSchema,
).load(many=False)
