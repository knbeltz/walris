from datetime import date

from fastapi import APIRouter, Depends

from app.core.auth import verify_admin_secret
from app.services.briefing_service import run_daily_briefing_job
from app.services.notification_service import send_daily_notifications

router = APIRouter()


@router.post(
    "/admin/trigger-briefing",
    dependencies=[Depends(verify_admin_secret)],
)
async def trigger_briefing() -> dict[str, str]:
    today = date.today()

    await run_daily_briefing_job(today)

    return {
        "status": "success",
        "date": today.isoformat(),
    }

@router.post(
    "/admin/trigger-notifications",
    dependencies=[Depends(verify_admin_secret)],
)
async def trigger_notifications() -> dict[str, str]:
    today = date.today()

    await send_daily_notifications(today)

    return {
            "status": "success",
            "date": today.isoformat(),
        }
