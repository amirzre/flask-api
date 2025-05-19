from flask import session
from werkzeug.security import check_password_hash

from src.exceptions import UnauthorizedException
from src.repositories import UserRepository
from src.schemas import LoginRequest, LoginResponse


class AuthController:
    """Business logic for Auth operations."""

    def __init__(self) -> None:
        """
        Initializes the AuthController.

        Args:
            user_repository (UserRepository): Repository instance for interacting with User model.
        """
        self.user_repository = UserRepository()

    def login(self, login_request: LoginRequest) -> LoginResponse:
        """
        Authenticate a user using provided credentials.

        Args:
            login_request (LoginRequest): Object containing user's username and password.

        Returns:
            LoginResponse: Object containing user info.

        Raises:
            BadRequestException: If credentials are invalid.
        """
        user = self.user_repository.get_by_username(login_request.username)
        if not user or not check_password_hash(user.password, login_request.password):
            raise UnauthorizedException(message="Invalid credentials.")

        session.clear()
        session["user_id"] = user.id
        return LoginResponse(id=user.id, username=user.username)

    def logout(self) -> None:
        """
        Log out a user by removing their user ID from session.
        """
        session.clear()
