from ast import dump
from marshmallow import Schema,fields
from pkg_resources import require

from models import profession

class PlainUserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    contact = fields.Str(required=True)
    dob = fields.Date(required=True)
    gender = fields.Str(required=True)

class PlainAuthSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required =True)

class UserUpdateSchema(Schema):
    name = fields.Str(required=True)
    address= fields.Str(required=True)
    contact = fields.Str(required=True)


class ProfessionSchema(Schema):
    id = fields.Int(dump_only = True)
    profession_name = fields.Str(required=True)

class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    role_name = fields.Str(required=True)


class UserSchema(PlainUserSchema):
    role_id = fields.Int(required=True,load_only=True)
    profession_id = fields.Int(required=True,load_only=True)
    profession = fields.Nested(ProfessionSchema(),dump_only=True)
    role = fields.Nested(RoleSchema(),dump_only=True)

class RoleUserScehma(RoleSchema):
    user = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

class Profession(Schema):
    user = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

class UserRoleMapSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    role_id = fields.Int(required=True)

class UserProfessionMapSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    profession_id = fields.Int(dump_only=True)