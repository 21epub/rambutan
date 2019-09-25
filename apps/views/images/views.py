from flask import Flask, current_app, abort, render_template
from flask.views import MethodView

from . import images
from .handles.jpg_handle import ImageProcessor
from .mixins import ProcessImageMixin

app = Flask(__name__)
with app.app_context():
    app = current_app


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
    def get(self, filename, size=0):

        if app.storage.is_exist(filename):
            content = app.storage.read(filename)
            return self.resize(content=content, size=size)
        else:
            return abort(404)


class AsciiArtImageView(ProcessImageMixin, MethodView):
    def get(self, filename):
        if app.storage.is_exist(filename):
            content = app.storage.read(filename)
            return render_template("images/aimg.html", aimg=self.to_asciiart(content))
        else:
            return abort(404)


images.add_url_rule(
    "/<filename>/resize/",
    view_func=ResizeImageView.as_view("image-processor-thumbnail"),
)
images.add_url_rule(
    "/<filename>/resize/<int:size>",
    view_func=ResizeImageView.as_view("image-processor"),
)

images.add_url_rule(
    "/<filename>/ascii/", view_func=AsciiArtImageView.as_view("image-ascii")
)
