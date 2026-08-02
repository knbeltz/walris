import asyncio
import logging
from datetime import UTC, datetime, timedelta
from typing import Any

import httpx

from app.core.config import settings
from app.schemas.fmp_data import CompanySpotlight, IndexQuote, SectorPerformance
from app.schemas.marketaux_data import MarketauxArticle
from app.services.fred_service import FRED_INDICATORS

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10.0

MARKETAUX_BASE_URL = "https://api.marketaux.com/v1"

MAX_CONCURRENCY = 10


def _log_request_error(
    message: str,
    error: httpx.HTTPError,
    **context: Any,
) -> None:
    """
    Log an HTTPX request error, including the response when available.
    """
    if isinstance(error, httpx.HTTPStatusError):
        logger.exception(
            "%s. Status code: %s. Response body: %s",
            message,
            error.response.status_code,
            error.response.text,
            extra=context,
        )
        return

    logger.exception(
        "%s: %s",
        message,
        error,
        extra=context,
    )


async def fetch_marketaux_articles(
    client: httpx.AsyncClient, itemkey: str, search_term: str
) -> list[MarketauxArticle]:
    """Fetch up to three recent Marketaux articles for a search term."""

    """Raises:
        httpx.HTTPError: If the Marketaux request fails or returns a bad status."""

    published_after = datetime.now(UTC) - timedelta(days=1)

    response = await client.get(
        f"{MARKETAUX_BASE_URL}/news/all",
        params={
            "search": search_term,
            "published_after": published_after.strftime("%Y-%m-%dT%H:%M:%S"),
            "sort": "published_desc",
            "api_token": settings.marketaux_api_key,
        },
    )
    response.raise_for_status()

    response_data = response.json()
    raw_articles = response_data.get("data", [])

    articles: list[MarketauxArticle] = []

    for raw_article in raw_articles[:3]:
        entities = raw_article.get("entities") or []

        sentiment = next(
            (
                entity.get("sentiment_score")
                for entity in entities
                if entity.get("sentiment_score") is not None
            ),
            None,
        )

        articles.append(
            MarketauxArticle(
                item_key=itemkey,
                headline=raw_article.get("title"),
                summary=raw_article.get("description"),
                url=raw_article.get("url"),
                source=raw_article.get("source"),
                published_at=raw_article.get("published_at"),
                sentiment=sentiment,
            )
        )

    return articles


def build_news_search_items(
    index_quotes: list[IndexQuote],
    sector_performance: list[SectorPerformance],
    gainer: CompanySpotlight | None,
    loser: CompanySpotlight | None,
) -> list[tuple[str, str]]:
    """Combine FRED and FMP results into Marketaux search items."""
    search_items = list(FRED_INDICATORS)

    search_items.extend((quote.symbol, quote.name) for quote in index_quotes)

    search_items.extend((sector.sector, sector.sector) for sector in sector_performance)

    if gainer is not None:
        search_items.append((gainer.symbol, gainer.name))

    if loser is not None:
        search_items.append((loser.symbol, loser.name))

    return search_items


async def fetch_all_articles(
    index_quotes: list[IndexQuote],
    sector_performance: list[SectorPerformance],
    gainer: CompanySpotlight | None,
    loser: CompanySpotlight | None,
) -> list[MarketauxArticle]:
    """Fetch recent Marketaux articles for all FRED and FMP search items."""

    search_items = build_news_search_items(
        index_quotes=index_quotes,
        sector_performance=sector_performance,
        gainer=gainer,
        loser=loser,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:

        async def fetch_one(
            itemkey: str,
            search_term: str,
        ) -> list[MarketauxArticle] | None:
            async with semaphore:
                try:
                    return await fetch_marketaux_articles(
                        client=client,
                        itemkey=itemkey,
                        search_term=search_term,
                    )
                except httpx.HTTPError as error:
                    _log_request_error(
                        "Failed to fetch Marketaux articles",
                        error,
                        itemkey=itemkey,
                        search_term=search_term,
                    )
                    return None

                except ValueError:
                    logger.exception(
                        "Marketaux returned invalid or missing articles",
                        extra={
                            "itemkey": itemkey,
                            "search_term": search_term,
                        },
                    )
                    return None

        tasks = [fetch_one(itemkey, search_term) for itemkey, search_term in search_items]

        results = await asyncio.gather(*tasks)

        return [article for result in results if result is not None for article in result]
