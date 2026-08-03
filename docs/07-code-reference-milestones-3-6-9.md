# Code Reference — Milestones 3, 6, 9

**Document:** docs/07-code-reference-milestones-3-6-9.md
**Status:** Reference document (not living — a snapshot)

---

## Why this document exists

Across Milestones 3–9, Claude wrote all of the actual code — Milestones 5, 7, and 8 were pure
configuration/verification with no real logic, but Milestones 3, 6, and 9 involved genuine
programming (functions, classes, conditional logic, data modeling, and a couple of real bugs that
needed real debugging). This document collects that code in one place for reference and study.

**This is a snapshot, not something to copy forward.** Starting Milestone 10, the working
agreement is: the user writes pseudocode and implementation; Claude handles configuration/tooling
and reviews. See `docs/05-resume-prompt.md`'s Important Decisions section and
`docs/06-learning-notes.md` for the concepts behind this code explained with analogies — this
document is just the code itself, organized by milestone.

---

## Milestone 3 — Backend Foundation

The first real backend code: settings loading, logging, and a health route, wired together in
`main.py`.

### `backend/app/core/config.py`

```python
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # extra="ignore": .env intentionally documents config for later milestones
    # (API keys, etc.) before Settings has a field to read them into.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: Literal["development", "production"] = "development"
    database_url: str


settings = Settings()
```

### `backend/app/core/logging.py`

```python
import logging


def configure_logging(environment: str) -> None:
    log_level = logging.DEBUG if environment == "development" else logging.INFO

    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
```

---

## Milestone 6 — Supabase Setup

Real data modeling: the SQLAlchemy engine/session setup, all 7 table models, and the Alembic
migration that creates them. This is where the authentication debugging saga happened (see
`docs/05-resume-prompt.md` and `docs/06-learning-notes.md` for the full story) — the actual root
cause was in `alembic/env.py`, reusing a separately-built engine instead of the one below.

### `backend/app/core/database.py`

```python
from collections.abc import Generator
from datetime import datetime

from sqlalchemy import DateTime, create_engine, func
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.core.config import settings

# Supabase's connection string uses the bare "postgresql://" scheme, which
# SQLAlchemy defaults to the old psycopg2 driver. Force psycopg (v3) instead.
db_url = make_url(settings.database_url).set(drivername="postgresql+psycopg")
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `backend/app/models/briefing.py`

```python
import uuid
from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class Briefing(Base, TimestampMixin):
    __tablename__ = "briefings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    briefing_date: Mapped[date] = mapped_column(Date, unique=True)
    title: Mapped[str]
    summary: Mapped[str]
    status: Mapped[str]
```

### `backend/app/models/economic_event.py`

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class EconomicEvent(Base, TimestampMixin):
    __tablename__ = "economic_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    briefing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("briefings.id", ondelete="CASCADE"))
    external_event_id: Mapped[str]
    event_name: Mapped[str]
    country: Mapped[str]
    release_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    actual_value: Mapped[float | None]
    forecast_value: Mapped[float | None]
    previous_value: Mapped[float | None]
    unit: Mapped[str | None]
    source: Mapped[str]
```

### `backend/app/models/enriched_event.py`

```python
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class EnrichedEvent(Base, TimestampMixin):
    __tablename__ = "enriched_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("economic_events.id", ondelete="CASCADE")
    )
    importance_score: Mapped[int]
    importance_reason: Mapped[str]
    plain_english_summary: Mapped[str]
    historical_context_summary: Mapped[str | None]
    news_context_summary: Mapped[str | None]
    affected_groups: Mapped[list[str]] = mapped_column(JSONB)
```

### `backend/app/models/fred_series.py`

