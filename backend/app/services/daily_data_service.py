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

from app.schemas.daily_data import (
    DailyDataItemCandidate,
    FmpFetchResults,
    CoveredDailyDataCandidate,
)


async def fetch_and_shape_fmp_candidates(
    symbols: list[str],
    as_of: date,
    market_cap_threshold: float,
) -> FmpFetchResults:
    """
    Fetch FMP data and shape it into DailyDataItem candidates.

    Includes:
    - One candidate for each successfully fetched market index
    - The best-performing sector
    - The worst-performing sector
    - The top qualifying gainer, when one exists
    - The top qualifying loser, when one exists
    """

    index_quotes = await fetch_market_snapshot(symbols)

    sector_performances = fetch_sector_performance(as_of)
    best_sector, worst_sector = pick_best_and_worst(sector_performances)

    top_gainer, top_loser = await asyncio.gather(
        fetch_top_gainer_spotlight(market_cap_threshold),
        fetch_top_loser_spotlight(market_cap_threshold),
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

    return FmpFetchResults(
        index_quotes=index_quotes,
        sector_performances=sector_performances,
        gainer=top_gainer,
        loser=top_loser,
        candidates=candidates,
    )


async def fetch_and_shape_fred_candidates() -> list[DailyDataItemCandidate]:
    """
    Fetch the latest FRED observations and shape them into
    DailyDataItemCandidate objects.
    """

    fred_observations: list[FredObservation] = await fetch_fred_observations()

    return [
        DailyDataItemCandidate(
            item_key=observation.series_id,
            source="fred",
            value=observation.value,
            raw_data=observation.model_dump(mode="json"),
        )
        for observation in fred_observations
    ]


async def fetch_and_shape_marketaux_candidates(
    index_quotes: list[IndexQuote],
    sector_performance: list[SectorPerformance],
    gainer: CompanySpotlight | None,
    loser: CompanySpotlight | None,
) -> list[MarketauxArticle]:
    """
    Fetch recent Marketaux news coverage for the day's FRED and FMP items.

    Includes all configured FRED indicators, the supplied index quotes and
    sector performance records, and the top gainer and loser when available.

    Returns a flattened list of MarketauxArticle objects. Each article carries
    the item_key of the FRED or FMP item whose search produced it.
    """

    return await fetch_all_articles(
        index_quotes=index_quotes,
        sector_performance=sector_performance,
        gainer=gainer,
        loser=loser,
    )


def filter_candidates_by_news_coverage(
    fmp_candidates: list[DailyDataItemCandidate],
    fred_candidates: list[DailyDataItemCandidate],
    marketaux_articles: list[MarketauxArticle],
) -> list[CoveredDailyDataCandidate]:
    """
    Combine FMP and FRED candidates, remove candidates without news coverage,
    and pair each surviving candidate with its matching Marketaux articles.

    A candidate survives when at least one Marketaux article has the same
    item_key.
    """
    all_candidates = [*fmp_candidates, *fred_candidates]

    articles_by_item_key: dict[str, list[MarketauxArticle]] = {}

    for article in marketaux_articles:
        articles_by_item_key.setdefault(
            article.item_key,
            [],
        ).append(article)

    return [
        CoveredDailyDataCandidate(
            candidate=candidate,
            articles=articles_by_item_key[candidate.item_key],
        )
        for candidate in all_candidates
        if candidate.item_key in articles_by_item_key
    ]


async def fetch_covered_daily_data_candidates(
    symbols: list[str],
    as_of: date,
    market_cap_threshold: float,
) -> list[CoveredDailyDataCandidate]:
    """
    Fetch and shape FMP and FRED candidates, retrieve their Marketaux coverage,
    and return only candidates with at least one matching article.
    """
    fmp_results, fred_candidates = await asyncio.gather(
        fetch_and_shape_fmp_candidates(
            symbols=symbols,
            as_of=as_of,
            market_cap_threshold=market_cap_threshold,
        ),
        fetch_and_shape_fred_candidates(),
    )

    marketaux_articles = await fetch_and_shape_marketaux_candidates(
        index_quotes=fmp_results.index_quotes,
        sector_performance=fmp_results.sector_performances,
        gainer=fmp_results.gainer,
        loser=fmp_results.loser,
    )

    return filter_candidates_by_news_coverage(
        fmp_candidates=fmp_results.candidates,
        fred_candidates=fred_candidates,
        marketaux_articles=marketaux_articles,
    )
