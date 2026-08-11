from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.user_briefings import UserBriefing
from app.schemas.user_briefing import BriefingContent, UserBriefingResponse

router = APIRouter()


@router.get("/users/me/briefing", response_model=UserBriefingResponse)
def get_todays_briefing(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserBriefingResponse:
    today = date.today()

    briefing = db.scalar(
        select(UserBriefing).where(
            UserBriefing.user_id == user.id,
            UserBriefing.date == today,
        )
    )

    if briefing is not None:
        return UserBriefingResponse(
            date=briefing.date,
            content=BriefingContent(**briefing.content),
        )

    return UserBriefingResponse(
        date=today,
        content=BriefingContent(
            headline="No briefing available yet for today.",
            sections=[],
        ),
    )