```python
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class FredSeries(Base, TimestampMixin):
    __tablename__ = "fred_series"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("economic_events.id", ondelete="CASCADE")
    )
    series_id: Mapped[str]
    series_name: Mapped[str]
    latest_value: Mapped[float]
    previous_value: Mapped[float | None]
    ten_year_average: Mapped[float | None]
    historical_percentile: Mapped[float | None]
    trend_direction: Mapped[str | None]
    data_points: Mapped[list[dict[str, float]]] = mapped_column(JSONB)
```

### `backend/app/models/news_article.py`

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class NewsArticle(Base, TimestampMixin):
    __tablename__ = "news_articles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("economic_events.id", ondelete="CASCADE")
    )
    headline: Mapped[str]
    source: Mapped[str]
    url: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    summary: Mapped[str | None]
    sentiment: Mapped[str | None]
    entities: Mapped[list[str]] = mapped_column(JSONB)
    topics: Mapped[list[str]] = mapped_column(JSONB)
```

### `backend/app/models/device_token.py`

```python
import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, TimestampMixin


class DeviceToken(Base, TimestampMixin):
    __tablename__ = "device_tokens"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    expo_push_token: Mapped[str] = mapped_column(unique=True)
    device_id: Mapped[str]
    platform: Mapped[str]
    timezone: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
```

### `backend/app/models/job_run.py`

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class JobRun(Base):
    __tablename__ = "job_runs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    job_name: Mapped[str]
    status: Mapped[str]
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None]
    # "metadata" is a reserved attribute name on SQLAlchemy's declarative Base
    # (Base.metadata is the schema's MetaData object) — job_metadata is the
    # Python-side name, "metadata" is still the actual database column name.
    job_metadata: Mapped[dict[str, str] | None] = mapped_column("metadata", JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

### `backend/app/models/__init__.py`

```python
from app.models.briefing import Briefing
from app.models.device_token import DeviceToken
from app.models.economic_event import EconomicEvent
from app.models.enriched_event import EnrichedEvent
from app.models.fred_series import FredSeries
from app.models.job_run import JobRun
from app.models.news_article import NewsArticle

__all__ = [
    "Briefing",
    "DeviceToken",
    "EconomicEvent",
    "EnrichedEvent",
    "FredSeries",
    "JobRun",
    "NewsArticle",
]
```

### `backend/alembic/env.py`

```python
from logging.config import fileConfig

import app.models  # noqa: F401  (imports every model so Base.metadata is fully populated)
from alembic import context
from app.core.database import Base, engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Reuses the same Engine app/core/database.py builds for the rest of the
    app, rather than re-parsing the connection URL from a string a second
    time (that string round-trip was the source of a real, hard-to-diagnose
    bug — see Milestone 6 notes in docs/06-resume-prompt.md).
    """
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### `backend/alembic/versions/b9a040b66e1e_create_initial_tables.py`

Auto-generated by `alembic revision --autogenerate` from the models above, then reviewed before
applying (never trust an autogenerated migration blindly — this one was checked against the model
definitions column by column before running).

```python
"""create initial tables

