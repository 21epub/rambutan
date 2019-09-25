# from flask import Flask
# from flask import Response
# from werkzeug.routing import BaseConverter


# app = Flask(__name__)
# app.config.from_pyfile('../config/default.py')


# class RegexConverter(BaseConverter):
#     def __init__(self, url_map, *items):
#         super(RegexConverter, self).__init__(url_map)
#         self.regex = items[0]

# app.url_map.converters['regex'] = RegexConverter

# import images


# def get_content_type(filename):
#     content_type = 'image/jpeg'
#     if filename.endswith('png'):
#         content_type = 'image/png'
#     return content_type


# @app.route('/img/<int:size>/<image_name>', methods=['GET'])
# def handel_img(size, image_name):
#     filename = 'img/{0}'.format(image_name)
#     app.logger.info("size %d, imagename %s" % (size, filename))
#     content = images.resize(filename, size)
#     content_type = get_content_type(filename)
#     return Response(content, content_type=content_type)


# @app.route('/images/<int:size>/<image_name>', methods=['GET'])
# def handel_images(size, image_name):
#     # string = "%d %s" % (size, image_name)
#     filename = 'images/{0}'.format(image_name)
#     app.logger.info("size %d, imagename %s" % (size, filename))
#     content = images.resize(filename, size)
#     content_type = get_content_type(filename)
#     return Response(content, content_type=content_type)


# @app.route('/avatar/<int:size>/<avatar_name>', methods=['GET'])
# def handle_avatar(size, avatar_name):
#     filename = 'avatar/{0}'.format(avatar_name)
#     # app.logger.info("avatar %s" % filename)
#     content_type = get_content_type(filename)

#     content = images.resize(filename, size)
#     return Response(content, content_type=content_type)


# @app.route('/avatar/<int:size>/large/<avatar_name>', methods=['GET'])
# def handle_old_avatar(size, avatar_name):
#     filename = 'avatar/large/{0}'.format(avatar_name)
#     app.logger.info("avatar %s" % filename)
#     content = images.resize(filename, size)
#     return Response(content, content_type='image/jpeg')


# # TODO: get origin image
# @app.route('/img/<image_name>', methods=['GET'])
# def origin_img(image_name):
#     path = image_name.split('_')
#     app.logger.info(path)
#     if len(path) > 1:
#         filename = path[0]
#         size = path[1].split('x')
#         app.logger.info("%s %s" % (filename, size[0]))

#         filename = 'img/{0}'.format(filename)
#         content = images.resize(filename, int(size[0]))
#         return Response(content, content_type='image/jpeg')
#     filename = 'img/{0}'.format(image_name)
#     content = images.origin(filename)
#     return Response(content, content_type='image/jpeg')

# @app.route('/images/<image_name>', methods=['GET'])
# def origin_image(image_name):
#     path = image_name.split('_')
#     app.logger.info(path)
#     if len(path) > 1:
#         filename = path[0]
#         size = path[1].split('x')
#         app.logger.info("%s %s" % (filename, size[0]))

#         filename = 'images/{0}'.format(filename)
#         content = images.resize(filename, int(size[0]))
#         return Response(content, content_type='image/jpeg')
#     filename = 'images/{0}'.format(image_name)
#     content = images.origin(filename)
#     return Response(content, content_type='image/jpeg')


# @app.route('/avatar/<string:size>/<avatar_name>', methods=['GET'])
# @app.route('/avatar/<avatar_name>', methods=['GET'])
# def origin_avatar(avatar_name, size=None):
#     if size:
#         filename = 'avatar/{0}/{1}'.format(size, avatar_name)
#     else:
#         filename = 'avatar/{0}'.format(avatar_name)
#     app.logger.info(filename)
#     content = images.origin(filename)
#     return Response(content, content_type='image/jpeg')

# if __name__ == '__main__':
#     # app.debug = False
#     app.run(host="0.0.0.0")

# __author__ = 'xiejiaxin'


from flask import Flask
from flask_bootstrap import Bootstrap

from instance.config import app_config

from flask_storage.local_storage import FileStorage


def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")

    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # set storage
    app.storage = FileStorage(app)
    Bootstrap(app)

    from apps.views.images import images as images_url

    app.register_blueprint(images_url)

    return app


__version__ = "2.0.0"
