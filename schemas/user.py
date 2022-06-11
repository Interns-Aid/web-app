from marshmallow_mongoengine import ModelSchema

from models.user import User


class UserSchema(ModelSchema):
    class Meta:
        model = User
