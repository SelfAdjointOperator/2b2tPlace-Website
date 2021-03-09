from flask import Blueprint, render_template, url_for, request, abort, flash
from sqlalchemy import and_
from time import time
import random
import json

from . import MODULE_CONFIG
from .models import db, Pixel, PixelHistory, User, ActiveToken
from .forms import Form_SubmitPixel

bp = Blueprint("api",
    __name__,
    static_folder = "static",
    template_folder = "templates",
    url_prefix = "/api"
)

def requiresAuthKey(function):
    """Decorator for admin / Discord bot methods"""
    def decorated(*args, **kwargs):
        authKey = request.headers.get("authKey")
        if authKey != MODULE_CONFIG["secretKey_API"]:
            return abort(401)
        return function(*args, **kwargs)
    decorated.__name__ = function.__name__
    return decorated

@bp.route("/")
def index():
    return render_template("api/index.html")

@bp.route("/admin/token.json")
@requiresAuthKey
def admin_token():
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

@bp.route("/pixels.json")
def pixels():
    """Fetch current state of all pixels"""
    pixels_JSON = [{
        "x": pixel.x,
        "y": pixel.y,
        "colourId": pixel.colourId,
        "pixelActivityTotal": pixel.pixelActivityTotal
    } for pixel in Pixel.query.all()]
    return json.dumps(pixels_JSON)

@bp.route("/history.json")
def history():
    """Fetch history about a range of space or time, or history from a user
    URL query parameter groups: (userId), (timeFrom), (timeTo), (xFrom, xTo, yFrom, yTo)"""

    q = PixelHistory.query

    try:
        userId = int(request.args.get("userId"))
        q = q.join(User).filter(User.id == userId)
    except:
        pass

    try:
        timeFrom = int(request.args.get("timeFrom"))
        q = q.filter(PixelHistory.timestamp >= timeFrom)
    except:
        pass

    try:
        timeTo = int(request.args.get("timeTo"))
        q = q.filter(PixelHistory.timestamp <= timeTo)
    except:
        pass

    try:
        xFrom = int(request.args.get("xFrom"))
        xTo   = int(request.args.get("xTo"))
        yFrom = int(request.args.get("yFrom"))
        yTo   = int(request.args.get("yTo"))
        q = q.join(Pixel).filter(
            and_(
                Pixel.x >= xFrom,
                Pixel.x <= xTo,
                Pixel.y >= yFrom,
                Pixel.y <= yTo
            )
        )
    except:
        pass

    historyEntries = q.order_by(
        PixelHistory.id.desc()
    ).all()

    returnJSON = [{
        "historyId": historyEntry.id,
        "x": historyEntry.pixel.x,
        "y": historyEntry.pixel.y,
        "oldColourId": historyEntry.oldColourId,
        "colourId": historyEntry.colourId,
        "timestamp": historyEntry.timestamp,
        "userId": historyEntry.userId,
        "userDiscordTag": historyEntry.user.discordTag if historyEntry.user is not None else None
    } for historyEntry in historyEntries]
    return json.dumps(returnJSON)

@bp.route("/submit.json", methods = ["POST"])
def submit():
    form = Form_SubmitPixel(request.form)
    if form is None:
        flash("Error: No form detected in POST request", "error")
        return abort(400)
    if not form.validate():
        for field in form.errors:
            for error in form.errors[field]:
                print(error)
                flash("Error: {}".format(error), "error")
        return abort(400)

    form_auth_token_data = (form.fsp_auth_token.data).upper()

    if (db_token := ActiveToken.query.filter_by(tokenValue = form_auth_token_data).first()) is None:
        flash("Error: Token not recognised", "error")
        abort(401)

    form_coordinate_x = int(form.fsp_coordinate_x.data)
    form_coordinate_y = int(form.fsp_coordinate_y.data)
    form_anonymise = form.fsp_anonymise.data
    form_colourId = int(form.fsp_colourId.data)
    timestamp = int(time())

    db_user = db_token.user
    db_pixel = Pixel.query.filter_by(x = form_coordinate_x, y = form_coordinate_y).first()

    newPixelHistory_pixelId = db_pixel.id
    newPixelHistory_oldColourId = db_pixel.colourId
    newPixelHistory_colourId = form_colourId
    newPixelHistory_timestamp = timestamp
    newPixelHistory_pixelActivityNumber = db_pixel.pixelActivityTotal + 1

    db_pixel.pixelActivityTotal = db_pixel.pixelActivityTotal + 1

    if form_anonymise == "public":
        newPixelHistory_userId = db_user.id
        newPixelHistory_userActivityNumber = db_user.userActivityTotal + 1
        db_user.userActivityTotal = db_user.userActivityTotal + 1
    else:
        newPixelHistory_userId = None
        newPixelHistory_userActivityNumber = None

    db_pixel.colourId = form_colourId
    db_user.lastSubmitTime = timestamp

    newPixelHistory = PixelHistory(
        pixelId = newPixelHistory_pixelId,
        userId = newPixelHistory_userId,
        oldColourId = newPixelHistory_oldColourId,
        colourId = newPixelHistory_colourId,
        timestamp = timestamp,
        pixelActivityNumber = newPixelHistory_pixelActivityNumber,
        userActivityNumber = newPixelHistory_userActivityNumber
    )

    db.session.add(newPixelHistory)
    db.session.delete(db_token)
    db.session.commit()
    flash("Pixel updated!", "info")

    return json.dumps({"success": "success"}), 200
