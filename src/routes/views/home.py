from flask import render_template
from . import views_blueprint

@views_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")
