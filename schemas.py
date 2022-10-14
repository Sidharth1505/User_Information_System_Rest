from marshmallow import Schema,fields
from pkg_resources import require

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    contact = fields.Str(required=True)
    dob = fields.Str(required=True)
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
