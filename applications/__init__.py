from flask import Flask
from flask import Response
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

import images


@app.route('/img/<int:size>/<image_name>', methods=['GET'])
def handel_img(size, image_name):
    # string = "%d %s" % (size, image_name)
    filename = 'img/{0}'.format(image_name)
    app.logger.info("size %d, imagename %s" % (size, filename))
    content = images.resize(filename, size)
    return Response(content, content_type='image/jpeg')


@app.route('/images/<int:size>/<image_name>', methods=['GET'])
def handel_images(size, image_name):
    # string = "%d %s" % (size, image_name)
    filename = 'images/{0}'.format(image_name)
    app.logger.info("size %d, imagename %s" % (size, filename))
    content = images.resize(filename, size)
    return Response(content, content_type='image/jpeg')


@app.route('/avatar/<int:size>/large/<avatar_name>', methods=['GET'])
@app.route('/avatar/<int:size>/<avatar_name>', methods=['GET'])
def handle_avatar(size, avatar_name):
    filename = 'avatar/' + avatar_name
    content = images.resize(filename, size)
    return Response(content, content_type='image/jpeg')


# def handle_avatar(size, avatar_name):
#     filename = 'avatar/' + avatar_name
#     content = images.resize(filename, size)
#     return Response(content, content_type='image/jpeg')


# TODO: get origin image
@app.route('/img/<image_name>', methods=['GET'])
def origin_img(image_name):
    path = image_name.split('_')
    app.logger.info(path)
    if len(path) > 1:
        filename = path[0]
        size = path[1].split('x')
        app.logger.info("%s %s" % (filename, size[0]))

        filename = 'img/{0}'.format(filename)
        content = images.resize(filename, int(size[0]))
        return Response(content, content_type='image/jpeg')
    filename = 'img/{0}'.format(image_name)
    content = images.origin(filename)
    return Response(content, content_type='image/jpeg')

@app.route('/images/<image_name>', methods=['GET'])
def origin_image(image_name):
    path = image_name.split('_')
    app.logger.info(path)
    if len(path) > 1:
        filename = path[0]
        size = path[1].split('x')
        app.logger.info("%s %s" % (filename, size[0]))

        filename = 'images/{0}'.format(filename)
        content = images.resize(filename, int(size[0]))
        return Response(content, content_type='image/jpeg')
    filename = 'images/{0}'.format(image_name)
    content = images.origin(filename)
    return Response(content, content_type='image/jpeg')


@app.route('/avatar/<string:size>/<avatar_name>', methods=['GET'])
@app.route('/avatar/<avatar_name>', methods=['GET'])
def origin_avatar(avatar_name, size=None):
    if size:
        filename = 'avatar/{0}/{1}'.format(size, avatar_name)
    else:
        filename = 'avatar/{0}'.format(avatar_name)
    app.logger.info(filename)
    content = images.origin(filename)
    return Response(content, content_type='image/jpeg')

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

__author__ = 'xiejiaxin'

