from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from .database import db, migrate, ma
from .routes import api_v1
import config

load_dotenv()


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
