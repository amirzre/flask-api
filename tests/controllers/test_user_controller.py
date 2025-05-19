from datetime import datetime, timedelta, timezone

import pytest

from src.controllers import UserController
from src.exceptions import BadRequestException, NotFoundException
from src.extensions import db
from src.models import User
from src.schemas import (
    RegisterUser,
    UpdateUser,
    UserFilterParams,
    UserResponse,
)


def create_user(
    username: str = "testuser", phone: str = "09123456789", password: str = "Test@1235"
) -> User:
    """
    Helper to create and persist a single User instance.
    """
    user = User(username=username, phone=phone, password=password)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserController:
    """
    Tests for methods in UserController:
    """

    @pytest.fixture(autouse=True)
    def setup(self, session):
        db.session = session
        self.controller = UserController()

    def test_get_user_found(self):
        """
        get_user should return correct UserResponse when user exists.
        """
        user = create_user(username="alice", phone="11122233344", password="pwd")
        response = self.controller.get_user(user_id=user.id)

        assert isinstance(response, UserResponse)
        assert response.id == user.id
        assert response.username == "alice"
        assert response.phone == "11122233344"

    def test_get_user_not_found(self):
        """
        get_user should raise NotFoundException for non-existent user.
        """
        with pytest.raises(NotFoundException):
            self.controller.get_user(user_id=9999)

    def test_get_users_no_filters(self):
        """
        get_users should return all users when no filters are applied.
        """
        # create multiple users with different creation dates
        now = datetime.now(timezone.utc)
        users = [
            User(
                username=f"user{i}",
                phone=f"000{i}",
                password="pwd",
                created=now - timedelta(days=i),
            )
            for i in range(3)
        ]
        db.session.add_all(users)
        db.session.commit()

        params = UserFilterParams(
            username=None,
            phone=None,
            created_from=None,
            created_to=None,
            limit=10,
            offset=0,
        )
        paginated = self.controller.get_users(filter_params=params)

        assert paginated.total == 3
        assert len(paginated.items) == 3
        returned_ids = {item.id for item in paginated.items}
        assert returned_ids == {u.id for u in users}

    def test_register_user_success(self):
        """
        register_user should create a new user and return UserResponse.
        """
        req = RegisterUser(username="bob", phone="09123456781", password="Test@123")
        response = self.controller.register_user(register_user=req)

        assert isinstance(response, UserResponse)
        assert response.username == "bob"
        assert response.phone == "09123456781"

        user = db.session.query(User).filter_by(username="bob").one_or_none()
        assert user is not None
        assert user.phone == "09123456781"

    def test_register_user_conflict(self):
        """
        register_user should raise BadRequestException if username already exists.
        """
        create_user(username="sam", phone="09123456781", password="Test@123")
        req = RegisterUser(username="sam", phone="09123456780", password="Test@123")
        with pytest.raises(BadRequestException):
            self.controller.register_user(register_user=req)

    def test_update_user_success(self):
        """
        update_user should change provided fields and return updated UserResponse.
        """
        user = create_user(username="eve", phone="09123456789", password="Test@123")
        req = UpdateUser(phone="09123456780", password="Test@1234")
        response = self.controller.update_user(user_id=user.id, update_user_request=req)

        assert isinstance(response, UserResponse)
        assert response.phone == "09123456780"

        updated = db.session.query(User).get(user.id)
        assert updated.phone == "09123456780"

    def test_update_user_not_found(self):
        """
        update_user should raise NotFoundException for non-existent user.
        """
        req = UpdateUser(phone="09123456780")
        with pytest.raises(NotFoundException):
            self.controller.update_user(user_id=8888, update_user_request=req)

    def test_delete_user_success(self):
        """
        delete_user should remove the user from the database.
        """
        user = create_user(username="tom", phone="55566677788", password="pwd")
        self.controller.delete_user(user_id=user.id)

        assert db.session.query(User).get(user.id) is None

    def test_delete_user_not_found(self):
        """
        delete_user should raise NotFoundException when user does not exist.
        """
        with pytest.raises(NotFoundException):
            self.controller.delete_user(user_id=7777)
