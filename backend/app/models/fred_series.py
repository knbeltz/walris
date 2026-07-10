import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class FredSeries(Base, TimestampMixin):
    __tablename__ = "fred_series"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("economic_events.id", ondelete="CASCADE")
    )
    series_id: Mapped[str]
    series_name: Mapped[str]
    latest_value: Mapped[float]
    previous_value: Mapped[float | None]
    ten_year_average: Mapped[float | None]
    historical_percentile: Mapped[float | None]
    trend_direction: Mapped[str | None]
    data_points: Mapped[list[dict[str, float]]] = mapped_column(JSONB)
