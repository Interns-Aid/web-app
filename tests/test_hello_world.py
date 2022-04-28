def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"hello": "world"}
