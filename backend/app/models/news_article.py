import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class NewsArticle(Base, TimestampMixin):
    __tablename__ = "news_articles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("economic_events.id", ondelete="CASCADE")
    )
    headline: Mapped[str]
    source: Mapped[str]
    url: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    summary: Mapped[str | None]
    sentiment: Mapped[str | None]
    entities: Mapped[list[str]] = mapped_column(JSONB)
    topics: Mapped[list[str]] = mapped_column(JSONB)
