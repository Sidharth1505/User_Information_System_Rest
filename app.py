
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db

from resources.user import blp as UserBluePrint
from resources.auth import blp as AuthBluePrint
from resources.profession import blp as ProfessionBluePrint
from resources.role import blp as RoleBluePrint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "jose"
    jwt = JWTManager(app)

    with app.app_context():
        import models  # noqa: F401

        db.create_all()

    api.register_blueprint(UserBluePrint)
    api.register_blueprint(AuthBluePrint)
    api.register_blueprint(ProfessionBluePrint)
    api.register_blueprint(RoleBluePrint)

    return app