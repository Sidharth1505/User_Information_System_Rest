import imp
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import db
from models.user import UserModel
from schemas import UserUpdateSchema, PlainUserSchema
from sqlalchemy.exc import SQLAlchemyError

blp =  Blueprint("User",__name__, description="Operation on users")

@blp.route("/users")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200,PlainUserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
    @jwt_required()
    @blp.arguments(PlainUserSchema)
    @blp.response(200,PlainUserSchema)
    def post(self,user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Error occurred while creating the user")
        return user,201

@blp.route("/users/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, PlainUserSchema)
    def get(self,user_id):
        user =  UserModel.query.get_or_404(user_id)
        return user


    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(200,PlainUserSchema)
    def put(self,user_data,user_id):
        user = UserModel.query.get(user_id)
        if user:
            user.name = user_data["name"]
            user.address = user_data["address"]
            user.contact = user_data["contact"]
        else:
            user = UserModel(id=user_id,**user_data)

        db.session.add(user)
        db.session.commit()

        return user

    @jwt_required()
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message":"User deleted successfully"}