from .conftest import register


def test_customer_can_register(client):
    response = register(client)
    assert response.status_code == 200
    assert b"Your account has been created" in response.data


def test_duplicate_registration_is_rejected(client):
    register(client)
    client.post("/auth/logout")
    response = register(client)
    assert b"already exists" in response.data


def test_invalid_login_is_rejected(client):
    response = client.post("/auth/login", data={"email": "nobody@test.com", "password": "wrong"})
    assert b"Incorrect email or password" in response.data

