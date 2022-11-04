import pytest

from models import User, Internship
from services.token import generate_verification_token


@pytest.mark.parametrize(
    "body,status_code,data",
    [
        (
            {
                "username": "rajesh",
                "email": "rajesh.k.khadka@gmail.com",
                "first_name": "Rajesh",
                "last_name": "Khadka",
                "password": "pass",
            },
            400,
            {
                "code": 400,
                "description": {"password": ["invalid password"]},
                "name": "BAD_REQUEST",
            },
        ),
        (
            {
                "username": "active_user",
                "first_name": "Active",
                "last_name": "User",
                "email": "active_user@mit.com",
                "password": "Pass@1234",
            },
            400,
            {
                "code": 400,
                "description": "User already exist with given username",
                "name": "DUPLICATE_USER",
            },
        ),
    ],
)
@pytest.mark.usefixtures("app_ctx")
def test_post_users(body, status_code, data, client):
    """
    test 1: invalid password
    test 2: username already exist
    """
    response = client.post("/api/v1/signup", json=body)
    # assert response.status_code == status_code
    assert response.json == data


@pytest.mark.usefixtures("app_ctx")
def test_create_user(client):
    email = "test_email@gmail.com"
    password = "Password@1234"
    test_username = "test_username"
    first_name = "first_name"
    last_name = "last_name"
    data = {
        "username": test_username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    }
    response = client.post("/api/v1/signup", json=data)
    user = User.query.get(response.json.get("id"))
    assert user is not None
    assert user.email == email


@pytest.mark.parametrize(
    "body,status_code,data",
    [
        (
            {"username": "TestUser", "password": "RandomPass@12345"},
            401,
            {
                "code": 401,
                "description": "Username/Password does not match",
                "name": "INVALID_CREDENTIALS",
            },
        )
    ],
)
@pytest.mark.usefixtures("app_ctx")
def test_login_failure(body, status_code, data, client, users):
    response = client.post("/api/v1/login", json=body)
    assert response.status_code == status_code
    assert response.json == data


@pytest.mark.usefixtures("app_ctx")
def test_login_success(client, users):
    data = {"username": users[0].username, "password": users[0].password}
    response = client.post("/api/v1/login", json=data)
    response_body = response.json
    response.status_code == 200
    response_body.get("access_token") is not None
    response_body.get("refresh_token") is not None
    response_body.get("username") == users[0].username


@pytest.mark.usefixtures("app_ctx")
def test_login_inactive_user(client, users):
    inactive_user = User.query.filter_by(active=False).first()
    data = {"username": inactive_user.username, "password": inactive_user.password}
    response = client.post("/api/v1/login", json=data)
    assert response.status_code == 401
    assert response.json == {
        "code": 401,
        "description": "Username/Password does not match",
        "name": "INVALID_CREDENTIALS",
    }


@pytest.mark.usefixtures("app_ctx")
def test_refresh_token(token_refresh_client):
    response = token_refresh_client.post("/api/v1/refresh")
    assert response.json.get("access_token") is not None


@pytest.mark.usefixtures("app_ctx")
def test_user_profile(authenticated_client, user):
    response = authenticated_client.get(
        f"/api/v1/users/{user.get('user').get('id')}/profile"
    )
    assert response.status_code == 200
    assert response.json.get("username") == "active_user"


def test_update_profile(authenticated_client, user, client):
    updated_password = "Updated@PW123"
    updated_first_name = "updated_first_name"
    updated_last_name = "updated_last_name"
    updated_email = "updated_email@gmail.com"

    response = authenticated_client.put(
        f"/api/v1/users/{user.get('user').get('id')}/profile",
        json={
            "first_name": updated_first_name,
            "last_name": updated_last_name,
            "email": updated_email,
            "password": updated_password,
        },
    )
    assert response.status_code == 200
    assert response.json.get("first_name") == updated_first_name
    assert response.json.get("last_name") == updated_last_name
    assert response.json.get("email") == updated_email

    # login with updated password
    response = client.post(
        "/api/v1/login", json={"username": "active_user", "password": updated_password}
    )
    assert response.status_code == 200
    assert response.json.get("id") == user.get("id")


@pytest.mark.usefixtures("app_ctx")
def test_logout(client):
    response = client.post(
        "/api/v1/login", json={"username": "active_user", "password": "Mit@1234"}
    )
    access_token, refresh_token, user_id = (
        response.json.get("access_token"),
        response.json.get("refresh_token"),
        response.json.get("user").get("id"),
    )

    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
    response = client.post("/api/v1/logout", json={"refresh_token": refresh_token})
    assert response.json == {"success": True}

    # verify refresh token is revoked or not
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {refresh_token}"
    response = client.post("/api/v1/refresh")
    assert response.json == {"msg": "Token has been revoked"}

    # verify access token is revoked or not
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
    response = client.get(f"/api/v1/users/{user_id}/profile")
    assert response.json == {"msg": "Token has been revoked"}


@pytest.mark.parametrize(
    "data,status_code",
    [
        (
            {
                "assignment": {
                    "duration": "45 minutes",
                    "platform": "CodeSignal",
                    "questions": [
                        {"title": "Find the duplicate elements"},
                        {"title": "Find the word count"},
                    ],
                    "title": "Coding Test",
                    "type": "coding",
                },
                "attachments": [
                    {"url": "www.internsaid.com/docs_1.pdf"},
                    {"url": "www.internsaid.com/docs_2.pdf"},
                ],
                "company": {
                    "location": "France",
                    "name": "Google",
                    "website": "www.google.com",
                },
                "tags": [{"title": "python"}, {"title": "flask"}],
                "title": "Backend Developer Internship",
            },
            200,
        ),
    ],
)
@pytest.mark.usefixtures("app_ctx")
def test_create_internship(data, status_code, authenticated_client):
    response = authenticated_client.post("/api/v1/internships", json=data)
    assert response.status_code == status_code
    if status_code == 200:
        assert (
            data.get("title")
            == Internship.query.filter_by(title=data.get("title")).first().title
        )


def test_email_verification(client):
    user_email = "inactive_user@mit.com"
    token = generate_verification_token(user_email)
    response = client.patch("api/v1/email-confirmation", json={"token": token})
    assert response.status_code == 200


def test_email_verification_should_return_error(client):
    user_email = "inactive_user@mit.com"
    token = generate_verification_token(user_email)
    mangled_token = token + "test"
    response = client.patch("api/v1/email-confirmation", json={"token": mangled_token})
    assert response.status_code == 400
    assert response.json == {
        "code": 400,
        "description": "Invalid Signature",
        "name": "BAD_TOKEN_SIGNATURE",
    }