Revision ID: b9a040b66e1e
Revises:
Create Date: 2026-07-10 10:49:01.480299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b9a040b66e1e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('briefings',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('briefing_date', sa.Date(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('summary', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('briefing_date')
    )
    op.create_table('device_tokens',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('expo_push_token', sa.String(), nullable=False),
    sa.Column('device_id', sa.String(), nullable=False),
    sa.Column('platform', sa.String(), nullable=False),
    sa.Column('timezone', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('expo_push_token')
    )
    op.create_table('job_runs',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('job_name', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('error_message', sa.String(), nullable=True),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('economic_events',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('briefing_id', sa.Uuid(), nullable=False),
    sa.Column('external_event_id', sa.String(), nullable=False),
    sa.Column('event_name', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('release_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('actual_value', sa.Float(), nullable=True),
    sa.Column('forecast_value', sa.Float(), nullable=True),
    sa.Column('previous_value', sa.Float(), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['briefing_id'], ['briefings.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('enriched_events',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('event_id', sa.Uuid(), nullable=False),
    sa.Column('importance_score', sa.Integer(), nullable=False),
    sa.Column('importance_reason', sa.String(), nullable=False),
    sa.Column('plain_english_summary', sa.String(), nullable=False),
    sa.Column('historical_context_summary', sa.String(), nullable=True),
    sa.Column('news_context_summary', sa.String(), nullable=True),
    sa.Column('affected_groups', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['economic_events.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fred_series',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('event_id', sa.Uuid(), nullable=False),
    sa.Column('series_id', sa.String(), nullable=False),
    sa.Column('series_name', sa.String(), nullable=False),
    sa.Column('latest_value', sa.Float(), nullable=False),
    sa.Column('previous_value', sa.Float(), nullable=True),
    sa.Column('ten_year_average', sa.Float(), nullable=True),
    sa.Column('historical_percentile', sa.Float(), nullable=True),
    sa.Column('trend_direction', sa.String(), nullable=True),
    sa.Column('data_points', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['economic_events.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news_articles',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('event_id', sa.Uuid(), nullable=False),
    sa.Column('headline', sa.String(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('summary', sa.String(), nullable=True),
    sa.Column('sentiment', sa.String(), nullable=True),
    sa.Column('entities', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('topics', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['economic_events.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('news_articles')
    op.drop_table('fred_series')
    op.drop_table('enriched_events')
    op.drop_table('economic_events')
    op.drop_table('job_runs')
    op.drop_table('device_tokens')
    op.drop_table('briefings')
```

---

## Milestone 9 — API Foundation

Real programming: an error-response schema, a logging middleware class, three exception handlers
with actual branching logic, an empty versioned router, and the wiring in `main.py`. This is also
where we found and fixed a real bug — the 404 handler initially didn't catch "no matching route"
errors because they're raised as Starlette's *base* `HTTPException`, not the `fastapi.HTTPException`
subclass we'd first registered against.

### `backend/app/schemas/errors.py`

```python
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
    request_id: str
```

### `backend/app/schemas/health.py`

```python
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
```

### `backend/app/core/middleware.py`

```python
import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "%s %s %d %.1fms request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )
        response.headers["X-Request-ID"] = request_id
        return response
```

### `backend/app/core/exceptions.py`

```python
import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.schemas.errors import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)

_STATUS_CODE_TO_ERROR_CODE = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    500: "INTERNAL_SERVER_ERROR",
}


def _error_response(request: Request, status_code: int, code: str, message: str) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    body = ErrorResponse(error=ErrorDetail(code=code, message=message), request_id=request_id)
    return JSONResponse(status_code=status_code, content=body.model_dump())


# Registered against Starlette's base HTTPException (not fastapi.HTTPException,
# a subclass) because routing-level errors like "no matching route" (404) are
# raised as the base class — a handler registered only on the subclass would
# miss them and silently fall through to FastAPI's default handler.
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    code = _STATUS_CODE_TO_ERROR_CODE.get(exc.status_code, "HTTP_ERROR")
    return _error_response(request, exc.status_code, code, str(exc.detail))


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return _error_response(
        request, status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR", str(exc.errors())
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    logger.exception("Unhandled exception (request_id=%s)", request_id)
    message = str(exc) if settings.environment == "development" else "Internal server error."
    return _error_response(
        request, status.HTTP_500_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", message
    )
```

### `backend/app/routers/__init__.py`

```python
# Future versioned endpoints (briefings, events, notifications, admin) get
# registered on this router — it's included in the app now, with no routes
# yet, so the /v1 prefix is already solved when the first real one arrives.
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")
```

### `backend/app/routers/health.py` (current form, updated across Milestones 6 and 9)

```python
# This should stay intentionally trivial right now — there is no external
# API to check yet (those arrive in later milestones).

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)) -> HealthResponse:
    db.execute(text("SELECT 1"))
    return HealthResponse(status="ok")
```

### `backend/app/main.py` (current form, updated across Milestones 3, 6, and 9)

```python
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
```
