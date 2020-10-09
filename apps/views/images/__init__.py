from flask import Blueprint

images = Blueprint("images", __name__, url_prefix="/epub360-media")  # noqa

from . import views
