from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db
from src.mixins import IDMixin, TimestampMixin


class Log(db.Model, IDMixin, TimestampMixin):
    __tablename__ = "logs"

    method: Mapped[str] = mapped_column(String(10), nullable=True)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(10), nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True, index=True
    )

    user = relationship("User", back_populates="logs")
