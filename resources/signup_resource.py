from flask import request
from flask_restful import Resource

from models.user import User
from schemas.user import UserSchema


class SignupResource(Resource):
    def get(self):
        schema = UserSchema(many=True)
        users = User.objects
        return schema.dump(users)

    def post(self):
        user_schema = UserSchema()
        user = user_schema.load(request.json)
        user.save()
        return user_schema.dump(user)
