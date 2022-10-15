import json

from flask import Blueprint
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException, InternalServerError

APP_ERRORS = {
    "DUPLICATE_USER": ("User already exist with given username", 400),
    "INVALID_CREDENTIALS": ("Username/Password does not match", 401),
    "INACTIVE_USER": ("User has been disabled", 401),
}

bp = Blueprint("errors", __name__)


class BaseError(Exception):
    def __init__(self, key="", code="", name="", description=""):
        message, error_code = APP_ERRORS.get(key)
        self.code = error_code or code
        self.name = key or name
        self.description = message or description

    def to_json(self):
        return {"code": self.code, "name": self.name, "description": self.description}


def parse_response(e):
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@bp.app_errorhandler(BaseError)
def handle_generic_exception(e):
    return e.to_json(), e.code


@bp.app_errorhandler(ValidationError)
def handle_validation_error(e):
    return {"code": 400, "name": "BAD_REQUEST", "description": e.messages}, 400


@bp.app_errorhandler(HTTPException)
def handle_exception(e):
    return parse_response(e)


@bp.app_errorhandler(InternalServerError)
def handle_500(e):
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": 500,
            "name": "INTERNAL_SERVER_ERROR",
            "description": "Server encountered exception",
        }
    )
    response.content_type = "application/json"
    return response
