from werkzeug.security import generate_password_hash

from src.exceptions import BadRequestException, NotFoundException
from src.repositories import UserRepository
from src.schemas import (
    PaginationResponse,
    RegisterUser,
    UpdateUser,
    UserFilterParams,
    UserResponse,
)


class UserController:
    """Business logic for User operations."""

    def __init__(self) -> None:
        """
        Initializes the UserController.

        Args:
            user_repository (UserRepository): Repository instance for interacting with User model.
        """
        self.user_repository = UserRepository()

    def get_users(
        self, filter_params: UserFilterParams
    ) -> PaginationResponse[UserResponse]:
        """
        Retrieves a list of users based on filter parameters.

        Args:
            filter_params (UserFilterParams): Filtering and pagination parameters.

        Returns:
            PaginationResponse[UserResponse]: Paginated list of users.
        """
        users, total = self.user_repository.get_filtered_users(
            filter_params=filter_params
        )

        return PaginationResponse[UserResponse](
            limit=filter_params.limit,
            offset=filter_params.offset,
            total=total,
            items=[UserResponse.model_validate(user) for user in users],
        )

    def get_user(self, user_id: int) -> UserResponse:
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): Unique identifier of the user.

        Returns:
            UserResponse: User data.

        Raises:
            NotFoundException: If user does not exist.
        """
        user = self.user_repository.get_by_id(id_=user_id)
        if not user:
            raise NotFoundException(message="User not found.")

        return UserResponse(
            id=user.id,
            username=user.username,
            phone=user.phone,
            created=user.created,
        )

    def register_user(self, register_user: RegisterUser) -> UserResponse:
        """
        Registers a new user.

        Args:
            register_user_request (RegisterUserRequest): User registration data.

        Returns:
            UserResponse: Data of the newly created user.

        Raises:
            BadRequestException: If email already exists.
        """
        user = self.user_repository.get_by_username(username=register_user.username)
        if user:
            raise BadRequestException(message="User already exists with this username.")

        hashed_password = generate_password_hash(password=register_user.password)

        user_data = register_user.model_dump(exclude_unset=True)
        user_data["password"] = hashed_password
        created_user = self.user_repository.create(attributes=user_data)

        return UserResponse(
            id=created_user.id,
            username=created_user.username,
            phone=created_user.phone,
            created=created_user.created,
        )

    def update_user(
        self, *, user_id: int, update_user_request: UpdateUser
    ) -> UserResponse:
        """
        Updates an existing user's data.

        Args:
            user_id (int): Unique identifier of the user.
            update_user (UpdateUser): Updated user data.

        Returns:
            UserResponse: Updated user data.

        Raises:
            NotFoundException: If user does not exist.
        """
        user = self.user_repository.get_by_id(id_=user_id)
        if not user:
            raise NotFoundException(message="User not found.")

        update_data = update_user_request.model_dump(exclude_unset=True)
        new_password = update_data.get("password")
        if new_password:
            update_data["password"] = generate_password_hash(password=new_password)

        updated_user = self.user_repository.update(model=user, attributes=update_data)

        return UserResponse(
            id=updated_user.id,
            username=updated_user.username,
            phone=updated_user.phone,
            created=updated_user.created,
        )

    def delete_user(self, *, user_id: int) -> None:
        """
        Deletes a user by UUID.

        Args:
            user_id (int): Unique identifier of the user.

        Returns:
            UserResponse: Deleted user data.

        Raises:
            NotFoundException: If user does not exist.
        """
        user = self.user_repository.get_by_id(id_=user_id)
        if not user:
            raise NotFoundException(message="User not found.")

        return self.user_repository.delete(model=user)
