# pylint: disable=maybe-no-member

from time import time
import json
import random
from flask import Flask, redirect, url_for, render_template, request, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from wtforms import validators, Form, StringField, RadioField, SelectField

try:
    with open("./config_private.json") as config_private_file:
        GLOBAL_CONFIG_PRIVATE = json.load(config_private_file)
except FileNotFoundError:
    print("Error: File './config_private.json' not found")
    raise SystemExit

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(GLOBAL_CONFIG_PRIVATE["databaseURI"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = GLOBAL_CONFIG_PRIVATE["secretKey_App"]

db = SQLAlchemy(app)

class Pixel(db.Model):
    __tablename__   = "PIXEL"
    id              = db.Column(db.Integer, primary_key = True)
    x               = db.Column(db.Integer, nullable = False)
    y               = db.Column(db.Integer, nullable = False)
    colourId        = db.Column(db.Integer, nullable = False, default = 0) # use Colour Enum / constants
    activityCount   = db.Column(db.Integer, nullable = False, default = 0)

    pixelHistoryEntries = db.relationship("PixelHistory", back_populates = "pixel", uselist = True)

class PixelHistory(db.Model):
    __tablename__ = "PIXELHISTORY"
    id            = db.Column(db.Integer, primary_key = True)
    pixelId       = db.Column(db.Integer, db.ForeignKey("PIXEL.id"), nullable = False)
    userId        = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable = True)
    colourId      = db.Column(db.Integer, nullable = False) # use Colour Enum
    timestamp     = db.Column(db.Integer, nullable = False)

    pixel         = db.relationship("Pixel", back_populates = "pixelHistoryEntries")
    user          = db.relationship("User", back_populates = "pixelHistoryEntries")

class User(db.Model):
    __tablename__  = "USER"
    id             = db.Column(db.Integer, primary_key = True)
    discordUUID    = db.Column(db.String(512), nullable = True)
    discordTag     = db.Column(db.String(512), nullable = True)
    lastSubmitTime = db.Column(db.Integer, nullable = True)

    pixelHistoryEntries = db.relationship("PixelHistory", back_populates = "user", uselist = True)
    activeToken = db.relationship("ActiveToken", back_populates = "user", uselist = False)

class ActiveToken(db.Model):
    __tablename__ = "ACTIVETOKEN"
    id            = db.Column(db.Integer, primary_key = True)
    userId        = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable = False)
    tokenValue    = db.Column(db.String(GLOBAL_CONFIG_PRIVATE["tokenLength"]), nullable = False)

    user          = db.relationship("User", back_populates = "activeToken", uselist = False)


class Form_SubmitPixel(Form):
    fsp_auth_token = StringField(validators = [
        validators.InputRequired(message = "Please enter a token, obtained in the Discord"),
        validators.Length(message = "Token has length {}".format(GLOBAL_CONFIG_PRIVATE["tokenLength"]), min = GLOBAL_CONFIG_PRIVATE["tokenLength"], max = GLOBAL_CONFIG_PRIVATE["tokenLength"]),
        validators.Regexp("^[0-9a-fA-F]+$", message = "Token is a hex string")],
        render_kw = {"placeholder": "Token"}
    )
    fsp_coordinate_x = SelectField(validators = [
        validators.InputRequired(message = "Please specify x coordinate"),
        validators.AnyOf([str(i) for i in range(128)], message = "x coordinate must be in the range 0 to 127")],
        choices = [(str(i), str(i)) for i in range(128)]
    )
    fsp_coordinate_y = SelectField(validators = [
        validators.InputRequired(message = "Please specify y coordinate"),
        validators.AnyOf([str(i) for i in range(128)], message = "y coordinate must be in the range 0 to 127")],
        choices = [(str(i), str(i)) for i in range(128)]
    )
    fsp_anonymise = RadioField(validators = [
        validators.InputRequired(message = "Please choose whether to anonymise your pixel choice"),
        validators.AnyOf(["public", "anonymous"], message = "Anonymity field must be 'public' or 'anonymous'")],
        choices = [("public", "Show my Discord tag publicly"), ("anonymous", "Keep me anonymous")],
        default = "anonymous"
    )
    # TODO field for colour

def handle_Form_SubmitPixel(form):
    if not form.validate():
        for field in form.errors:
            for error in form.errors[field]:
                flash("Error: {}".format(error), "error")
        return False

    form_tokenValue = (form.fsp_auth_token.data).upper()

    if (db_token := ActiveToken.query.filter_by(tokenValue = form_tokenValue).first()) is None:
        flash("Error: Token not recognised")
        return False

    form_x = int(form.fsp_coordinate_x.data)
    form_y = int(form.fsp_coordinate_y.data)
    form_anonymise = form.fsp_anonymise.data
    form_colourId = int(0) # TODO implement colourId #int(form.fsp_colourID.data)
    timestamp = int(time())

    db_token_user = db_token.user
    db_pixel = Pixel.query.filter_by(x = form_x, y = form_y).first()
    if form_anonymise == "public":
        pixelHistory_new_userId = db_token_user.id
    else:
        pixelHistory_new_userId = None
    pixelHistory_new = PixelHistory(pixelId = db_pixel.id,
        userId = pixelHistory_new_userId,
        colourId = form_colourId,
        timestamp = timestamp
    )
    db_token_user.lastSubmitTime = timestamp
    db_pixel.colourId = form_colourId
    db_pixel.activityCount = Pixel.activityCount + 1
    db.session.add(pixelHistory_new)
    db.session.delete(db_token)
    db.session.commit()
    flash("Pixel updated!", "info")
    return True

### Error handlers ###

@app.errorhandler(400)
def app_errorhandler_400(e):
    return '{"error": "Bad request, check headers"}', 400

@app.errorhandler(401)
def app_errorhandler_401(e):
    return '{"error": "Unauthorised"}', 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

### Main site ###

@app.route("/", methods = ["GET", "POST"])
def index():
    form = Form_SubmitPixel(request.form)
    if request.method == "POST":
        handle_Form_SubmitPixel(form)
        return redirect(url_for("index"))
    elif request.method == "GET":
        return render_template("index.html", form = form)

### API routes ###

# TODO decorator for routes that require authKey

# TODO more routes for json files for main js app to load

@app.route("/api/token.json")
def api_token():
    authKey = request.headers.get("authKey")
    if authKey != GLOBAL_CONFIG_PRIVATE["secretKey_API"]:
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
        return {"token": user_token.tokenValue}
    elif ((user_lastSubmitTime := user_byUUID.lastSubmitTime) is None) or ((timestamp - int(user_lastSubmitTime)) >= GLOBAL_CONFIG_PRIVATE["timeBetweenSubmissions"]):
        newTokenValue = ("%0{}x".format(GLOBAL_CONFIG_PRIVATE["tokenLength"]) % random.randrange(16 ** GLOBAL_CONFIG_PRIVATE["tokenLength"])).upper()
        user_byUUID.activeToken = ActiveToken(tokenValue = newTokenValue)
        db.session.commit()
        return {"token": newTokenValue}
    else:
        return {"nextTimeAllowed": str(GLOBAL_CONFIG_PRIVATE["timeBetweenSubmissions"] + int(user_lastSubmitTime))}

################################################################################

def initialiseDatabaseIfNecessary():
    if not (pixelPing := Pixel.query.first()):
        db.session.bulk_save_objects([Pixel(x = x, y = y) for x in range(128) for y in range(128)])
        db.session.commit()

db.create_all()
initialiseDatabaseIfNecessary()

if __name__ == "__main__":
    app.run(debug = True)
