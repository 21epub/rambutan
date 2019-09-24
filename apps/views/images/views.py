import requests
from flask import Flask, current_app, Response
from flask.views import MethodView

from . import images
from .handles.jpg_handle import ImageProcessor

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


class ProcessorImageView(MethodView):

    def resize(self, content, size):
        _size = get_thumbnail_size()
        if size >= _size:
            _size = size
        processor = ImageProcessor(fd=content)
        img = processor.resize((_size, _size))
        content, mime_type = ImageProcessor.output(
            img, format=processor.get_format(), quality=get_quality_size()
        )
        return Response(content, content_type=mime_type)

    def get(self, filename, size=0):
        res = requests.get("https://img.chainnews.com/upload/cover/{}".format(filename))
        return self.resize(content=res.content, size=size)


images.add_url_rule(
    "/<filename>/resize",
    view_func=ProcessorImageView.as_view("image-processor-thumbnail"),
)
images.add_url_rule(
    "/<filename>/resize/<int:size>",
    view_func=ProcessorImageView.as_view("image-processor"),
)
