
from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from blocklist import BLOCKLIST

from db import db

from resources.user import blp as UserBluePrint
from resources.auth import blp as AuthBluePrint
from resources.profession import blp as ProfessionBluePrint
from resources.role import blp as RoleBluePrint

from models.user_role_map import UserRoleMapModel
from models.role import RoleModel

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

    app.config["JWT_SECRET_KEY"] = "228093562702811058850520514772539608930"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        role_id = UserRoleMapModel.query.filter(UserRoleMapModel.user_id==identity).first().role_id
        role = RoleModel.query.filter(RoleModel.id==role_id).first().role_name
        print(role)
        if role == "admin":
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

        
    with app.app_context():
        import models  # noqa: F401

        db.create_all()

    api.register_blueprint(UserBluePrint)
    api.register_blueprint(AuthBluePrint)
    api.register_blueprint(ProfessionBluePrint)
    api.register_blueprint(RoleBluePrint)

    return app