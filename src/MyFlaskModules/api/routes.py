from flask import Blueprint, render_template, url_for, request, abort
from sqlalchemy import and_
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
        "userDiscordTag": historyEntry.user.discordTag
    } for historyEntry in historyEntries]
    return json.dumps(returnJSON)
