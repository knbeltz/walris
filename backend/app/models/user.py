import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    clerk_user_id: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str | None]
    phone_number: Mapped[str | None]
    name: Mapped[str | None]
