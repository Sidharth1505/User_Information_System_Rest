from db import db

class ProfessionModel(db.Model):
    __tablename__ = "profession"

    id = db.Column(db.Integer, primary_key=True)
    profession_name = db.Column(db.String(25), nullable = False)
