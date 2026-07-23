import uuid

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    clerk_user_id: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str | None]
    name: Mapped[str | None]
    category: Mapped[str | None]
    additional_topics: Mapped[list[str]] = mapped_column(JSONB, default=list)

