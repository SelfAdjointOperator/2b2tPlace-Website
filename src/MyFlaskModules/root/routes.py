from flask import Blueprint, render_template, url_for, request

from . import MODULE_CONFIG

bp = Blueprint("root",
    __name__,
    static_folder = "static",
    template_folder = "templates",
    url_prefix = "/",
    static_url_path = "root/static"
)

@bp.route("/")
def index():
    return render_template("root/index.html")
