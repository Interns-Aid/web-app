import pytest

from models import User


@pytest.mark.parametrize('body,status_code,data',
                         [({'username': 'rajesh',
                            'email': 'rajesh.k.khadka@gmail.com',
                            'password': 'pass'}, 400,
                           {'code': 400,
                            'description': {'password': ['invalid password']},
                            'name': 'BAD_REQUEST'}),
                          ({'username': 'active_user',
                            'email': 'active_user@mit.com',
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
    test_username = 'test_username'
    data = {
        'username': test_username,
        'email': email,
        'password': password
    }
    response = client.post('/api/v1/signup', json=data)
    user = User.query.get(response.json.get('id'))
    assert user is not None
    assert user.email == email


@pytest.mark.parametrize('body,status_code,data',
                         [({'username': 'TestUser',
                            'password': 'RandomPass@12345'},
                           401,
                           {'code': 401,
                            'description': 'Username/Password does not match',
                            'name': 'INVALID_CREDENTIALS'})])
@pytest.mark.usefixtures('app_ctx')
def test_login_failure(body, status_code, data, client, users):
    response = client.post('/api/v1/login', json=body)
    assert response.status_code == status_code
    assert response.json == data


@pytest.mark.usefixtures('app_ctx')
def test_login_success(client, users):
    data = {'username': users[0].username,
            'password': users[0].password}
    response = client.post('/api/v1/login', json=data)
    response_body = response.json
    response.status_code == 200
    response_body.get('access_token') is not None
    response_body.get('refresh_token') is not None
    response_body.get('username') == users[0].username


@pytest.mark.usefixtures('app_ctx')
def test_login_inactive_user(client, users):
    inactive_user = User.query.filter_by(active=False).first()
    data = {
        'username': inactive_user.username,
        'password': inactive_user.password
    }
    response = client.post('/api/v1/login', json=data)
    assert response.status_code == 401
    assert response.json == {'code': 401,
                             'description': 'Username/Password does not match',
                             'name': 'INVALID_CREDENTIALS'}
