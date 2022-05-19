from flask import Blueprint
from flask_restful import Resource, Api


class V1Resource(Resource):
    @classmethod
    def get(cls):
        return {"version1": "v1"}


v1 = Blueprint("v1", import_name="v1", url_prefix="/api/v1")
v1_api = Api(v1)
v1_api.add_resource(V1Resource, "/")