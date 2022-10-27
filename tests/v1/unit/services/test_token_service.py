import time

import pytest

from errors import BaseError
from services.token import generate_verification_token, decode_token


def test_generate_verification_token():
    token = generate_verification_token("test@email.com")
    assert token is not None


def test_decode_token():
    email = "test@gmail.com"
    token = generate_verification_token(email)
    decoded_result = decode_token(token)
    assert email == decoded_result


def test_decode_raise_token_expired_exception():
    email = "test@gmail.com"
    token = generate_verification_token(email)
    time.sleep(1)
    with pytest.raises(BaseError) as e:
        decode_token(token, expiration=0.1)
        assert e.key == "EMAIL_VERIFICATION_TOKEN_EXPIRED"


def test_decode_raise_invalid_signature_exception():
    user_email = "inactive_user@mit.com"
    token = generate_verification_token(user_email)
    with pytest.raises(BaseError) as e:
        decode_token(token + "test")
        assert e.key == "BAD_TOKEN_SIGNATURE"
