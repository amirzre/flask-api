from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    This class serves as the foundation for defining database models using SQLAlchemy's
    declarative system. All database models should inherit from this base class.
    """


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
