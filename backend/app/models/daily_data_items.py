from __future__ import annotations

import uuid

from datetime import date, datetime

from typing import Any

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    String,
    UniqueConstraint,
    func
)

from sqlalchemy.dialects.postgresql import JSONB, UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class DailyDataItem(Base, TimestampMixin):
    __tablename__ = "daily_data_items"

    __table_args__ = (UniqueConstraint("item_key", "date", name="uq_daily_items_item_key_date"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid64,
    )

    item_key: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String, 
        nullable=False,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    raw_data: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )