from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.daily_data_items import DailyDataItem
from app.models.user import User
from app.models.user_briefings import UserBriefing
from app.schemas.user_briefing import (
    BriefingContent,
    IndicatorPoint,
    IndicatorSeries,
    NewsItem,
    UserBriefingResponse,
)
from app.services.fred_service import FRED_INDICATORS
from app.services.openai_service import get_relevant_fred_item_keys, get_user_daily_data_with_news

router = APIRouter()


@router.get("/users/me/briefing", response_model=UserBriefingResponse)
def get_todays_briefing(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserBriefingResponse:
    today = date.today()

    items_with_news = get_user_daily_data_with_news(user, today)
    all_news = [n for item_with_news in items_with_news for n in item_with_news.news]

    deduped = {n.url: n for n in all_news}.values()

    sorted_news = sorted(deduped, key=lambda n: n.published_at, reverse=True)

    news = [
        NewsItem(
            headline=n.headline,
            source=n.source,
            summary=n.summary,
            published_at=n.published_at,
            url=n.url,
            sentiment=n.sentiment,
        )
        for n in sorted_news[:5]
    ]




    relevant_keys = get_relevant_fred_item_keys(user)

    items = db.scalars(
        select(DailyDataItem).where(
            DailyDataItem.item_key.in_(relevant_keys)
        ).order_by(
            DailyDataItem.item_key, DailyDataItem.date
        )
    ).all()

    labels = dict(FRED_INDICATORS)

    points_by_key: dict[str, list[IndicatorPoint]] = {}

    for item in items:
        if item.value is None:
            continue

        points_by_key.setdefault(item.item_key, []).append(
            IndicatorPoint(date=item.date, value=item.value)
        )

    indicators = [
        IndicatorSeries(item_key=key, label=labels.get(key, key), points=points)
        for key, points in points_by_key.items()
    ]

    briefing = db.scalar(
        select(UserBriefing).where(
            UserBriefing.user_id == user.id,
            UserBriefing.date == today,
        )
    )

    if briefing is not None:
        return UserBriefingResponse(
            date=briefing.date,
            indicators=indicators,
            content=BriefingContent(**briefing.content),
            news=news
        )

    return UserBriefingResponse(
        date=today,
        indicators=indicators,
        content=BriefingContent(
            headline="No briefing available yet for today.",
            sections=[],
        ),
        news=news,
    )


