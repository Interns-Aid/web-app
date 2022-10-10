from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from core.extensions import db
from errors import BaseError
from schemas.user import UserSchema


class SignupResource(Resource):
    @classmethod
    def post(cls):
        user_schema = UserSchema()
        user = user_schema.load(request.json)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            raise BaseError(key='DUPLICATE_USER')
        return user_schema.dump(user)
