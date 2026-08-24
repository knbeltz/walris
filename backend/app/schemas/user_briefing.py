from datetime import date, datetime

from pydantic import BaseModel


class BriefingSection(BaseModel):
    heading: str
    body: str


class BriefingContent(BaseModel):
    headline: str
    sections: list[BriefingSection]


class IndicatorPoint(BaseModel):
    date: date
    value: float


class IndicatorSeries(BaseModel):
    item_key: str
    label: str
    points: list[IndicatorPoint]


class NewsItem(BaseModel):
    headline: str
    source: str
    summary: str
    published_at: datetime
    url: str
    sentiment: float | None


class UserBriefingResponse(BaseModel):
    date: date
    content: BriefingContent
    indicators: list[IndicatorSeries]
    news: list[NewsItem]
