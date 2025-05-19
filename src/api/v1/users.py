from http import HTTPStatus

from flask import Blueprint, request

from src.controllers import UserController
from src.schemas import (
    PaginationResponse,
    RegisterUser,
    UpdateUser,
    UserFilterParams,
    UserResponse,
)

user_bp = Blueprint("users", __name__)
user_controller = UserController()


@user_bp.route("", methods=["GET"])
def get_users():
    """
    Get a list of users with filtering and pagination.
    """
    params = {}

    if "limit" in request.args:
        params["limit"] = int(request.args.get("limit", 100))
    if "offset" in request.args:
        params["offset"] = int(request.args.get("offset", 0))
    if "order_by" in request.args:
        params["order_by"] = request.args.get("order_by")

    if "username" in request.args:
        params["username"] = request.args.get("username")
    if "phone" in request.args:
        params["phone"] = request.args.get("phone")

    if "created_from" in request.args:
        params["created_from"] = request.args.get("created_from")

    if "created_to" in request.args:
        params["created_to"] = request.args.get("created_to")

    filter_params = UserFilterParams(**params)

    pagination_response: PaginationResponse[UserResponse] = user_controller.get_users(
        filter_params=filter_params
    )

    return pagination_response.model_dump(), HTTPStatus.OK


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """
    Get a user by ID.
    """
    user_response: UserResponse = user_controller.get_user(user_id)

    return user_response.model_dump(), HTTPStatus.OK


@user_bp.route("", methods=["POST"])
def register_user():
    """
    Register a new user.
    """

    user_data = request.get_json()

    register_user = RegisterUser(**user_data)
    user_response: UserResponse = user_controller.register_user(
        register_user=register_user
    )

    return user_response.model_dump(), HTTPStatus.CREATED


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    """
    Update an existing user.
    """
    user_data = request.get_json()

    update_user_request = UpdateUser(**user_data)

    updated_user: UserResponse = user_controller.update_user(
        user_id=user_id, update_user_request=update_user_request
    )

    return updated_user.model_dump(), HTTPStatus.OK


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """
    Delete a user by ID.
    """
    user_controller.delete_user(user_id=user_id)

    return {}, HTTPStatus.NO_CONTENT
