import logging
from datetime import date

from dataclasses import dataclass, field

from openai import AsyncOpenAI
from sqlalchemy import select

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.daily_data_items import DailyDataItem
from app.models.daily_data_news import DailyDataNews
from app.models.user import User
from app.services.category_config import CATEGORY_ITEM_KEYS, TOPIC_ITEM_KEYS
from app.services.daily_data_service import (
    MARKET_INDEX_SYMBOLS, 
    SP_500_SYMBOL,
    NASDAQ_COMPOSITE_SYMBOL
)

@dataclass(frozen=True, slots=True)
class MarketContentRules: 
    wants_all_sectors: bool = False
    wants_best_worst_sector: bool = False
    named_sectors: frozenset[str] = field(
        default_factory=frozenset
    )
    wants_company_spotlight: bool = False
    index_symbols: frozenset[str] = field(
        default_factory=frozenset, 
    )

CATEGORY_MARKET_CONTENT: dict[str, MarketContentRules] = {
    "investor": MarketContentRules(
        wants_all_sectors=True,
        wants_company_spotlight=True,
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS),
    ), 
    "small_business_owner": MarketContentRules(
        wants_best_worst_sector=True,
        index_symbols=frozenset({
            SP_500_SYMBOL, 
        }),
    ),
    "consumer": MarketContentRules(),
    "home": MarketContentRules(
        named_sectors=frozenset({
            "Real Estate",
            "Financial Services",
            "Consumer Cyclical",
        }),
        index_symbols=frozenset({
            SP_500_SYMBOL,
        }),
    ),
    "student": MarketContentRules(
        wants_best_worst_sector=True,
        index_symbols=frozenset({
            SP_500_SYMBOL,
            NASDAQ_COMPOSITE_SYMBOL,
        }),
    ),
    "job_seeker": MarketContentRules(
        wants_best_worst_sector=True,
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS),
    ),
    "everything": MarketContentRules(
        wants_all_sectors=True,
        wants_company_spotlight=True,
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS)
    ),
}

TOPIC_MARKET_CONTENT: dict[str, MarketContentRules] = {
    "industry_sector_performance": MarketContentRules(
        wants_all_sectors=True,
    ),
    "company_spotlights": MarketContentRules(
        wants_company_spotlight=True,
    ),
    "major_market_indicies": MarketContentRules(
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS),
    ),
}
