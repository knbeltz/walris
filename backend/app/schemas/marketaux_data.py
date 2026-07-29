from datetime import datetime

from pydantic import BaseModel


class MarketauxArticle(BaseModel):
    item_key: str
    headline: str
    source: str
    url: str
    published_at: datetime
    summary: str
    sentiment: float | None
