from datetime import date
from typing import Literal

from pydantic import BaseModel


class IndexQuote(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_percentage: float


class SectorPerformance(BaseModel):
    sector: str
    average_change: float
    date: date


class CompanySpotlight(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_percentage: float
    market_cap: float
    direction: Literal["gainer", "loser"]
