import uuid
from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class Briefing(Base, TimestampMixin):
    __tablename__ = "briefings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    briefing_date: Mapped[date] = mapped_column(Date, unique=True)
    title: Mapped[str]
    summary: Mapped[str]
    status: Mapped[str]
