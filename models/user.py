from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80),unique=True,nullable = False)
    address = db.Column(db.String(100),nullable = False)
    contact = db.Column(db.Integer,nullable = False)
    dob = db.Column(db.Date,nullable=False)
    gender = db.Column(db.String(15),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("RoleModel", back_populates="user")