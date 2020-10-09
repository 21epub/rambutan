import re

from flask import Flask, current_app, abort
from flask.views import MethodView

from . import images
from .mixins import ProcessImageMixin

app = Flask(__name__)
with app.app_context():
    app = current_app

image_size_map = {
    "origin": 0,
    "thumb": 320,
    "large": 1024,
    "hd": 2048
}

image_pattern = re.compile(r".*-(thumb|large|hd)$", re.IGNORECASE)


def image_config() -> dict:
    image_config = app.config.get("IMAGE_CONFIG", {})
    return image_config


def get_thumbnail_size() -> int:
    thumbnail_size = image_config()["thumbnail_size"]
    if not isinstance(thumbnail_size, int):
        raise Exception
    return thumbnail_size


def get_quality_size() -> int:
    thumbnail_size = image_config()["quality"]
    if not isinstance(thumbnail_size, int):
        raise Exception
    return thumbnail_size


class ResizeImageView(ProcessImageMixin, MethodView):
    def get(self, filename):

        _filename, _size_string = self.process_filename(filename)
        if _size_string in image_size_map:
            _size = image_size_map[_size_string]
        else:
            return abort(401)

        if app.storage.is_exist(_filename):
            content = app.storage.read(_filename)
            return self.resize(content=content, size=_size)
        else:
            return abort(404)


images.add_url_rule(
    "/<regex('.*'):filename>",
    view_func=ResizeImageView.as_view("image-processor"),
)
