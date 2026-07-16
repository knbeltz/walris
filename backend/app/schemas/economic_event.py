from datetime import datetime

from pydantic import BaseModel


class EconomicEvent(BaseModel):
    external_event_id: str
    event_name: str
    country: str
    release_time: datetime
    actual_value: float | None
    forecast_value: float | None
    previous_value: float | None
    impact: str | None
    unit: str | None
    source: str
