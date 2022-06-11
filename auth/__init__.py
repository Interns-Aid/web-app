from flask import Blueprint
from flask_restful import Api

from resources.signup_resource import SignupResource

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")
api = Api(auth_bp)
api.add_resource(SignupResource, "/signup")
