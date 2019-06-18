from piny import YamlLoader

config = YamlLoader(path="config.yaml").load()
print(config)
# {'db': {'login': 'user', 'password': 'my_db_password'},
# 'mail': {'login': 'user', 'password': 'my_default_password'},
# 'sentry': {'dsn': None}}
