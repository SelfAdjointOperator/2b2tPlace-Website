from flask import Blueprint, render_template, url_for, request, abort
from time import time
import random
import json

from . import MODULE_CONFIG
from .models import db, Pixel, PixelHistory, User, ActiveToken

bp = Blueprint("api",
    __name__,
    static_folder = "static",
    template_folder = "templates",
    url_prefix = "/api"
)

@bp.route("/")
def index():
    return render_template("api/index.html")

@bp.route("/token.json")
def api_token():
    # TODO decorator for routes that require authKey
    authKey = request.headers.get("authKey")
    if authKey != MODULE_CONFIG["secretKey_API"]:
        return abort(401)
    discordUUID = request.headers.get("discordUUID")
    discordTag = request.headers.get("discordTag")
    if (discordUUID is None) or (discordTag is None) or (not isinstance(discordUUID, str)) or (not isinstance(discordTag, str)):
        return abort(400)
    if not (user_byUUID := User.query.filter_by(discordUUID = discordUUID).first()):
        user_byUUID = User(discordUUID = discordUUID, discordTag = discordTag)
        db.session.add(user_byUUID)
        db.session.commit()
    elif user_byUUID.discordTag != discordTag:
        user_byUUID.discordTag = discordTag
        db.session.commit()
    timestamp = int(time())
    if (user_token := user_byUUID.activeToken):
        return json.dumps({"token": user_token.tokenValue})
    elif ((user_lastSubmitTime := user_byUUID.lastSubmitTime) is None) or ((timestamp - int(user_lastSubmitTime)) >= MODULE_CONFIG["timeBetweenSubmissions"]):
        newTokenValue = ("%0{}x".format(MODULE_CONFIG["tokenLength"]) % random.randrange(16 ** MODULE_CONFIG["tokenLength"])).upper()
        user_byUUID.activeToken = ActiveToken(tokenValue = newTokenValue)
        db.session.commit()
        return json.dumps({"token": newTokenValue})
    else:
        return json.dumps({"nextTimeAllowed": str(MODULE_CONFIG["timeBetweenSubmissions"] + int(user_lastSubmitTime))})

# TODO more routes for json files for main js app to load
