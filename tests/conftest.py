import pytest
from common.app_initialization import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    return app


@pytest.fixture(autouse=True)
def client(app):
    client = app.test_client()
    yield client



