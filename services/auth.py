from sqlalchemy.exc import IntegrityError

from core.extensions import db
from errors import BaseError
from models import User
from services.email import send_verification_email
from services.token import generate_verification_token, decode_token


def register(user: User):
    try:
        db.session.add(user)
        db.session.commit()
        token = generate_verification_token(user.email)
        send_verification_email(
            token=token, email=user.email, first_name=user.first_name
        )
    except IntegrityError:
        db.session.rollback()
        raise BaseError(key="DUPLICATE_USER")
    return user


def verify_email(token):
    if email := decode_token(token, expiration=86400):
        user = User.query.filter(User.email == email).one()
        user.active = True
        db.session.commit()
