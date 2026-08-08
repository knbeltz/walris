from pydantic import BaseModel


class BriefingSection(BaseModel):
    heading: str
    body: str


class BriefingContent(BaseModel):
    headline: str
    sections: list[BriefingSection]
