from marshmallow.schema import Schema, fields

from api.specs import spec
from api.helpers.specs import definition


@definition(spec)
class LoginSchema(Schema):
    login = fields.Email(required=True)
    password = fields.String(required=True)
