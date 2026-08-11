from datetime import date

from pydantic import BaseModel


class BriefingSection(BaseModel):
    heading: str
    body: str


class BriefingContent(BaseModel):
    headline: str
    sections: list[BriefingSection]


class UserBriefingResponse(BaseModel):
    date: date
    content: BriefingContent
