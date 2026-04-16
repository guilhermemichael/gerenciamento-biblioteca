import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///{path}".format(path=os.path.join(basedir, "mission_control.db")),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }
    SWAGGER = {
        "title": "SGAL API",
        "uiversion": 3,
    }

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
