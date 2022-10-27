from unittest.mock import patch

import pytest

from errors import BaseError
from models import User
from schemas.user import UserSchema
from services.auth import register, verify_email
from services.token import generate_verification_token


@patch("services.auth.send_verification_email")
def test_register_should_send_verification_email(send_verification_email):
    data = {
        "username": "test_user",
        "email": "test_user@email.com",
        "password": "ActiveUser@1234",
        "first_name": "Test User",
        "last_name": "Last Name",
    }
    user_schema = UserSchema()
    user = user_schema.load(data)
    register(user)
    send_verification_email.assert_called_once()


def test_register_should_raise_exception_when_username_is_duplicate():
    data = {
        "username": "active_user",
        "email": "active_user@email.com",
        "password": "ActiveUser@1234",
        "first_name": "Active User",
        "last_name": "Last Name",
    }
    user_schema = UserSchema()
    user = user_schema.load(data)
    with pytest.raises(BaseError):
        register(user)


@pytest.mark.usefixtures("app_ctx")
def test_verify_email():
    user_email = "inactive_user@mit.com"
    token = generate_verification_token(user_email)
    verify_email(token)
    user = User.query.filter(User.email == user_email).one()
    assert user.active == True
