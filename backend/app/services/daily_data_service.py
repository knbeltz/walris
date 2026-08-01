import logging 
import asyncio

from datetime import datetime, date

from app.services.fmp_service import (
    fetch_market_snapshot,
    fetch_sector_performance,
    fetch_top_gainer_spotlight,
    fetch_top_loser_spotlight,
    pick_best_and_worst,
)
from app.services.fred_service import fetch_all as fetch_fred_observations
from app.services.marketaux_service import fetch_all_articles

from app.schemas.fmp_data import CompanySpotlight, IndexQuote, SectorPerformance
from app.schemas.fred_data import FredObservation
from app.schemas.marketaux_data import MarketauxArticle

from app.core.database import SessionLocal

from app.models.daily_data_items import DailyDataItem
from app.models.daily_data_news import DailyDataNews

from app.schemas.daily_data import DailyDataItemCandidate


async def fetch_and_shape_fmp_candidates(
    symbols: list[str],
    as_of: date, 
    market_cap_threshold: float,
) -> list[DailyDataItemCandidate]:
    """
    Fetch FMP data and shape it into DailyDataItem candidates. 

    Includes: 
    - One candidate for each successfully fetched market index 
    - The best-performing sector 
    - The worst-performing sector 
    - The top qualifying gainer, when one exists 
    - The top qualifying loser, when one existis 
    """

    index_quotes = await fetch_market_snapshot(symbols)

    sector_performances = fetch_sector_performance(as_of)
    best_sector, worst_sector = pick_best_and_worst(
        sector_performances
    )

    top_gainer, top_loser = await asyncio.gather(
        fetch_top_gainer_spotlight(
            market_cap_threshold
        ),
        fetch_top_loser_spotlight(
            market_cap_threshold
        ),
    )

    candidates: list[DailyDataItemCandidate] = []

    candidates.extend(
        DailyDataItemCandidate(
            item_key=quote.symbol,
            source="fmp",
            value=quote.price,
            raw_data=quote.model_dump(mode="json"),
        )
        for quote in index_quotes
    )

    candidates.extend(
        [
            DailyDataItemCandidate(
                item_key=f"sector: {best_sector.sector}",
                source="fmp",
                value=best_sector.average_change,
                raw_data=best_sector.model_dump(mode="json"),
            ),

            DailyDataItemCandidate(
                item_key=f"sector: {worst_sector.sector}",
                source="fmp",
                value=worst_sector.average_change,
                raw_data=worst_sector.model_dump(mode="json"),
            ),
        ]
    )

    if top_gainer is not None: 
        candidates.append(
            DailyDataItemCandidate(
                item_key=f"company: {top_gainer.symbol}",
                source="fmp",
                value=top_gainer.change_percentage,
                raw_data=top_gainer.model_dump(mode="json"),
            )
        )

    if top_loser is not None:
        candidates.append(
            DailyDataItemCandidate(
                item_key=f"company: {top_loser.symbol}",
                source="fmp",
                value=top_loser.change_percentage,
                raw_data=top_loser.model_dump(mode="json"),
            )
        )

    return candidates 
