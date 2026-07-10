import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class DeviceToken(Base, TimestampMixin):
    __tablename__ = "device_tokens"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    expo_push_token: Mapped[str] = mapped_column(unique=True)
    device_id: Mapped[str]
    platform: Mapped[str]
    timezone: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
