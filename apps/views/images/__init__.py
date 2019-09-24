from flask import Blueprint

images = Blueprint("images", __name__, url_prefix="/image")

from . import views
