from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from core.extensions import db
from errors import BaseError
from models import User
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


class LoginResource(Resource):
    @classmethod
    def post(cls):
        user_schema = UserSchema(only=('username', 'password'))
        user = user_schema.load(request.json)
        db_user = User.query.filter_by(username=user.username).one_or_none()
        if not db_user or not check_password_hash(db_user.password, request.json.get('password')):
            raise BaseError(key='INVALID_CREDENTIALS')
        if not db_user.active:
            raise BaseError(key='INACTIVE_USER')

        access_token = create_access_token(identity=db_user.username)
        refresh_token = create_refresh_token(identity=db_user.username)

        return {'access_token': access_token,
                'refresh_token': refresh_token,
                **UserSchema().dump(db_user)}


class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}
