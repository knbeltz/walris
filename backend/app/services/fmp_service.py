import asyncio
import logging
from datetime import date
from typing import Any

import httpx
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.fmp_data import (
    CompanySpotlight,
    IndexQuote,
    SectorPerformance,
)

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10.0

FMP_BASE_URL = "https://financialmodelingprep.com"

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


async def fetch_market_snapshot(
    symbols: list[str],
) -> list[IndexQuote]:
    if not symbols:
        return []

    normalized_symbols: list[str] = []
    seen_symbols: set[str] = set()

    for symbol in symbols:
        normalized_symbol = symbol.strip().upper()

        if not normalized_symbol:
            continue

        if normalized_symbol in seen_symbols:
            continue

        seen_symbols.add(normalized_symbol)
        normalized_symbols.append(normalized_symbol)

    endpoint = f"{FMP_BASE_URL}/stable/quote"
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async with httpx.AsyncClient(
        timeout=REQUEST_TIMEOUT,
    ) as client:

        async def fetch_one_quote(
            symbol: str,
        ) -> IndexQuote | None:
            try:
                async with semaphore:
                    response = await client.get(
                        endpoint,
                        params={
                            "symbol": symbol,
                            "apikey": settings.fmp_api_key,
                        },
                    )

                response.raise_for_status()
                raw_response: Any = response.json()

            except httpx.HTTPError as error:
                _log_request_error(
                    f"Could not fetch quote for {symbol}",
                    error,
                    symbol=symbol,
                )
                raise

            if (
                not isinstance(raw_response, list)
                or not raw_response
            ):
                logger.warning(
                    "No quote was returned for symbol %s",
                    symbol,
                )
                return None

            raw_quote = raw_response[0]

            if not isinstance(raw_quote, dict):
                logger.warning(
                    "Quote for symbol %s was not an object",
                    symbol,
                )
                return None

            try:
                return IndexQuote(
                    symbol=raw_quote["symbol"],
                    name=raw_quote["name"],
                    price=raw_quote["price"],
                    change=raw_quote["change"],
                    change_percentage=raw_quote[
                        "changePercentage"
                    ],
                )

            except (
                KeyError,
                TypeError,
                ValueError,
                ValidationError,
            ) as error:
                logger.warning(
                    "Quote for symbol %s could not be normalized: %s",
                    symbol,
                    error,
                )
                return None

        tasks = [
            fetch_one_quote(symbol)
            for symbol in normalized_symbols
        ]

        results = await asyncio.gather(*tasks)

    return [
        result
        for result in results
        if result is not None
    ]


