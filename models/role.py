from db import db
from models.user_role_map import UserRoleMapModel

class RoleModel(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(15), nullable=False)
    user = db.relationship("UserModel", back_populates="role")