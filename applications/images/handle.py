from cStringIO import StringIO

import requests
from flask import abort

from .pnglib import tiny
from .handleImage import HandleImage

# intranet_image_server = "http://image.guoku.com/"
intranet_image_server = "http://10.0.2.50/"

PNG = 'png'

def compress(f):
    rv = tiny(f, len(f))
    return rv

def origin(image_name, **kwargs):
    url = intranet_image_server + image_name
    r = requests.get(url)
    if r.status_code == 404:
        return abort(404)
    if url.endswith(PNG):
        rv = compress(r.content)
        return rv
    f = StringIO(r.content)
    return f.read()


def resize(image_name, size, **kwargs):
    # url = intranet_image_server + image_name
    # r = requests.get(url)
    # if r.status_code == 404:
    #     return abort(404)

    f = origin(image_name)

    f = StringIO(f)

    image = HandleImage(f)
    image.resize(size, size)

    return image.getImageString()







__author__ = 'xiejiaxin'

