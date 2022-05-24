from flask import Blueprint
from flask_restful import Resource, Api


v1 = Blueprint("version1", import_name=__name__)
v1_api = Api(v1)


class V1Resource(Resource):
    @classmethod
    def get(cls):
        return {"version1": "v1"}


v1_api.add_resource(V1Resource, "/")







