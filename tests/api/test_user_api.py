from http import HTTPStatus

import pytest
from werkzeug.security import generate_password_hash

from src.extensions import db
from src.models import User


def create_user(
    username: str = "testuser", phone: str = "09123456789", password: str = "Test@123"
) -> User:
    """
    Helper to create and persist a single User instance.
    """
    user = User(
        username=username,
        phone=phone,
        password=generate_password_hash(password),
        created="1404-02-29 18:57:15",
    )

    db.session.add(user)
    db.session.commit()
    return user


def login(client, username: str, password: str):
    """
    Helper to log in via the auth endpoint and preserve session cookie.
    """
    resp = client.post(
        "/api/v1/auth/login", json={"username": username, "password": password}
    )
    assert resp.status_code == HTTPStatus.OK
    return resp


class TestUserBlueprintEndpoints:
    """
    Tests for user management endpoints.
    """

    @pytest.fixture(autouse=True)
    def setup(self, client, session):
        db.session = session
        self.client = client

        self.admin = create_user(
            username="admin", phone="09123456780", password="Test@123"
        )
        login(self.client, "admin", "Test@123")

    def test_get_users_success(self):
        """
        Test get users should return 200 and list of users when authenticated.
        """
        user1 = create_user(username="alice", phone="09123456781", password="Test@123")
        user2 = create_user(username="bob", phone="09123456782", password="Test@123")

        resp = self.client.get("/api/v1/users?limit=10&offset=0")
        assert resp.status_code == HTTPStatus.OK
        data = resp.get_json()
        assert data["total"] >= 3
        ids = {item["id"] for item in data["items"]}
        assert self.admin.id in ids and user1.id in ids and user2.id in ids

    def test_get_user_success(self):
        """
        Test get user returns 200 and correct user data.
        """
        user = create_user(username="user3", phone="09123456783", password="Test@123")
        resp = self.client.get(f"/api/v1/users/{user.id}")
        assert resp.status_code == HTTPStatus.OK
        data = resp.get_json()
        assert data["id"] == user.id
        assert data["username"] == "user3"

    def test_get_user_not_found(self):
        """
        Test not found user returns 404.
        """
        resp = self.client.get("/api/v1/users/9999")
        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_register_user_success(self):
        """
        Test creates a new user and returns 201.
        """
        payload = {"username": "user4", "phone": "09123456784", "password": "Test@123"}
        resp = self.client.post("/api/v1/users", json=payload)
        assert resp.status_code == HTTPStatus.CREATED
        data = resp.get_json()
        assert data["username"] == "user4"
        assert data["phone"] == "09123456784"

    def test_register_user_conflict(self):
        """
        Test create user with existing username returns 400 Bad Request.
        """
        create_user(username="user5", phone="09123456785", password="Test@123")
        payload = {"username": "user5", "phone": "09123456784", "password": "Test@123"}
        resp = self.client.post("/api/v1/users", json=payload)

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_update_user_success(self):
        """
        Test updates an existing user and returns 200.
        """
        user = create_user(username="frank", phone="09123456786", password="Test@123")
        payload = {"phone": "09123456787", "password": "Test@1234"}
        resp = self.client.put(f"/api/v1/users/{user.id}", json=payload)

        assert resp.status_code == HTTPStatus.OK
        data = resp.get_json()
        assert data["phone"] == "09123456787"

    def test_update_user_not_found(self):
        """
        Test updates not found user returns 404.
        """
        payload = {"phone": "09123456788"}
        resp = self.client.put("/api/v1/users/8888", json=payload)
        assert resp.status_code == HTTPStatus.NOT_FOUND

    def test_delete_user_success(self):
        """
        Test delete user removes the user and returns 204.
        """
        user = create_user(username="grace", phone="09123456789", password="Test@1234")
        resp = self.client.delete(f"/api/v1/users/{user.id}")
        assert resp.status_code == HTTPStatus.NO_CONTENT

        resp2 = self.client.get(f"/api/v1/users/{user.id}")
        assert resp2.status_code == HTTPStatus.NOT_FOUND

    def test_delete_user_not_found(self):
        """
        Test delete not exists user returns 404.
        """
        resp = self.client.delete("/api/v1/users/9999")
        assert resp.status_code == HTTPStatus.NOT_FOUND
