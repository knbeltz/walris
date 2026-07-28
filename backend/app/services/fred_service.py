import asyncio
import logging
from typing import Any

import httpx

from app.schemas.fred_data import FredObservation

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10.0

FRED_BASE_URL = "https://api.stlouisfed.org/fred"

MAX_CONCURRENCY = 10

FRED_INDICATORS: list[tuple[str, str]] = [
    ("CPIAUCSL", "Consumer Price Index"),
    ("CPILFESL", "Core CPI"),
    ("PCEPI", "PCE Price Index"),
    ("PCEPILFE", "Core PCE Price Index"),
    ("PPIACO", "Producer Price Index"),
    ("CUSR0000SEHA", "Rent/Shelter Inflation"),
    ("CPIUFDSL", "Food Inflation"),
    ("CPIENGSL", "Energy CPI"),
    ("PAYEMS", "Nonfarm Payrolls"),
    ("UNRATE", "Unemployment Rate"),
    ("ICSA", "Initial Jobless Claims"),
    ("CCSA", "Continuing Jobless Claims"),
    ("CIVPART", "Labor Force Participation Rate"),
    ("CES0500000003", "Average Hourly Earnings"),
    ("JTSJOL", "JOLTS Job Openings"),
    ("GDP", "Gross Domestic Product"),
    ("RSAFS", "Retail Sales"),
    ("INDPRO", "Industrial Production"),
    ("TCU", "Capacity Utilization"),
    ("UMCSENT", "U Mich Consumer Sentiment"),
    ("DSPI", "Disposable Personal Income"),
    ("FEDFUNDS", "Federal Funds Rate"),
    ("MPRIME", "Prime Rate"),
    ("DGS2", "2-Year Treasury Yield"),
    ("DGS10", "10-Year Treasury Yield"),
    ("DGS30", "30-Year Treasury Yield"),
    ("T10Y2Y", "Yield Curve (10Y-2Y)"),
    ("M2SL", "M2 Money Supply"),
    ("TERMCBCCALLNS", "Credit Card Interest Rate"),
    ("HOUST", "Housing Starts"),
    ("PERMIT", "Building Permits"),
    ("EXHOSLUSM495S", "Existing Home Sales"),
    ("HSN1F", "New Home Sales"),
    ("MORTGAGE30US", "30-Year Fixed Mortgage Rate"),
    ("MORTGAGE15US", "15-Year Fixed Mortgage Rate"),
    ("CSUSHPISA", "Case-Shiller Home Price Index"),
    ("USSTHPI", "FHFA House Price Index"),
    ("POPTHM", "Population"),
    ("GASREGW", "Regular Gas Prices"),
]

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

async def fetch_fred_observation(
    client: httpx.AsyncClient,
    api_key: str,
    series_id: str,
    name: str,
) -> FredObservation:
    response = await client.get(
            f"{FRED_BASE_URL}/series/observations",
            params={
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 1,
            },
        )

    response.raise_for_status()

    data: dict[str, Any] = response.json()
    observations = data.get("observations", [])

    if not observations:
        raise ValueError(
            f"FRED returned no observations for series {series_id}"
        )

    latest = observations[0]

    # FRED uses "." when a value is missing.
    raw_value = latest["value"]
    value = None if raw_value == "." else float(raw_value)

    return FredObservation(
        series_id=series_id,
        name=name,
        value=value,
        date=latest["date"],
    )

async def fetch_all(
        api_key: str,
) -> list[FredObservation]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:

        async def fetch_one(
            series_id: str,
            name: str,
        ) -> FredObservation | None:
            async with semaphore:
                try:
                    return await fetch_fred_observation(
                        client=client,
                        api_key=api_key,
                        series_id=series_id,
                        name=name,
                    )
                except httpx.HTTPError as error:
                    _log_request_error(
                        "Failed to fetch FRED observation",
                        error,
                        series_id=series_id,
                        name=name,
                    )
                    return None

                except ValueError:
                    logger.exception(
                        "FRED returned invalid or missing observation data",
                        extra={
                            "series_id": series_id,
                            "name": name,
                        }
                    )
                    return None

        tasks = [
            fetch_one(series_id, name)
            for series_id, name in FRED_INDICATORS
        ]

        results = await asyncio.gather(*tasks)

        return [
            result
            for result in results
            if result is not None
        ]






