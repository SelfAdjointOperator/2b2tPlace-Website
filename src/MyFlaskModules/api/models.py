import json
import os
from flask_sqlalchemy import SQLAlchemy

from . import MODULE_CONFIG

db = SQLAlchemy()

class Pixel(db.Model):
    __tablename__   = "PIXEL"
    id              = db.Column(db.Integer, primary_key = True)
    x               = db.Column(db.Integer, nullable = False)
    y               = db.Column(db.Integer, nullable = False)
    colourId        = db.Column(db.Integer, nullable = False, default = 0) # use Colour Enum / constants
    pixelActivityTotal = db.Column(db.Integer, nullable = False, default = 0)

    pixelHistoryEntries = db.relationship("PixelHistory", back_populates = "pixel", uselist = True)

class PixelHistory(db.Model):
    __tablename__ = "PIXELHISTORY"
    id            = db.Column(db.Integer, primary_key = True)
    pixelId       = db.Column(db.Integer, db.ForeignKey("PIXEL.id"), nullable = False)
    userId        = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable = True)
    oldColourId   = db.Column(db.Integer, nullable = False)
    colourId      = db.Column(db.Integer, nullable = False) # use Colour Enum
    timestamp     = db.Column(db.Integer, nullable = False)
    pixelActivityNumber = db.Column(db.Integer, nullable = False)
    userActivityNumber = db.Column(db.Integer, nullable = True)

    pixel         = db.relationship("Pixel", back_populates = "pixelHistoryEntries")
    user          = db.relationship("User", back_populates = "pixelHistoryEntries")

class User(db.Model):
    __tablename__  = "USER"
    id             = db.Column(db.Integer, primary_key = True)
    discordUUID    = db.Column(db.Unicode(512), nullable = True)
    discordTag     = db.Column(db.Unicode(512), nullable = True)
    lastSubmitTime = db.Column(db.Integer, nullable = True)
    userActivityTotal = db.Column(db.Integer, nullable = False, default = 0)

    pixelHistoryEntries = db.relationship("PixelHistory", back_populates = "user", uselist = True)
    activeToken = db.relationship("ActiveToken", back_populates = "user", uselist = False)

class ActiveToken(db.Model):
    __tablename__ = "ACTIVETOKEN"
    id            = db.Column(db.Integer, primary_key = True)
    userId        = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable = False)
    tokenValue    = db.Column(db.String(MODULE_CONFIG["tokenLength"]), nullable = False)

    user          = db.relationship("User", back_populates = "activeToken", uselist = False)

def initialiseDatabaseIfNecessary():
    # creates blank pixels: will probably be replaced with terrain generator
    if not (pixelPing := Pixel.query.first()):
        db.session.bulk_save_objects([Pixel(x = x, y = y) for x in range(128) for y in range(128)])
        db.session.commit()

def initialiseFromMapJSON(mapJSONFilename):
    """For initialising our database with an image"""
    if (pixelPing := Pixel.query.first()):
        return
    mapJSONFilename = os.path.normpath(mapJSONFilename)
    with open(mapJSONFilename) as f:
        loadedJSON = json.load(f)
    db.session.bulk_save_objects([Pixel(x = pixel["x"], y = pixel["y"], colourId = pixel["colourId"]) for pixel in loadedJSON])
    db.session.commit()
