from flask import request
from flask_restful import Resource

from core.extensions import db
from models.user import User
from schemas.user import UserSchema


class SignupResource(Resource):
    @classmethod
    def get(cls):
        schema = UserSchema(many=True)
        users = User.query.all()
        return schema.dump(users)

    @classmethod
    def post(cls):
        user_schema = UserSchema()
        user = user_schema.load(request.json)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
