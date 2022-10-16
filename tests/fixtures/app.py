import pytest
from dotenv import load_dotenv

from app import create_app
from core.extensions import db


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def app():
    load_dotenv(".env")
    app = create_app("config.TestingConfig")
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
    response = test_client.post(
        "/api/v1/login", json={"username": "active_user", "password": "Mit@1234"}
    )
    return response.json


@pytest.fixture()
def authenticated_client(user, client):
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {user.get('access_token')}"
    return client


@pytest.fixture()
def token_refresh_client(client, user):
    refresh_token = user.get("refresh_token")
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {refresh_token}"
    return client
