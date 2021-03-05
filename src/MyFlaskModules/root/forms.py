from flask import flash
from wtforms import validators, Form, StringField, RadioField, SelectField

from . import MODULE_CONFIG

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
    # TODO field for colour


# TODO move this to API \/

# def handle_Form_SubmitPixel(form):
#     if not form.validate():
#         for field in form.errors:
#             for error in form.errors[field]:
#                 flash("Error: {}".format(error), "error")
#         return False

#     form_tokenValue = (form.fsp_auth_token.data).upper()

#     if (db_token := ActiveToken.query.filter_by(tokenValue = form_tokenValue).first()) is None:
#         flash("Error: Token not recognised")
#         return False

#     form_x = int(form.fsp_coordinate_x.data)
#     form_y = int(form.fsp_coordinate_y.data)
#     form_anonymise = form.fsp_anonymise.data
#     form_colourId = int(0) # TODO implement colourId #int(form.fsp_colourID.data)
#     timestamp = int(time())

#     db_token_user = db_token.user
#     db_pixel = Pixel.query.filter_by(x = form_x, y = form_y).first()
#     if form_anonymise == "public":
#         pixelHistory_new_userId = db_token_user.id
#     else:
#         pixelHistory_new_userId = None
#     pixelHistory_new = PixelHistory(pixelId = db_pixel.id,
#         userId = pixelHistory_new_userId,
#         colourId = form_colourId,
#         timestamp = timestamp
#     )
#     db_token_user.lastSubmitTime = timestamp
#     db_pixel.colourId = form_colourId
#     db_pixel.activityCount = Pixel.activityCount + 1
#     db.session.add(pixelHistory_new)
#     db.session.delete(db_token)
#     db.session.commit()
#     flash("Pixel updated!", "info")
#     return True
