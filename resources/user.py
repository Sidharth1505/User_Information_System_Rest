from email import message
import imp
from flask_jwt_extended import jwt_required,get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from models import profession, user_profession_map
from models.user import UserModel
from models.user_role_map import UserRoleMapModel
from models.user_profession_map import UserProfessionModel
from schemas import UserUpdateSchema, PlainUserSchema, UserSchema
from sqlalchemy.exc import SQLAlchemyError

blp =  Blueprint("User",__name__, description="Operation on users")

@blp.route("/users")
class UserList(MethodView):
    # @jwt_required()
    @blp.response(200,UserSchema(many=True))
    def get(self):
        try:
            return UserModel.query.all()
        except SQLAlchemyError:
            abort(501, message="Error in connecting the database")
    
    # @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200,PlainUserSchema)
    def post(self,user_data):
        _user_id,user,role_id,_profession_id = user_data["id"],user_data, user_data["role_id"],user_data["profession_id"]
        del user["profession_id"]
        user_role_map = {"user_id":_user_id,"role_id":role_id}
        user_profession_map = []
        user = UserModel(**user)
        for id in _profession_id:
            user_profession_map.append(UserProfessionModel(profession_id=id))
        user.profession = user_profession_map
        rolemap = UserRoleMapModel(**user_role_map)
        try:
            db.session.add(user)
            db.session.add(rolemap)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message="Error occurred while creating the user {}".format(e))
        return user,201

@blp.route("/users/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, PlainUserSchema)
    def get(self,user_id):
        try:
            user =  UserModel.query.get_or_404(user_id)
        except SQLAlchemyError as e:
            abort(500, message="Error occured while accessing the database {}".format(e))
        return user


    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(200,PlainUserSchema)
    def put(self,user_data,user_id):
        try:
            user = UserModel.query.get(user_id)
            if user:
                user.name = user_data["name"]
                user.address = user_data["address"]
                user.contact = user_data["contact"]
            else:
                user = UserModel(id=user_id,**user_data)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Error occured {}".format(e))
        return user

    @jwt_required()
    def delete(self,user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        try:
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message="Error occurred {}".format(e))

        return {"message":"User deleted successfully"}