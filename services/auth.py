from sqlalchemy.exc import IntegrityError

from errors import BaseError
from models import User


class AuthService:
    def __init__(self, email_service, db):
        self.email_service = email_service
        self.db = db

    def register(self, user: User):
        try:
            self.db.session.add(user)
            self.db.session.commit()
            self.email_service.send()
        except IntegrityError:
            raise BaseError(key="DUPLICATE_USER")
        return user
