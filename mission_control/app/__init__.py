import flask as _flask
import flask.json as _flask_json
import json as _json
from flask import Flask
from flask_cors import CORS
from markupsafe import Markup

# Flasgger expects flask.Markup and flask.json.JSONEncoder on Flask 3.x.
_flask.Markup = Markup
_flask_json.JSONEncoder = _json.JSONEncoder

from flasgger import Swagger
from .database import db, migrate, ma
from .routes import api_v1
import config


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or config.DevelopmentConfig)

    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    Swagger(app)

    app.register_blueprint(api_v1, url_prefix="/api/v1")

    return app
