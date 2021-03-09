from flask import flash
from wtforms import validators, Form, StringField, RadioField, SelectField
import json

from . import MODULE_CONFIG

with open("./src/MyFlaskModules/api/resources/colourIdLookup.json") as f:
    colourIdLookupJSON = json.load(f)

class Form_SubmitPixel(Form):
    fsp_auth_token = StringField(validators = [
        validators.InputRequired(message = "Please enter a token, obtained in the Discord"),
        validators.Length(message = "Token has length {}".format(MODULE_CONFIG["tokenLength"]), min = MODULE_CONFIG["tokenLength"], max = MODULE_CONFIG["tokenLength"]),
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
    fsp_colourId = SelectField(validators = [
        validators.InputRequired(message = "Please select a colour"),
        validators.AnyOf([str(key) for key in colourIdLookupJSON.keys()], message = "Invalid colourId")],
        choices = [(str(key), str(key)) for key in colourIdLookupJSON.keys()]
    )

