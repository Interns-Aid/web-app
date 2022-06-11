from flask import Blueprint
from flask_restful import Api

from auth import auth_bp

v1_bp = Blueprint('v1', __name__)
v1 = Api(v1_bp)
v1_bp.register_blueprint(auth_bp)
