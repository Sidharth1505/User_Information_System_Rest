
from db import db 
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError
from models import AuthModel
from schemas import PlainAuthSchema,PlainUserSchema
from flask_jwt_extended import (create_access_token,get_jwt,jwt_required,
set_access_cookies,
unset_jwt_cookies,get_csrf_token,
verify_jwt_in_request)
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST
from flask import jsonify

blp = Blueprint("Authentication","authentication",description="Operations on authentication")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(PlainAuthSchema)
    @blp.response(200,PlainAuthSchema)
    def post(self,register_data):
        if AuthModel.query.filter(AuthModel.username == register_data["username"]).first():
            abort(409,message="A user with that name already exists")
        new_user = AuthModel(
                username = register_data["username"],
                password = pbkdf2_sha256.hash(register_data["password"])
            )
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            print("error thrown is {}".format(e))
        return {"message":"User created Successfully"},201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainAuthSchema)
    def post(self,login_data):
        user = AuthModel.query.filter(AuthModel.username == login_data["username"]).first()
        if user and pbkdf2_sha256.verify(login_data["password"],user.password):
            access_token = create_access_token(identity=user.id)
            resp = jsonify({"Login":True, "csrf-cookie":get_csrf_token(access_token)})
            set_access_cookies(resp,access_token)
            
            return resp,200
        
        abort(401,message="Invalid Credentials, please check and try again")


@blp.route("/logout")
class UserLogout(MethodView):
    # @jwt_required(locations=['cookies'])
    
    def post(self):
        # jti = get_jwt()["jti"]
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        # BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200