import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class EnrichedEvent(Base, TimestampMixin):
    __tablename__ = "enriched_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("economic_events.id", ondelete="CASCADE")
    )
    importance_score: Mapped[int]
    importance_reason: Mapped[str]
    plain_english_summary: Mapped[str]
    historical_context_summary: Mapped[str | None]
    news_context_summary: Mapped[str | None]
    affected_groups: Mapped[list[str]] = mapped_column(JSONB)
