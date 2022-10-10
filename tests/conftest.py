import pytest

from app import create_app
from core.extensions import db
from models import User


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def app():
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
        data = {'username': 'rajesh',
                'email': 'rajesh@mit.com',
                'password': 'mit@1234',
                'first_name': 'rajesh',
                'last_name': 'khadka',
                'active': True}
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        yield User.query.all()
        User.query.delete()
