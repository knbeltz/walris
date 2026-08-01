from datetime import date
from typing import Any

from pydantic import BaseModel

class DailyDataItemCandidate(BaseModel):
    item_key: str
    source: str
    value: float
    raw_data: dict[str, Any]