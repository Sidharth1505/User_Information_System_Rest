from db import db

class UserProfessionModel(db.Model):
    __tablename__ = "userprofessionmap"

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    profession_id = db.Column(db.Integer,db.ForeignKey("profession.id"))