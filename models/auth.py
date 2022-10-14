from db import db

class AuthModel(db.Model):
    __tablename__ ="authtable"

    id = db.Column(db.Integer,primary_key = True,nullable=False)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)