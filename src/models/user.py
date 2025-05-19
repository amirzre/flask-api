from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.extensions import db
from src.mixins import IDMixin, TimestampMixin


class User(db.Model, IDMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(
        String(11), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
