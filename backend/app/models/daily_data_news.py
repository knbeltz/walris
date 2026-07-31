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

class DailyDataNews(Base, TimestampMixin):
    __tablename__ = "daily_data_news"

    __table_args__ = (UniqueConstraint("item_key", "date", name="uq_daily_items_item_key_date"),)
