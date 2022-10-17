from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


def generate_verification_token(key: str) -> str:
    serializer = URLSafeTimedSerializer(secret_key=app.config.get("SECRET_KEY"))
    return serializer.dumps(key, salt=app.config.get("SECURITY_PASSWORD_SALT"))


def decode_token(token, expiration=3600) -> str:
    serializer = URLSafeTimedSerializer(secret_key=app.config.get("SECRET_KEY"))
    try:
        return serializer.loads(
            token, salt=app.config.get("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
    except SignatureExpired:
        return ""
