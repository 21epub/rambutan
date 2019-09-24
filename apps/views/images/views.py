import requests
from flask import Flask, current_app, Response, request
from flask.views import MethodView

from . import images
from .handles.jpg_handle import ImageProcessor

app = Flask(__name__)
with app.app_context():
    app = current_app


class ProcessorImageView(MethodView):
    def resize(self, content, size):
        processor = ImageProcessor(fd=content)
        img = processor.resize((size, size))
        content, mime_type = ImageProcessor.output(
            img, format=processor.get_format(), quality=85
        )
        return Response(content, content_type=mime_type)

    def get(self, filename, size=128):
        # f9af0489-8eb8-50ab-837b-c92bb27e4a65_qcBMpRS.jpg
        # app.logger.info(filename)
        res = requests.get("https://img.chainnews.com/upload/cover/{}".format(filename))
        return self.resize(content=res.content, size=size)


images.add_url_rule(
    "/<filename>/resize/<int:size>",
    view_func=ProcessorImageView.as_view("image-processor"),
)
