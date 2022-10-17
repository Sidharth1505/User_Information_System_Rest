import imp
from db import db

class UserRoleMapModel(db.Model):
    __tablename__ = "userrolemap"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))
    role = db.relationship("RoleModel")
    user = db.relationship("UserModel")