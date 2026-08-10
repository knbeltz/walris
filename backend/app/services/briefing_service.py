import logging
from datetime import UTC, date, datetime

from sqlalchemy.exc import SQLAlchemyError

from app.core.database import SessionLocal
from app.models.job_run import JobRun
from app.services.daily_data_service import (
    delete_stale_daily_data,
    fetch_covered_daily_data_candidates,
    saved_covered_daily_data_candidates,
)
from app.services.openai_service import generate_and_persist_all_briefings

JOB_NAME = "daily_briefing_job"
MARKET_CAP_THRESHOLD = 10_000_000_000.0

logger = logging.getLogger(__name__)


async def run_daily_briefing_job(as_of: date) -> None:
    error_message: str | None = None

    with SessionLocal() as session:
        job_run = JobRun(
            job_name=JOB_NAME,
            status="running",
            started_at=datetime.now(UTC),
        )
        session.add(job_run)
        session.commit()

        try:
            covered_candidates = await fetch_covered_daily_data_candidates(
                as_of, MARKET_CAP_THRESHOLD
            )
            saved_covered_daily_data_candidates(covered_candidates, as_of)
            await generate_and_persist_all_briefings(as_of)
            status = "success"

        except Exception as error:
            status = "failed"
            error_message = str(error)

        try:
            delete_stale_daily_data()

        except SQLAlchemyError:
            logger.exception("Failed to delete stale daily data")

        job_run.status = status
        job_run.finished_at = datetime.now(UTC)
        job_run.error_message = error_message

        session.commit()
