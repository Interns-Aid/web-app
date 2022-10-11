import pytest
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from app import create_app
from core.extensions import db
from models import User


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


@pytest.fixture()
def user(app):
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', json={'username': 'active_user',
                                                       'password': 'Mit@1234'})
    return response.json


@pytest.fixture()
def authenticated_client(user, client):
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {user.get('access_token')}"
    return client


@pytest.fixture()
def token_refresh_client(client, user):
    refresh_token = user.get('refresh_token')
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {refresh_token}'
    return client


@pytest.fixture(autouse=True)
def users(app):
    with app.app_context():
        active_user = {'username': 'active_user',
                       'email': 'active_user@mit.com',
                       'password': 'Mit@1234',
                       'first_name': 'active',
                       'last_name': 'user',
                       'active': True}

        user = User(**active_user)
        user.password = generate_password_hash(user.password)
        db.session.add(user)
        db.session.commit()

        inactive_user = {'username': 'inactive_user',
                         'email': 'inactive_user@mit.com',
                         'password': 'Lol@1234',
                         'first_name': 'Inactive',
                         'last_name': 'User',
                         'active': False}

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
