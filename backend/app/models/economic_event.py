import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class EconomicEvent(Base, TimestampMixin):
    __tablename__ = "economic_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    briefing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("briefings.id", ondelete="CASCADE"))
    external_event_id: Mapped[str]
    event_name: Mapped[str]
    country: Mapped[str]
    release_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    actual_value: Mapped[float | None]
    forecast_value: Mapped[float | None]
    previous_value: Mapped[float | None]
    unit: Mapped[str | None]
    source: Mapped[str]
