from datetime import date

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.device_token import DeviceToken
from app.models.job_run import JobRun
from app.models.user import User
from app.models.user_briefings import UserBriefing
from app.routers.briefings import get_todays_briefing
from app.services.briefing_service import JOB_NAME, run_daily_briefing_job
from app.services.notification_service import send_daily_notifications


async def run_backend(as_of: date, user: User) -> None:

    results = []

    await run_daily_briefing_job(as_of)

    with SessionLocal() as session:
        job_run = session.scalar(
            select(JobRun).where(JobRun.job_name == JOB_NAME).order_by(JobRun.started_at.desc())
        )
        results.append(
            (
                "Step 1: JobRun succeeded",
                job_run is not None and job_run.status == "success",
                f"status={job_run.status if job_run else 'NOT FOUND'}",
            )
        )

        briefing_row = session.scalar(
            select(UserBriefing).where(
                UserBriefing.user_id == user.id,
                UserBriefing.date == as_of,
            )
        )
        results.append(
            (
                "Step 1: UserBriefing created",
                briefing_row is not None,
                f"found={briefing_row is not None}",
            )
        )

        result = get_todays_briefing(user, db=session)

        results.append(
            (
                "Step 2: briefing date matches",
                result.date == as_of,
                f"result.date-{result.date}, as_of={as_of}",
            )
        )

        results.append(
            (
                "Step 2: headline is real content",
                result.content.headline != "No briefing available yet for today.",
                f"headline={result.content.headline!r}",
            )
        )

    fake_token = "ExponentPushToken[fake-token-for-integration-check]"

    with SessionLocal() as session:
        device_token = DeviceToken(
            expo_push_token=fake_token,
            device_id="integration-check_device",
            platform="ios",
            timezone="America/New_York",
            user_id=user.id,
        )
        session.add(device_token)
        session.commit()

    await send_daily_notifications(as_of)

    with SessionLocal() as session:
        found_device_token = session.scalar(
            select(DeviceToken).where(DeviceToken.expo_push_token == fake_token)
        )
        results.append(
            (
                "Step 3: Device token deactiviated",
                found_device_token is not None and found_device_token.is_active is False,
                f"is_active={found_device_token.is_active if found_device_token else 'NOT FOUND'}",
            )
        )

        if found_device_token is not None:
            session.delete(found_device_token)
            session.commit()

    for name, passed, detail in results:
        print(f"{'PASS' if passed else 'FAIL'} - {name} ({detail})")

    if all(passed for _, passed, _ in results):
        print("\nAll checks passed.")

    else:
        print("\nSome checks failed.")
