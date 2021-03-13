from flask import Blueprint, render_template

from . import MODULE_CONFIG

bp = Blueprint("auxiliary",
    __name__,
    static_folder = "static",
    template_folder = "templates",
    url_prefix = "/auxiliary"
)

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
