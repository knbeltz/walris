# This file's only job is to wire things together — no route handlers,
# business logic, or config parsing should live directly in here (see
# Milestone 3, Phase 2 decision on keeping main.py thin).

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.core.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.routers import v1_router
from app.routers.health import router as health_router

configure_logging(settings.environment)
app = FastAPI()

app.add_middleware(RequestLoggingMiddleware)

app.exception_handler(RequestValidationError)(validation_exception_handler)
app.exception_handler(HTTPException)(http_exception_handler)
app.exception_handler(Exception)(unhandled_exception_handler)

app.include_router(health_router)
app.include_router(v1_router)
