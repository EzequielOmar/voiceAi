from flask import Blueprint

views_blueprint = Blueprint("views", __name__)

from . import home