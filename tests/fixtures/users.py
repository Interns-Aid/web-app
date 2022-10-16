import pytest
from werkzeug.security import generate_password_hash

from core.extensions import db
from models import User


@pytest.fixture(autouse=True)
def users(app):
    with app.app_context():
        active_user = {
            "username": "active_user",
            "email": "active_user@mit.com",
            "password": "Mit@1234",
            "first_name": "active",
            "last_name": "user",
            "active": True,
        }

        user = User(**active_user)
        user.password = generate_password_hash(user.password)
        db.session.add(user)
        db.session.commit()

        inactive_user = {
            "username": "inactive_user",
            "email": "inactive_user@mit.com",
            "password": "Lol@1234",
            "first_name": "Inactive",
            "last_name": "User",
            "active": False,
        }

        user = User(**inactive_user)
        user.password = generate_password_hash(user.password)
        db.session.add(user)
        db.session.commit()

        yield User.query.all()
        User.query.delete()


@pytest.fixture
@pytest.mark.usefixtures("app_ctx")
def active_user():
    user = User.query.filter_by(active=True).first()
    yield user
