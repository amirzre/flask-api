from datetime import datetime

import jdatetime
import pytz
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


def utc_to_jalali() -> str:
    """
    Convert an aware UTC datetime to a Jalali (solar) date‐time string
    in the Asia/Tehran timezone, style.
    """
    tehran = pytz.timezone("Asia/Tehran")
    now_tehran = datetime.now(tehran)

    j_dt = jdatetime.datetime.fromgregorian(
        year=now_tehran.year,
        month=now_tehran.month,
        day=now_tehran.day,
        hour=now_tehran.hour,
        minute=now_tehran.minute,
        second=now_tehran.second,
    )
    return j_dt.strftime("%Y-%m-%d %H:%M:%S")


class IDMixin:
    """Mixin to add an auto-incrementing `id` field to a model."""

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )


class TimestampMixin:
    """Mixin to add timestamp fields for created times to a model."""

    created: Mapped[str] = mapped_column(
        String(20),
        default=utc_to_jalali,
        nullable=False,
    )
