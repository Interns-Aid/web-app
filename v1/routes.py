from datetime import datetime
from datetime import timezone

from flask import request, render_template
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    get_jti,
)
from flask_restful import Resource
from werkzeug.security import check_password_hash

from core.extensions import db, jwt
from errors import BaseError
from models import User
from models.blocked_token import BlockedToken
from schemas.internship import InternshipSchema
from schemas.user import UserSchema
from services.auth import register, verify_email


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token = db.session.query(BlockedToken.id).filter_by(jti=jti).scalar()
    return token is not None


@jwt.user_lookup_loader
def user_lookup(jwt_header, jwt_payload: dict):
    username = jwt_payload.get("sub")
    user = User.query.filter_by(username=username).first()
    return user


class SignupResource(Resource):
    @classmethod
    def post(cls):
        user_schema = UserSchema()
        user = user_schema.load(request.json)
        return user_schema.dump(register(user))


class LoginResource(Resource):
    @classmethod
    def post(cls):
        user_schema = UserSchema(only=("username", "password"))
        user = user_schema.load(request.json)
        db_user = User.query.filter_by(username=user.username).one_or_none()
        if not db_user or not check_password_hash(
            db_user.password, request.json.get("password")
        ):
            raise BaseError(key="INVALID_CREDENTIALS")
        if not db_user.active:
            raise BaseError(key="INACTIVE_USER")

        access_token = create_access_token(identity=db_user.username)
        refresh_token = create_refresh_token(identity=db_user.username)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            **UserSchema().dump(db_user),
        }


class TokenRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}


class LogoutResource(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        access_token = get_jwt()
        jti = access_token["jti"]
        token_type = access_token["type"]
        now = datetime.now(timezone.utc)
        db.session.add(BlockedToken(jti=jti, type=token_type, created_at=now))

        refresh_token = request.json.get("refresh_token")
        jti = get_jti(refresh_token)
        db.session.add(BlockedToken(jti=jti, type="refresh", created_at=now))

        db.session.commit()
        return {"success": True}


class EmailConfirmationResource(Resource):
    @classmethod
    def patch(cls):
        verify_email(request.json.get("token"))
        return render_template("email-confirmation.html")


class UserProfile(Resource):
    @jwt_required()
    def get(self):
        user = User.query.filter_by(username=get_jwt_identity()).first()
        user_schema = UserSchema()
        return user_schema.dump(user)

    @jwt_required()
    def put(self):
        user = User.query.get(request.json.get("id"))
        user_schema = UserSchema(only=("first_name", "last_name", "password", "email"))
        user_schema.load(request.json, instance=user, partial=True)
        db.session.commit()
        return user_schema.dump(user)


class InternshipResource(Resource):
    @jwt_required()
    def post(self):
        internship_schema = InternshipSchema()
        internship = internship_schema.load(request.json)
        db.session.add(internship)
        db.session.commit()
        return internship_schema.dump(internship)
