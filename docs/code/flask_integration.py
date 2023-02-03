from flask import Flask
from flask.logging import default_handler
from piny import YamlLoader, StrictMatcher, PydanticValidator
from pydantic import BaseModel, validator
from typing import Any, Dict, Optional
from werkzeug.serving import run_simple
import logging
import sys

#
# Validation
#


class AppSettings(BaseModel):
    company: str
    secret: str
    max_content_len: Optional[int] = None
    debug: bool = False
    testing: bool = False


class LoggingSettings(BaseModel):
    fmt: str
    date_fmt: str
    level: str

    @validator("level")
    def validate_name(cls, value):
        upper = value.upper()
        if upper not in logging._nameToLevel:
            raise ValueError("Invalid logging level")
        return upper


class Configuration(BaseModel):
    app: AppSettings
    logging: LoggingSettings


#
# Helpers
#


def configure_app(app: Flask, configuration: Dict[str, Any]) -> None:
    """
    Apply configs to application
    """
    app.settings = configuration
    app.secret_key = app.settings["app"]["secret"].encode("utf-8")


def configure_logging(app: Flask) -> None:
    """
    Configure app's logging
    """
    app.logger.removeHandler(default_handler)
    log_formatter = logging.Formatter(
        fmt=app.settings["logging"]["fmt"], datefmt=app.settings["logging"]["date_fmt"]
    )
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(app.settings["logging"]["level"])
    app.logger.addHandler(log_handler)


#
# Factory
#


def create_app(path: str) -> Flask:
    """
    Application factory
    """
    # Get and validate config
    config = YamlLoader(
        path=path,
        matcher=StrictMatcher,
        validator=PydanticValidator,
        schema=Configuration,
    ).load()

    # Initialize app
    app = Flask(__name__)

    # Configure app
    configure_app(app, config)
    configure_logging(app)

    return app


if __name__ == "__main__":
    app = create_app(sys.argv[1])

    @app.route("/")
    def hello():
        return "Hello World!"

    # Run application:
    # $ python flask_integration.py your-config.yaml
    run_simple(hostname="localhost", port=5000, application=app)
