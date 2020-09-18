from flask import Flask
from flask_bootstrap import Bootstrap

from instance.config import app_config

from flask_storage.local_storage import FileStorage


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

    return app


def register_extensions(app):
    app.storage = FileStorage(app)
    Bootstrap(app)


def register_blueprints(app):
    from apps.views.images import images as images_url

    app.register_blueprint(images_url)


__version__ = "0.1.0"
