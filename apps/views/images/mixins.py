from flask import Response, Flask, current_app

from apps.views.images.handles.jpg_handle import ImageProcessor

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


class ProcessImageMixin(object):

    def resize(self, content, size, quality=85):
        _size = get_thumbnail_size()
        app.logger.info(_size)
        if size >= _size:
            _size = size
        processor = ImageProcessor(fd=content)
        img = processor.resize((_size, _size))
        content, mime_type = ImageProcessor.output(
            img, format=processor.get_format(), quality=quality
        )
        return Response(content, content_type=mime_type)

    def to_asciiart(self, content):
        processor = ImageProcessor(fd=content)
        aimg = processor.to_ascii()
        return aimg
