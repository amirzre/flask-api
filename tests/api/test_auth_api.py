from http import HTTPStatus

import pytest
from werkzeug.security import generate_password_hash

from src.extensions import db
from src.models import User


def create_user(
    username: str = "testuser", phone: str = "091234567890", password: str = "Test@123"
) -> User:
    """
    Helper to create a user with hashed password in the database.
    """
    user = User(
        username=username, phone=phone, password=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    return user


class TestAuthEndpoints:
    """
    Tests for authentication endpoints:
    """

    @pytest.fixture(autouse=True)
    def setup(self, client, session):
        self.client = client
        db.session = session

    def test_login_success(self):
        """
        POST login with valid credentials should return 200 and user info, and set session cookie.
        """
        user = create_user(username="alice", phone="09123546677", password="Test@123")
        payload = {"username": "alice", "password": "Test@123"}

        response = self.client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        assert data["id"] == user.id
        assert data["username"] == "alice"
        assert any("session" in c for c in response.headers.get_all("Set-Cookie"))

    @pytest.mark.parametrize(
        "payload,expected_status",
        [
            ({"username": "no_user", "password": "pwd"}, HTTPStatus.UNAUTHORIZED),
            ({"username": "alice", "password": "wrong"}, HTTPStatus.UNAUTHORIZED),
        ],
    )
    def test_login_failures(self, payload, expected_status):
        """
        POST login with invalid username or password should return 401.
        """
        create_user(username="alice", phone="000", password="rightpass")
        response = self.client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == expected_status
        assert not response.headers.get_all("Set-Cookie")

    def test_logout(self):
        """
        DELETE /logout should clear the session and return 204 No Content.
        """
        create_user(username="bob", phone="09123546678", password="Test@123")
        payload = {"username": "bob", "password": "Test@123"}

        login_resp = self.client.post("/api/v1/auth/login", json=payload)
        assert login_resp.status_code == HTTPStatus.OK

        response = self.client.delete("/api/v1/auth/logout")
        assert response.status_code == HTTPStatus.NO_CONTENT

        cookies = response.headers.get_all("Set-Cookie")
        assert any("session=;" in c or "session=; Expires=" in c for c in cookies)
