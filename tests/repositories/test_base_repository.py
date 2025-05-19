import pytest
from datetime import datetime, timezone
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError

from src.extensions import db
from src.repositories.base import BaseRepository


class DummyModel(db.Model):
    """
    A simple model for testing BaseRepository.
    """
    __tablename__ = 'dummy_models'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timestamp = Column(db.DateTime, nullable=True)


class DummySchema(BaseModel):
    """
    Pydantic schema matching DummyModel fields.
    """
    name: str
    timestamp: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# Ensure the test table is created before any tests run
@pytest.fixture(scope="module", autouse=True)
def setup_tables(engine):
    """
    Create all tables for DummyModel before tests and drop them afterward.
    """
    db.metadata.create_all(bind=engine)
    yield
    db.metadata.drop_all(bind=engine)


pytestmark = pytest.mark.usefixtures("session")


class TestCreateDelete:
    """
    Tests for create() and delete() methods of BaseRepository.
    """

    @pytest.fixture(autouse=True)
    def repo(self) -> BaseRepository[DummyModel]:
        """
        Provide a repository instance for DummyModel.
        """
        return BaseRepository(DummyModel)

    def test_create_with_dict(self, repo):
        """
        Creating a model using a plain dict should persist and return the new instance.
        """
        attrs: Dict[str, Any] = {"name": "foo"}
        instance = repo.create(attrs)

        assert isinstance(instance, DummyModel)
        assert instance.id is not None
        assert instance.name == "foo"

    def test_create_with_pydantic_model(self, repo):
        """
        Creating using a Pydantic BaseModel should also work and strip tzinfo from datetimes.
        """
        now = datetime.now(timezone.utc)
        schema = DummySchema(name="bar", timestamp=now)
        instance = repo.create(schema)

        assert instance.timestamp.tzinfo is None
        assert instance.name == "bar"

    def test_delete_success(self, repo):
        """
        Deleting an existing instance should remove it from the database.
        """
        inst = repo.create({"name": "to_delete"})
        repo.delete(inst)

        assert repo._one_or_none(repo._query().where(DummyModel.id == inst.id)) is None

    def test_delete_nonexistent_raises(self, repo):
        """
        Deleting an object not in the session should raise SQLAlchemyError.
        """
        fake = DummyModel(name="fake")
        with pytest.raises(SQLAlchemyError):
            repo.delete(fake)

class TestUpdate:
    """
    Tests for update() method of BaseRepository.
    """

    @pytest.fixture(autouse=True)
    def repo(self) -> BaseRepository[DummyModel]:
        return BaseRepository(DummyModel)

    def test_update_with_dict(self, repo):
        """
        Updating an existing model via dict should change its attributes.
        """
        inst = repo.create({"name": "original"})
        updated = repo.update(inst, {"name": "changed"})

        assert updated.id == inst.id
        assert updated.name == "changed"

    def test_update_with_pydantic_model(self, repo):
        """
        Updating via a Pydantic model should also work and handle datetime tzinfo.
        """
        inst = repo.create({"name": "tz_test"})
        new_time = datetime(2020, 1, 1, 12, tzinfo=timezone.utc)
        schema = DummySchema(name="tz_test", timestamp=new_time)
        updated = repo.update(inst, schema)

        assert updated.timestamp.tzinfo is None
        assert updated.timestamp == new_time.replace(tzinfo=None)

    def test_update_no_changes_returns_same(self, repo):
        """
        Calling update with empty attributes should leave the instance unchanged.
        """
        inst = repo.create({"name": "unchanged"})
        before = inst.name
        updated = repo.update(inst, {})
        assert updated.name == before

    def test_update_failure_rollback(self, repo, session):
        """
        If commit fails (e.g. due to constraint), the session should be rolled back.
        """
        inst = repo.create({"name": "dup"})

        with pytest.raises(SQLAlchemyError):
            repo.update(inst, {"name": None})

        new_inst = repo.create({"name": "after_rollback"})
        assert new_inst.id is not None


class TestQueryHelpers:
    """
    Tests for _one_or_none, _all, and _count methods.
    """

    @pytest.fixture(autouse=True)
    def repo(self) -> BaseRepository[DummyModel]:
        return BaseRepository(DummyModel)

    def test_one_or_none_returns_item(self, repo):
        """
        _one_or_none should return the matched instance when exactly one exists.
        """
        inst = repo.create({"name": "unique"})
        found = repo._one_or_none(repo._query().where(DummyModel.id == inst.id))
        assert found.id == inst.id

    def test_one_or_none_no_match(self, repo):
        """
        _one_or_none should return None if no rows match.
        """
        assert repo._one_or_none(repo._query().where(DummyModel.id < 0)) is None

    def test_all_returns_list(self, repo):
        """
        _all should return all persisted instances.
        """
        repo.create({"name": "a"})
        repo.create({"name": "b"})
        all_items = repo._all(repo._query())

        assert isinstance(all_items, list)
        assert len(all_items) >= 2

    def test_count_returns_correct(self, repo):
        """
        _count should return the correct number of matching rows.
        """
        repo.create({"name": "c"})
        repo.create({"name": "d"})
        cnt = repo._count(repo._query().where(DummyModel.name.in_(["c", "d"])))

        assert cnt == 2
