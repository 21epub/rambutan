import logging
import logging.handlers

from flask import Flask
from flask_bootstrap import Bootstrap
from werkzeug.routing import BaseConverter

from flask_storage.local_storage import FileStorage
from instance.config import app_config


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")

    # app.config.from_mapping(
    #     SECRET_KEY="dev",
    #     # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    register_extensions(app)
    register_blueprints(app)
    register_logging(app)

    return app


def register_extensions(app):
    app.storage = FileStorage(app)
    Bootstrap(app)
    app.url_map.converters["regex"] = RegexConverter


def register_blueprints(app):
    from apps.views.images import images as images_url

    app.register_blueprint(images_url)


def register_logging(app):
    handler = logging.handlers.RotatingFileHandler(
        "/tmp/flask.log", maxBytes=1024 * 1024
    )
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


__version__ = "0.1.3"
