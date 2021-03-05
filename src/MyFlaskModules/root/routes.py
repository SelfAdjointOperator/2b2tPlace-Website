from flask import Blueprint, render_template, url_for, request

from . import MODULE_CONFIG
from .forms import Form_SubmitPixel

bp = Blueprint("root",
    __name__,
    static_folder = "static",
    template_folder = "templates",
    url_prefix = "/",
    static_url_path = "root/static"
)

@bp.route("/") # methods = ["GET", "POST"]
def index():
    form = Form_SubmitPixel(request.form)
    # if request.method == "POST":
    #     handle_Form_SubmitPixel(form)
    #     return redirect(url_for(".index"))
    # elif request.method == "GET": # TODO remove all this and use JS to query API
    #, form = form
    return render_template("root/index.html")
