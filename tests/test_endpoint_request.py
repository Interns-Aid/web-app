
def test_should_make_request(client):
    response = client.get('/api/v1/')
    assert response.status_code == 200
    assert response.json == {"version1": "v1"}