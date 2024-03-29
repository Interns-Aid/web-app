from flask import Blueprint
from flask_restful import Api

from v1.routes import (
    SignupResource,
    LoginResource,
    TokenRefreshResource,
    LogoutResource,
    UserProfile,
    InternshipResource,
    EmailConfirmationResource,
)

v1_bp = Blueprint("v1", __name__)
v1 = Api(v1_bp)
v1.add_resource(SignupResource, "/signup")
v1.add_resource(LoginResource, "/login")
v1.add_resource(TokenRefreshResource, "/refresh")
v1.add_resource(LogoutResource, "/logout")
v1.add_resource(UserProfile, "/users/<string:user_id>/profile")
v1.add_resource(EmailConfirmationResource, "/email-confirmation")
v1.add_resource(InternshipResource, "/internships")
