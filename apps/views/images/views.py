from flask import Flask, current_app, abort, Response
from flask.views import MethodView

from . import images
from .mixins import ProcessImageMixin

app = Flask(__name__)
with app.app_context():
    app = current_app

image_size_map = {
    "thumb": 320,
    "large": 1024,
    "hd": 2048
}


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


class OriginImageView(MethodView):

    def get(self, filename):
        if app.storage.is_exist(filename):
            content = app.storage.read(filename)
            return Response(content, content_type="image/jpg")
        else:
            abort(404)


class ResizeImageView(ProcessImageMixin, MethodView):
    def get(self, filename, resize="thumb"):
        app.logger.info(resize)

        if resize in image_size_map:
            _size = image_size_map[resize]
        else:
            return abort(401)

        if app.storage.is_exist(filename):
            content = app.storage.read(filename)
            return self.resize(content=content, size=_size)
        else:
            return abort(404)


# class GrayImageView(ProcessImageMixin, MethodView):
#     def get(self, filename):
#         if app.storage.is_exist(filename):
#             content = app.storage.read(filename)
#             return self.to_gray(content=content)
#         else:
#             return abort(404)


# class AsciiArtImageView(ProcessImageMixin, MethodView):
#     def get(self, filename):
#         if app.storage.is_exist(filename):
#             content = app.storage.read(filename)
#             return render_template("images/aimg.html", aimg=self.to_asciiart(content))
#         else:
#             return abort(404)

images.add_url_rule(
    "/<filename>",
    view_func=OriginImageView.as_view("image-origin"),
)

images.add_url_rule(
    "/<filename>-<resize>",
    view_func=ResizeImageView.as_view("image-processor"),
)
# images.add_url_rule(
#     "/<filename>/resize/<int:size>",
#     view_func=ResizeImageView.as_view("image-processor"),
# )

# images.add_url_rule(
#     "/<filename>/l/", view_func=GrayImageView.as_view("image-gray")
# )

# images.add_url_rule(
#     "/<filename>/ascii/", view_func=AsciiArtImageView.as_view("image-ascii")
# )
