from marshmallow import Schema, fields

from schemas.user import UserSchema


class TokenRefreshDumpSchema(Schema):
    access_token = fields.Str()


class LoginDumpSchema(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()
    user = fields.Nested(UserSchema())


class LogoutDumpSchema(Schema):
    success = fields.Boolean()


class LogoutLoadSchema(Schema):
    refresh_token = fields.Str(required=True)


class EmailConfirmationLoadSchema(Schema):
    token = fields.Str(required=True)
