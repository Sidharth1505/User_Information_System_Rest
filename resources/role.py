from email import message
import imp
from db import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.role import RoleModel
from schemas import RoleSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Roles", __name__, description="Operation on Roles")

@blp.route("/role")
class RoleList(MethodView):

    @blp.response(200, RoleSchema(many=True))
    def get(self):
        return RoleModel.query.all()
    
    @blp.arguments(RoleSchema)
    @blp.response(201,RoleSchema)
    def post(self, roles):
        if RoleModel.query.filter(RoleModel.role_name==roles["role_name"]).first():
            abort(409, message="Role already exists")
        role = RoleModel(role_name=roles["role_name"])
        try:
            db.session.add(role)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message="Error while Creating a new Role and the error {}".format(e))
        return role,201

@blp.route("/role/<int:role_id>")
class Role(MethodView):

    @blp.response(200, RoleSchema)
    def get(self,role_id):
        return RoleModel.query.get_or_404(role_id)
    
    @blp.arguments(RoleSchema)
    @blp.response(200,RoleSchema)
    def put(self,role_update,role_id):
        role = RoleModel.query.get_or_404(role_id)
        if role:
            role.role_name = role_update["role_name"]
        else:
            role = RoleModel(id=role_id,**role_update)
        db.session.add(role)
        db.session.commit()
        return role,200

    def delete(self,role_id):
        role = RoleModel.query.get_or_404(role_id)

        db.session.delete(role)
        db.session.commit()

        return {"message":"Deletion Successfull"},200


