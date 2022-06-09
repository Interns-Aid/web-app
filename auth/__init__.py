from flask import Blueprint
from flask_restful import Api

from auth.resources.signup_resource import SignupResource

auth_bp = Blueprint('auth', __name__)
auth = Api(auth_bp)

auth.add_resource(SignupResource, '/signup')
