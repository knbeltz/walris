# Application entrypoint.
#
# This file's only job is to wire things together — no route handlers,
# business logic, or config parsing should live directly in here (see
# Milestone 3, Phase 2 decision on keeping main.py thin).
#
# Pseudocode (Phase 3, Milestone 3):
#   1. Load settings — fail fast if invalid
#   2. Configure logging using values from settings
#   3. Create the FastAPI app instance
#   4. Register routers (including the health router)
#
# TODO: implement the four steps above, in order, using:
# - app.core.config (step 1)
# - app.core.logging (step 2)
# - fastapi.FastAPI (step 3)
# - app.routers.health (step 4, via app.include_router(...))

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.routers.health import router

configure_logging(settings.environment)
app = FastAPI()
app.include_router(router)

