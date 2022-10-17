from db import db

class RoleModel(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(15), nullable=False)
    user = db.relationship("UserModel", back_populates="role")