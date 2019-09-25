import numpy as np
from io import BytesIO
from PIL import Image

mime_type = {"jpeg": "image/jpeg", "png": "image/png"}

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = "@%#*+=-:. "


def _get_mime_type(format) -> str:
    return mime_type.get(format.lower())


def get_average_l(image):
    if isinstance(image, Image.Image):
        im = np.array(image)
        w, h = im.shape
        return np.average(im.reshape(w * h))
    else:
        raise Exception("need a image object")


class ImageProcessor(object):
    def __init__(self, fd, **kwargs):
        self.im = Image.open(BytesIO(fd), mode="r")

    def get_format(self):
        return self.im.format

    def resize(self, size=tuple()) -> Image.Image:
        self.im.thumbnail(size)
        return self.im

    def to_ascii(self):

        return

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
