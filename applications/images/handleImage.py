from PIL import Image
from cStringIO import StringIO


class HandleImage():

    def __init__(self, data, image_format='JPEG'):
        # self.data = data
        self.im = Image.open(data, mode='r')
        # print self.im.format
        # self.format = image_format
        self.format = self.im.format

    def resize(self, w, h):
        #  quick fix 0 divide error in django.log
        if w == 0 or h == 0 :
            w = h = 100

        if (w / h > self.im.width / self.im.height):
            _width = round(h * self.im.width / self.im.height)
            _height = h
        else:
            _width = w
            _height = round(w * self.im.height / self.im.width)

        _width = int(_width)
        _height = int(_height)
        self.im = self.im.resize((_width, _height), Image.ANTIALIAS)

    def getImageString(self):
        output = StringIO()
        self.im.save(output, self.format, quality = 100)
        content = output.getvalue()
        output.close()
        return content

__author__ = 'xiejiaxin'
