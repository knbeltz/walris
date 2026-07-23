from pydantic import BaseModel 

class UserPreferences(BaseModel):
    category: str | None
    additional_topics: list[str]