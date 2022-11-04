from datetime import datetime
from datetime import timezone

from flask import request, render_template
from flask_apispec import MethodResource, marshal_with, use_kwargs, doc
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

from core.decorators import doc_protected
from core.extensions import db, jwt
from errors import BaseError
from models import User
from models.blocked_token import BlockedToken
from schemas.auth import (
    TokenRefreshDumpSchema,
    LogoutDumpSchema,
    LogoutLoadSchema,
    LoginDumpSchema,
    EmailConfirmationLoadSchema,
)
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


@doc(description="Signup", tags=["Auth"])
class SignupResource(MethodResource):
    @marshal_with(UserSchema)
    @use_kwargs(UserSchema())
    def post(self, user):
        return register(user)


@doc(description="Login", tags=["Auth"])
class LoginResource(MethodResource):
    @marshal_with(LoginDumpSchema)
    @use_kwargs(UserSchema(only=("username", "password")))
    def post(self, user):
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
            "user": db_user,
        }


@doc_protected(description="Refresh Token", tags=["Auth"], refresh=True)
class TokenRefreshResource(MethodResource):
    @marshal_with(TokenRefreshDumpSchema)
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}


@doc_protected(description="Logout", tags=["Auth"])
class LogoutResource(MethodResource):
    @marshal_with(LogoutDumpSchema)
    @use_kwargs(LogoutLoadSchema)
    @jwt_required(verify_type=False)
    def post(self, **kwargs):
        access_token = get_jwt()
        jti = access_token["jti"]
        token_type = access_token["type"]
        now = datetime.now(timezone.utc)
        db.session.add(BlockedToken(jti=jti, type=token_type, created_at=now))

        refresh_token = kwargs.get("refresh_token")
        jti = get_jti(refresh_token)
        db.session.add(BlockedToken(jti=jti, type="refresh", created_at=now))

        db.session.commit()
        return {"success": True}


@doc(description="Email Verification", tags=["Auth"])
class EmailConfirmationResource(MethodResource):
    @use_kwargs(EmailConfirmationLoadSchema)
    def patch(self, **kwargs):
        verify_email(kwargs.get("token"))
        return render_template("email-confirmation.html")


@doc_protected(description="Get User Profile", tags=["Profile"])
class UserProfile(MethodResource):
    @marshal_with(UserSchema())
    @jwt_required()
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @marshal_with(UserSchema)
    @use_kwargs(
        UserSchema(
            only=("first_name", "last_name", "password", "email"),
            partial=True,
            load_instance=False,
        )
    )
    @jwt_required()
    def put(self, user_id, **kwargs):
        user = User.query.get_or_404(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()
        return user


class InternshipResource(Resource):
    @jwt_required()
    def post(self):
        internship_schema = InternshipSchema()
        internship = internship_schema.load(request.json)
        db.session.add(internship)
        db.session.commit()
        return internship_schema.dump(internship)
