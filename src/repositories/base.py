from datetime import datetime
from typing import Any, Generic, Sequence, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import ScalarResult, Select, Subquery, func, select
from sqlalchemy.exc import SQLAlchemyError

from src.extensions import db

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Base repository implementing common CRUD operations for all models.
    """

    def __init__(self, model_class: Type[ModelType]):
        """
        Initialize the repository with a specific model class.

        Args:
            model_class: The SQLAlchemy model class this repository will work with.
        """
        self.model_class = model_class

    def create(self, attributes: dict[str, Any] | BaseModel) -> ModelType:
        """
        Create a new model instance.

        Args:
            attributes: Dictionary or Pydantic model containing the attributes.

        Returns:
            The created model instance.

        Raises:
            SQLAlchemyError: If there's an error during creation
        """
        data = (
            attributes.model_dump(exclude_unset=True)
            if isinstance(attributes, BaseModel)
            else attributes
        )

        for key, value in data.items():
            if isinstance(value, datetime) and value.tzinfo is not None:
                data[key] = value.replace(tzinfo=None)

        try:
            model = self.model_class(**data)
            db.session.add(model)
            db.session.commit()
            db.session.refresh(model)
            return model
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise ex

    def update(
        self, model: ModelType, attributes: dict[str, Any] | BaseModel
    ) -> ModelType:
        """
        Update an existing model instance.

        Args:
            model: The model instance to update.
            attributes: Dictionary or Pydantic model containing updated fields.

        Returns:
            The updated model instance.

        Raises:
            SQLAlchemyError: If there's an error during update.
        """
        if attributes:
            data = (
                attributes.model_dump(exclude_unset=True)
                if isinstance(attributes, BaseModel)
                else attributes
            )

            for key, value in data.items():
                if isinstance(value, datetime):
                    if value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                    data[key] = value
                setattr(model, key, value)

        try:
            db.session.commit()
            return model
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise ex

    def delete(self, model: ModelType) -> None:
        """
        Permanently delete a model instance.

        Args:
            model: The model instance to delete.

        Raises:
            SQLAlchemyError: If there's an error during deletion.
        """
        try:
            db.session.delete(model)
            db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise ex

    def _query(self) -> Select:
        """
        Construct a base SELECT query for the model.

        Args:
            order_: Optional dictionary specifying order clauses.

        Returns:
            A SQLAlchemy Select object.
        """
        query = select(self.model_class)

        return query

    def _one_or_none(self, query: Select) -> ModelType | None:
        """
        Execute a query and return exactly one or no result.

        Args:
            query: The SELECT query to execute.

        Returns:
            The matched model instance or None.
        """
        result: ScalarResult[ModelType] = db.session.scalars(query)
        return result.one_or_none()

    def _all(self, query: Select) -> Sequence[ModelType]:
        """
        Execute a query and return all results.

        Args:
            query: The SELECT query to execute.

        Returns:
            A list of model instances.
        """
        result: ScalarResult[ModelType] = db.session.scalars(query)
        return result.all()

    def _count(self, query: Select) -> int:
        """
        Count the number of results returned by a query.

        Args:
            query: The SELECT query to execute.

        Returns:
            The count of matching records.
        """
        subquery: Subquery = query.subquery()
        count_query = select(func.count()).select_from(subquery)
        result: ScalarResult[int] = db.session.scalars(count_query)
        return result.one()
