from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.device_token import DeviceToken
from app.models.user import User
from app.schemas.device_token import DeviceTokenRegistration

router = APIRouter()


@router.post("/notifications/register")
def register_device_token(
    body: DeviceTokenRegistration,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    device_token = db.scalar(
        select(DeviceToken).where(DeviceToken.expo_push_token == body.expo_push_token)
    )

    if device_token is None:
        device_token = DeviceToken(
            expo_push_token=body.expo_push_token,
            device_id=body.device_id,
            platform=body.platform,
            timezone=body.timezone,
        )
        db.add(device_token)
    else:
        device_token.device_id = body.device_id
        device_token.platform = body.platform
        device_token.timezone = body.timezone

    device_token.user_id = user.id

    db.commit()