def fetch_sector_performance(
    as_of: date,
) -> list[SectorPerformance]:
    """
    Fetch and normalize sector performance data for a given date.

    Request failures are re-raised. Malformed sector records are logged
    and skipped.
    """
    endpoint = f"{FMP_BASE_URL}/stable/sector-performance-snapshot"

    try:
        response = httpx.get(
            endpoint,
            params={
                "date": as_of.isoformat(),
                "apikey": settings.fmp_api_key,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        raw_sectors: Any = response.json()

    except httpx.HTTPError as error:
        _log_request_error(
            f"Could not fetch sector performance for {as_of}",
            error,
            as_of=as_of.isoformat(),
        )
        raise

    if not isinstance(raw_sectors, list):
        logger.warning(
            "Sector performance response for %s was not a list",
            as_of,
        )
        return []

    sector_performances: list[SectorPerformance] = []

    for raw_sector in raw_sectors:
        if not isinstance(raw_sector, dict):
            logger.warning(
                "Sector record could not be normalized because it was not an object: %r",
                raw_sector,
            )
            continue

        try:
            sector_performance = SectorPerformance(
                sector=raw_sector["sector"],
                average_change=raw_sector["averageChange"],
                date=as_of,
            )
        except (KeyError, TypeError, ValueError, ValidationError) as error:
            logger.warning(
                "Sector record could not be normalized: %s. Data: %r",
                error,
                raw_sector,
            )
            continue

        sector_performances.append(sector_performance)

    return sector_performances


def pick_best_and_worst(
    sectors: list[SectorPerformance],
) -> tuple[SectorPerformance, SectorPerformance]:
    """
    Return the sectors with the highest and lowest average changes.

    The first tuple item is the best sector. The second is the worst.
    """
    if not sectors:
        raise ValueError("Cannot select the best and worst sectors from an empty list.")

    best_sector = max(
        sectors,
        key=lambda sector: sector.average_change,
    )
    worst_sector = min(
        sectors,
        key=lambda sector: sector.average_change,
    )

    return best_sector, worst_sector


async def fetch_top_gainer_spotlight(
    market_cap_threshold: float,
) -> CompanySpotlight | None:
    """

    Return the qualifying company with the highest percentage gain.

    Return None when no gainer meets the market-cap threshold.

    """

    if market_cap_threshold < 0:
        raise ValueError("market_cap_threshold cannot be negative.")

    gainers_endpoint = f"{FMP_BASE_URL}/stable/biggest-gainers"

    profile_endpoint = f"{FMP_BASE_URL}/stable/profile"

    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        try:
            response = await client.get(
                gainers_endpoint,
                params={
                    "apikey": settings.fmp_api_key,
                },
            )

            response.raise_for_status()

            raw_gainers: Any = response.json()

        except httpx.HTTPError as error:
            _log_request_error(
                "Could not fetch biggest gainers",
                error,
            )

            raise

        if not isinstance(raw_gainers, list):
            logger.warning("Biggest-gainers response was not a list")

            return None

        async def process_gainer(
            raw_gainer: Any,
        ) -> CompanySpotlight | None:
            """

            Process one raw gainer record.

            Return a CompanySpotlight when the company qualifies,

            otherwise return None.

            """

            if not isinstance(raw_gainer, dict):
                logger.warning(
                    "Gainer record was not an object: %r",
                    raw_gainer,
                )

                return None

            try:
                symbol = str(raw_gainer["symbol"]).strip().upper()

                if not symbol:
                    raise ValueError("Gainer symbol is empty.")

            except (KeyError, TypeError, ValueError) as error:
                logger.warning(
                    "Gainer symbol could not be read: %s. Data: %r",
                    error,
                    raw_gainer,
                )

                return None

            try:
                async with semaphore:
                    profile_response = await client.get(
                        profile_endpoint,
                        params={
                            "symbol": symbol,
                            "apikey": settings.fmp_api_key,
                        },
                    )

                profile_response.raise_for_status()

                raw_profiles: Any = profile_response.json()

            except httpx.HTTPError as error:
                _log_request_error(
                    f"Could not fetch profile data for {symbol}",
                    error,
                    symbol=symbol,
                )

                return None

            if not isinstance(raw_profiles, list) or not raw_profiles:
                logger.warning(
                    "No profile was returned for symbol %s",
                    symbol,
                )

                return None

            raw_profile = raw_profiles[0]

            if not isinstance(raw_profile, dict):
                logger.warning(
                    "Profile for symbol %s was not an object",
                    symbol,
                )

                return None

            try:
                market_cap = float(raw_profile["marketCap"])

                if market_cap < market_cap_threshold:
                    return None

                return CompanySpotlight(
                    symbol=symbol,
                    name=raw_gainer["name"],
                    price=raw_gainer["price"],
                    change=raw_gainer["change"],
                    change_percentage=raw_gainer["changesPercentage"],
                    market_cap=market_cap,
                    direction="gainer",
                )

            except (
                KeyError,
                TypeError,
                ValueError,
                ValidationError,
            ) as error:
                logger.warning(
                    "Gainer %s could not be normalized: %s",
                    symbol,
                    error,
                )

                return None

        tasks = [process_gainer(raw_gainer) for raw_gainer in raw_gainers]

        results = await asyncio.gather(*tasks)

    qualifying_gainers = [result for result in results if result is not None]

    if not qualifying_gainers:
        return None

    return max(
        qualifying_gainers,
        key=lambda company: company.change_percentage,
    )


async def fetch_top_loser_spotlight(
    market_cap_threshold: float,
) -> CompanySpotlight | None:
    """
    Return the qualifying company with the largest percentage loss.

    Return None when no loser meets the market-cap threshold.
    """
    if market_cap_threshold < 0:
        raise ValueError("market_cap_threshold cannot be negative.")

    losers_endpoint = f"{FMP_BASE_URL}/stable/biggest-losers"
    profile_endpoint = f"{FMP_BASE_URL}/stable/profile"

    async with httpx.AsyncClient(
        timeout=REQUEST_TIMEOUT,
    ) as client:
        try:
            response = await client.get(
                losers_endpoint,
                params={
                    "apikey": settings.fmp_api_key,
                },
            )
            response.raise_for_status()
            raw_losers: Any = response.json()

        except httpx.HTTPError as error:
            _log_request_error(
                "Could not fetch biggest losers",
                error,
            )
            raise

        if not isinstance(raw_losers, list):
            logger.warning(
                "Biggest-losers response was not a list"
            )
            return None

        async def process_loser(
            raw_loser: Any,
        ) -> CompanySpotlight | None:
            if not isinstance(raw_loser, dict):
                logger.warning(
                    "Loser record was not an object: %r",
                    raw_loser,
                )
                return None

            try:
                symbol = str(
                    raw_loser["symbol"]
                ).strip().upper()

                if not symbol:
                    raise ValueError("Loser symbol is empty.")

            except (KeyError, TypeError, ValueError) as error:
                logger.warning(
                    "Loser symbol could not be read: %s. Data: %r",
                    error,
                    raw_loser,
                )
                return None

            try:
                profile_response = await client.get(
                    profile_endpoint,
                    params={
                        "symbol": symbol,
                        "apikey": settings.fmp_api_key,
                    },
                )
                profile_response.raise_for_status()
                raw_profiles: Any = profile_response.json()

            except httpx.HTTPError as error:
                _log_request_error(
                    f"Could not fetch profile data for {symbol}",
                    error,
                    symbol=symbol,
                )
                return None

            if (
                not isinstance(raw_profiles, list)
                or not raw_profiles
            ):
                logger.warning(
                    "No profile was returned for symbol %s",
                    symbol,
                )
                return None

            raw_profile = raw_profiles[0]

            if not isinstance(raw_profile, dict):
                logger.warning(
                    "Profile for symbol %s was not an object",
                    symbol,
                )
                return None

            try:
                market_cap = float(raw_profile["marketCap"])

                if market_cap < market_cap_threshold:
                    return None

                return CompanySpotlight(
                    symbol=symbol,
                    name=raw_loser["name"],
                    price=raw_loser["price"],
                    change=raw_loser["change"],
                    change_percentage=raw_loser[
                        "changesPercentage"
                    ],
                    market_cap=market_cap,
                    direction="loser",
                )

            except (
                KeyError,
                TypeError,
                ValueError,
                ValidationError,
            ) as error:
                logger.warning(
                    "Loser %s could not be normalized: %s",
                    symbol,
                    error,
                )
                return None

        tasks = [
            process_loser(raw_loser)
            for raw_loser in raw_losers
        ]

        results = await asyncio.gather(*tasks)

    qualifying_losers = [
        result
        for result in results
        if result is not None
    ]

    if not qualifying_losers:
        return None

    return min(
        qualifying_losers,
        key=lambda company: company.change_percentage,
    )
