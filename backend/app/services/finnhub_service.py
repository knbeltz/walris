import hashlib
import logging
from datetime import UTC, date, datetime
from typing import Any

import httpx

from app.core.config import settings
from app.schemas.economic_event import EconomicEvent

logger = logging.getLogger(__name__)

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


def create_external_event_id(raw_event: dict[str, Any]) -> str:
    """
    Create a deterministic ID from the fields that identify the event.

    Actual, estimate, and previous values are deliberately excluded because
    those values can change after an economic release. Including them would
    cause the same event to receive a different ID when Finnhub updates it.
    """

    identity = "|".join(
        [
            str(raw_event.get("country") or ""),
            str(raw_event.get("event") or ""),
            str(raw_event.get("time") or ""),
            str(raw_event.get("unit") or ""),
        ]
    )

    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()

    return f"finnhub: {digest}"


def parse_release_time(raw_time: str) -> datetime:
    """
    Parse Finnhub's naive timestamp and mark it as UTC.

    datetime.fromisoformat handles values such as:
        2026-07-15 08:30
        2026-07-15 08:30:00

    replace(tzinfo=UTC) attaches timezone information without shifting
    the clock time.
    """

    naive_release_time = datetime.fromisoformat(raw_time)

    if naive_release_time.tzinfo is not None:
        return naive_release_time.astimezone(UTC)

    return naive_release_time.replace(tzinfo=UTC)


def normalize_economic_event(raw_event: dict[str, Any]) -> EconomicEvent:
    """
    Convert one Finnhub event into the application's EconomicEvent schema.
    """
    return EconomicEvent(
        external_event_id=create_external_event_id(raw_event),
        event_name=raw_event.get("event"),
        country=raw_event.get("country"),
        release_time=parse_release_time(raw_event["time"]),
        actual_value=raw_event.get("actual"),
        forecast_value=raw_event.get("estimate"),
        previous_value=raw_event.get("prev"),
        unit=raw_event.get("unit"),
        impact=raw_event.get("impact"),
        source="Finnhub",
    )


def fetch_todays_economic_events() -> list[EconomicEvent]:
    """
    Fetch economic events for this machine's local calendar date.

    httpx exceptions intentionally propagate:
    - HTTPStatusError for bad HTTP statuses
    - TimeoutException for timeouts
    - ConnectError for connection failures
    """

    local_today = date.today().isoformat()

    params = {"from": local_today, "to": local_today, "token": settings.finnhub_api_key}

    with httpx.Client(
        base_url=FINNHUB_BASE_URL,
        timeout=10.0,
    ) as client:
        try:
            response = client.get(
                "/calendar/economic",
                params=params,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("Finnhub returned %s: %s", exc.response.status_code, exc.response.text)
            raise
        except httpx.RequestError as exc:
            logger.error("Finnhub request failed: %s", exc)
            raise

        payload = response.json()

    raw_events = payload.get("economicCalendar")

    return [normalize_economic_event(raw_event) for raw_event in raw_events]
