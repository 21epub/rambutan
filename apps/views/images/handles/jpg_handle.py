from io import BytesIO

from PIL import Image

image_format = {
    "RGB": "JPEG",
    "L": "JPEG",
    "RGBA": "PNG"
}

mime_type = {
    "jpeg": "image/jpeg",
    "png": "image/png",
}


# def _get_image_format(img) -> str:
#     return image_format.get(img.mode)


def _get_mime_type(format) -> str:
    return mime_type.get(format.lower())


class ImageProcessor(object):

    def __init__(self, fd, **kwargs):
        self.im = Image.open(BytesIO(fd), mode="r")

    def get_format(self):
        return self.im.format

    def resize(self, size=tuple()) -> Image.Image:
        # w, h = size
        # if w / h > self.im.width / self.im.height:
        #     _width = round(h * self.im.width / self.im.height)
        #     _height = h
        # else:
        #     _width = w
        #     _height = round(w * self.im.height / self.im.width)
        # _width = int(_width)
        # _height = int(_height)
        # return self.im.resize((_width, _height), Image.ANTIALIAS)
        self.im.thumbnail(size)
        return self.im

    @classmethod
    def output(cls, im, format="JPEG", quality=85) -> bytes:
        if not isinstance(im, Image.Image):
            raise
        fd = BytesIO()
        _format = format
        im.save(fd, format=_format, quality=quality)
        # im.save(fd, format=_format)
        content = fd.getvalue()
        fd.close()
        return content, _get_mime_type(_format)
