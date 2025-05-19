from typing import Sequence, Tuple

from src.models import User
from src.repositories import BaseRepository
from src.schemas import UserFilterParams


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""

    def __init__(self):
        super().__init__(User)

    def get_by_id(self, id_: int) -> User | None:
        """
        Retrieve a user by ID.

        Args:
            id (ID): The ID of the user.

        Returns:
            User | None: The user instance if found; otherwise, None.
        """
        query = self._query()
        query = query.filter(User.id == id_)

        return self._one_or_none(query)

    def get_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by username.

        Args:
            username (str): The user's username.

        Returns:
            User | None: The user instance if found; otherwise, None.
        """
        query = self._query()
        query = query.filter(User.username == username)

        return self._one_or_none(query)

    def get_by_phone(self, phone: str) -> User | None:
        """
        Retrieve a user by phone.

        Args:
            phone (str): The user's phone.

        Returns:
            User | None: The user instance if found; otherwise, None.
        """
        query = self._query()
        query = query.filter(User.phone == phone)

        return self._one_or_none(query)

    def get_filtered_users(
        self, filter_params: UserFilterParams
    ) -> Tuple[Sequence[User], int]:
        """
        Retrieve a list of users filtered by the provided parameters, with pagination support.

        Args:
            filter_params (UserFilterParams): Filtering and pagination parameters.

        Returns:
            Tuple[Sequence[User], int]: A tuple containing a list of matching users and the total count.
        """
        query = self._query()

        if filter_params.username:
            query = query.filter(User.username == filter_params.username)
        if filter_params.phone:
            query = query.filter(User.phone == filter_params.phone)

        if filter_params.created_from:
            query = query.where(
                User.created >= f"{filter_params.created_from} 00:00:00"
            )
        if filter_params.created_to:
            query = query.where(User.created <= f"{filter_params.created_to} 23:59:59")

        query = query.order_by(User.created.desc())

        paginated_query = query.limit(filter_params.limit).offset(filter_params.offset)

        users = self._all(query=paginated_query)
        total = self._count(query=query)

        return users, total
