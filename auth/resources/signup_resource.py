from flask_restful import Resource


class SignupResource(Resource):
    def post(self):
        return {'success': False}
