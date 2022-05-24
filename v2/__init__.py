from flask_restful import Resource, Api
from flask import Blueprint


class V2Resource(Resource):
    @classmethod
    def get(cls):
        return {"version2": "v2"}


v2 = Blueprint("v2", import_name=__name__)
api_v2 = Api(v2)

api_v2.add_resource(V2Resource, "/")
