def test_get_users(app, client):
    user = {
        'id': 1,
        'username': 'rajesh',
        'email': 'rajesh.k.khadka@gmail.com'
    }
    client.post('/api/v1/signup', json=user)

    response = client.get('/api/v1/signup')
    assert response.status_code == 200
    assert response.json == [user]


def test_post_users(app, client):
    user = {
        'id': 1,
        'username': 'rajesh',
        'email': 'rajesh.k.khadka@gmail.com'
    }
    response = client.post('/api/v1/signup', json=user)
    assert response.json == user
    assert response.status_code == 200
    assert response.json == user
