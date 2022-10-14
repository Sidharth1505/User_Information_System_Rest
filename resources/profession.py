from email import message
from pydoc import describe
from db import db
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from models import ProfessionModel, profession
from schemas import ProfessionSchema

blp = Blueprint("Profession", __name__,description="Operation on Profession Table")

@blp.route("/profession")
class ProfessionList(MethodView):

    @blp.response(200,ProfessionSchema(many=True))
    def get(self):
        return ProfessionModel.query.all()

    @blp.arguments(ProfessionSchema)
    @blp.response(200, ProfessionSchema)
    def post(self, profession_data):
        if ProfessionModel.query.filter(ProfessionModel.profession_name == profession_data["profession_name"]).first():
            abort(409, message="Profession Already exists")
        new_profession = ProfessionModel(profession_name = profession_data["profession_name"])
        try:
            db.session.add(new_profession)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Error while Creating the Profession and the error is {}".format(e))
        return new_profession,200

@blp.route("/profession/<int:profession_id>")
class Professsion(MethodView):


    @blp.response(200, ProfessionSchema)
    def get(self,profession_id):
        profession = ProfessionModel.query.get_or_404(profession_id)
        return profession

    @blp.arguments(ProfessionSchema)
    @blp.response(200, ProfessionSchema)
    def put(self,profession_data,profession_id):
        profession = ProfessionModel.query.get_or_404(profession_id)
        if profession:
            profession.profession_name = profession_data["profession_name"]
        else:
            profession = ProfessionModel(id=profession_id,**profession_data)
        
        db.session.add(profession)
        db.session.commit()
        return profession

    def delete(self,profession_id):
        profession = ProfessionModel.query.get_or_404(profession_id)
        db.session.delete(profession)
        db.session.commit()

        return {"message":"Deletion Successful"},200



