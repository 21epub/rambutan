from io import BytesIO

from PIL import Image

mime_type = {"jpeg": "image/jpeg", "png": "image/png"}


def _get_mime_type(format) -> str:
    return mime_type.get(format.lower())


class ImageProcessor(object):
    def __init__(self, fd, **kwargs):
        self.im = Image.open(BytesIO(fd), mode="r")

    def get_format(self):
        return self.im.format

    def resize(self, size=tuple()) -> Image.Image:
        self.im.thumbnail(size)
        return self.im

    @classmethod
    def output(cls, im, format="JPEG", quality=85) -> tuple:
        if not isinstance(im, Image.Image):
            raise
        fd = BytesIO()
        _format = format
        im.save(fd, format=_format, quality=quality)
        content = fd.getvalue()
        fd.close()
        return content, _get_mime_type(_format)
