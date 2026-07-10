# This file's only job is to wire things together — no route handlers,
# business logic, or config parsing should live directly in here (see
# Milestone 3, Phase 2 decision on keeping main.py thin).

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.routers.health import router

configure_logging(settings.environment)
app = FastAPI()
app.include_router(router)
