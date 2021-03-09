from flask import Flask, render_template
import json

import MyFlaskModules
try:
    with open("./config.json") as config_file:
        GLOBAL_CONFIG = json.load(config_file)
        MyFlaskModules.GLOBAL_CONFIG = GLOBAL_CONFIG
except FileNotFoundError:
    print("Error: File './config.json' not found")
    raise SystemExit

app = Flask(__name__)

from MyFlaskModules.root.routes import bp as bp_root
app.register_blueprint(bp_root)

from MyFlaskModules.api.routes import bp as bp_api
app.register_blueprint(bp_api)
from MyFlaskModules.api.models import db, initialiseDatabaseIfNecessary, initialiseFromMapJSON

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(GLOBAL_CONFIG["databaseURI"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = GLOBAL_CONFIG["secretKey_App"]

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.context_processor
def inject_DiscordURL():
    return dict(discordInviteURL = GLOBAL_CONFIG["discordInviteURL"])

db.init_app(app)
with app.app_context():
    db.create_all()
    # initialiseDatabaseIfNecessary()
    initialiseFromMapJSON(GLOBAL_CONFIG["initialMapJSONFilepath"])

################################################################################

if __name__ == "__main__":
    app.run(debug = True)
