# Application settings, loaded once at startup.
#
# Pseudocode (Phase 3, Milestone 3):
#   1. Load settings — fail fast if invalid
#
# TODO:
# - Define a Settings class using pydantic_settings.BaseSettings, with at
#   least an `environment` field (e.g. "development" / "production").
# - Create a single, reusable settings instance at module level that the
#   rest of the app imports from here (e.g. `settings = Settings()`).
#   Instantiating it at import time is what makes this "fail fast" — if
#   required fields are missing/invalid, this line raises immediately.
#
# Note: this stays intentionally tiny for Milestone 3. DATABASE_URL and the
# external API keys don't arrive until Milestones 6 and 7 — don't add them
# yet.

from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
     environment: Literal["development", "production"] = "development"

settings = Settings()