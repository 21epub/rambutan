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
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


class ImageProcessor(object):
    def __init__(self, fd, **kwargs):
        self.im = Image.open(BytesIO(fd), mode="r")

    def get_format(self):
        return self.im.format

    def resize(self, size=tuple()) -> Image.Image:
        self.im.thumbnail(size)
        return self.im

    def to_ascii(self, cols=80, scale=0.43, lv=False):
        im = self.im.convert("L")
        W, H = im.size
        w = W / cols
        h = w / scale
        rows = int(H / h)

        if cols > W or rows > H:
            raise
        aimg = list()
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)
            if j == rows - 1:
                y2 = H
            aimg.append("")
            for i in range(cols):
                x1 = int(i * w)
                x2 = int((i + 1) * w)
                if i == cols - 1:
                    x2 = W
                img = im.crop((x1, y1, x2, y2))
                avg = int(get_average_l(img))
                if lv:
                    gsval = gscale1[int((avg * 69) / 255)]
                else:
                    gsval = gscale2[int((avg * 9) / 255)]
                aimg[j] += gsval
        return aimg

    @classmethod
    def output(cls, im, format="JPEG", quality=85) -> bytes:
        if not isinstance(im, Image.Image):
            raise
        fd = BytesIO()
        _format = format
        im.save(fd, format=_format, quality=quality)
        content = fd.getvalue()
        fd.close()
        return content, _get_mime_type(_format)
