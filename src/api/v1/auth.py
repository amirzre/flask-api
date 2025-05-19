from http import HTTPStatus

from flask import Blueprint, request

from src.controllers import AuthController
from src.schemas.auth import LoginRequest

auth_bp = Blueprint("auth", __name__)
auth_controller = AuthController()


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user.
    """
    data = request.get_json()

    login_request = LoginRequest(**data)
    response = auth_controller.login(login_request)

    return response.model_dump(), HTTPStatus.OK


@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    """
    Log out a user.
    """
    auth_controller.logout()

    return {}, HTTPStatus.NO_CONTENT
