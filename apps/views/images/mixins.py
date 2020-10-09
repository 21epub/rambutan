import re

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
    img_pattern = re.compile(r".*-(thumb|large|hd)$", re.IGNORECASE)

    def process_filename(self, filename: str) -> tuple:
        m = self.img_pattern.match(filename)
        _size = "origin"
        if m:
            _size = m.group(1)
            _filename = filename.replace(f"-{_size}", "")
        else:
            _filename = filename
        return _filename, _size

    def resize(self, content, size, quality=95):
        if size == 0:
            return Response(content, content_type="image/jpg")

        _size = get_thumbnail_size()
        if size >= _size:
            _size = size
        processor = ImageProcessor(fd=content)
        img = processor.resize((_size, _size))
        content, mime_type = ImageProcessor.output(
            img, format=processor.get_format(), quality=quality
        )
        return Response(content, content_type=mime_type)
