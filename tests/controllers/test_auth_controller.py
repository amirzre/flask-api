import pytest
from flask import session
from werkzeug.security import generate_password_hash

from src.controllers import AuthController
from src.models import User
from src.schemas import LoginRequest, LoginResponse
from src.exceptions import UnauthorizedException
from src.extensions import db


def create_user(username: str = "testuser", phone: str = "09123456789", password: str = "Test@123") -> User:
    """
    Helper to create and persist a single User instance with a hashed password.
    """
    hashed = generate_password_hash(password)
    user = User(username=username, phone=phone, password=hashed)
    db.session.add(user)
    db.session.commit()
    return user


class TestAuthController:
    """
    Tests for the login and logout method of AuthController.
    """

    @pytest.fixture(autouse=True)
    def setup(self, app, session):
        db.session = session
        self.controller = AuthController()
        self.app = app

    def test_login_success(self):
        """
        login should authenticate a valid user and set session['user_id'].
        """
        user = create_user(username="alice", phone="09123456781", password="Test@123")
        req = LoginRequest(username="alice", password="Test@123")
        with self.app.test_request_context():
            response = self.controller.login(login_request=req)

            assert isinstance(response, LoginResponse)
            assert response.id == user.id
            assert response.username == "alice"
            assert session.get("user_id") == user.id

    def test_login_invalid_username(self):
        """
        login should raise UnauthorizedException for non-existent username.
        """
        req = LoginRequest(username="no_user", password="pwd")
        with self.app.test_request_context():
            with pytest.raises(UnauthorizedException):
                self.controller.login(login_request=req)

    def test_login_invalid_password(self):
        """
        login should raise UnauthorizedException for incorrect password.
        """
        create_user(username="bob", phone="09123456780", password="Test@123")
        req = LoginRequest(username="bob", password="wrongpass")
        with self.app.test_request_context():
            with pytest.raises(UnauthorizedException):
                self.controller.login(login_request=req)

    def test_logout_clears_session(self):
        """
        logout should remove user_id from session.
        """
        with self.app.test_request_context():
            session['user_id'] = 123
            assert 'user_id' in session

            self.controller.logout()
            assert 'user_id' not in session
            assert session == {}


