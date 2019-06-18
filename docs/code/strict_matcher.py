from piny import YamlLoader, StrictMatcher

config = YamlLoader(path="config.yaml", matcher=StrictMatcher).load()
