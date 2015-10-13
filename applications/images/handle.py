import requests
from cStringIO import StringIO
from .handleImage import HandleImage
from flask import abort

# intranet_image_server = "http://image.guoku.com/"
intranet_image_server = "http://10.0.2.50/"


def origin(image_name, **kwargs):
    url = intranet_image_server + image_name
    r = requests.get(url)
    if r.status_code == 404:
        return abort(404)
    f = StringIO(r.content)
    return f.read()


def resize(image_name, size, **kwargs):
    url = intranet_image_server + image_name
    r = requests.get(url)
    if r.status_code == 404:
        return abort(404)
    f = StringIO(r.content)

    image = HandleImage(f)
    image.resize(size, size)

    return image.getImageString()

__author__ = 'xiejiaxin'

