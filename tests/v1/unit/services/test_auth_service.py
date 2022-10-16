from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from errors import BaseError
from services.auth import AuthService


@patch("models.user.User")
@patch("core.extensions.db")
@patch("services.email.EmailService")
def test_register_should_send_verification_email(email_service, db, user):
    auth_service = AuthService(email_service, db=db)

    auth_service.register(user)

    email_service.send.assert_called_once()
    db.session.commit.assert_called_once()


@patch("models.user.User")
@patch("core.extensions.db")
@patch("services.email.EmailService")
def test_register_should_raise_exception_when_username_is_duplicate(
    email_service, db, user
):
    db.session.commit = MagicMock(side_effect=IntegrityError("", "", ""))

    auth_service = AuthService(email_service, db=db)

    with pytest.raises(BaseError):
        auth_service.register(user)
