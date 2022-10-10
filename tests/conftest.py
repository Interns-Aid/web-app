import pytest
from dotenv import load_dotenv

from app import create_app
from core.extensions import db
from models import User
from schemas.user import UserSchema


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def app():
    load_dotenv('.env')
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def users(app):
    with app.app_context():
        user_schema = UserSchema()

        active_user = {'username': 'active_user',
                       'email': 'active_user@mit.com',
                       'password': 'Mit@1234',
                       'first_name': 'active',
                       'last_name': 'user',
                       'active': True}
        user = user_schema.load(active_user)
        db.session.add(user)

        inactive_user = {'username': 'inactive_user',
                         'email': 'inactive_user@mit.com',
                         'password': 'Lol@1234',
                         'first_name': 'Inactive',
                         'last_name': 'User',
                         'active': False}

        user = user_schema.load(inactive_user)
        db.session.add(user)

        db.session.commit()

        yield User.query.all()
        User.query.delete()
