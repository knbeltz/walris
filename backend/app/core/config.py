from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # extra="ignore": .env intentionally documents config for later milestones
    # (API keys, etc.) before Settings has a field to read them into.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: Literal["development", "production"] = "development"
    database_url: str
    fmp_api_key: str
    marketaux_api_key: str
    fred_api_key: str


settings = Settings()
