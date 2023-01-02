from pathlib import Path

config_directory = Path(__file__).resolve().parent.joinpath("configs")

config_map = {
    "db": "my_db_password",
    "mail": "my_mail_password",
    "sentry": "my_sentry_password",
    "logging": "my_logging_password",
}
