import trafaret
from piny import TrafaretValidator, StrictMatcher, YamlLoader


DBSchema = trafaret.Dict(login=trafaret.String, password=trafaret.String)
ConfigSchema = trafaret.Dict(db=DBSchema)

config = YamlLoader(
    path="database.yaml",
    matcher=StrictMatcher,
    validator=TrafaretValidator,
    schema=ConfigSchema,
).load()
