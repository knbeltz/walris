from datetime import date 
from pydantic import BaseModel

class FredObservation(BaseModel):
    series_id: str
    name: str
    value: float | None
    date: date


