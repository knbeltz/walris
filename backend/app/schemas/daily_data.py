from datetime import date
from typing import Any

from app.schemas.fmp_data import (
    IndexQuote, 
    SectorPerformance,
    CompanySpotlight,
) 
from pydantic import BaseModel

class DailyDataItemCandidate(BaseModel):
    item_key: str
    source: str
    value: float
    raw_data: dict[str, Any]

class FmpFetchResults(BaseModel):
    candidates: list[DailyDataItemCandidate]
    index_quotes: list[IndexQuote]
    sector_performances: list[SectorPerformance]
    gainer: CompanySpotlight | None
    loser: CompanySpotlight | None

