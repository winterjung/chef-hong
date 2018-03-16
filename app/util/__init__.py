from flask import Blueprint

util = Blueprint('util', __name__)

from app.util import views  # noqa
