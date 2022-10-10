import pytest

from models import User


@pytest.mark.parametrize('body,status_code,data',
                         [({'username': 'rajesh',
                            'email': 'rajesh.k.khadka@gmail.com',
                            'password': 'pass'}, 400,
                           {'code': 400,
                            'description': {'password': ['invalid password']},
                            'name': 'BAD_REQUEST'}),
                          ({'username': 'rajesh',
                            'email': 'rajesh.k.khadka@gmail.com',
                            'password': 'Pass@1234'}, 400,
                           {'code': 400,
                            'description': 'User already exist with given username',
                            'name': 'DUPLICATE_USER'})])
@pytest.mark.usefixtures("app_ctx")
def test_post_users(body, status_code, data, client):
    """
    test 1: invalid password
    test 2: username already exist
    """
    response = client.post('/api/v1/signup', json=body)
    assert response.status_code == status_code
    assert response.json == data


@pytest.mark.usefixtures("app_ctx")
def test_create_user(client):
    email = 'test_email@gmail.com'
    password = 'Password@1234'
    data = {
        'username': 'test_username',
        'email': email,
        'password': password
    }
    response = client.post('/api/v1/signup', json=data)
    user = User.query.get(response.json.get('id'))
    assert user is not None
    assert user.email == email
