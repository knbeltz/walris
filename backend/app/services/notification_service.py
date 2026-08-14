import asyncio
import logging
from datetime import date

import httpx
from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.device_token import DeviceToken
from app.models.user_briefings import UserBriefing

logger = logging.getLogger(__name__)


async def send_push_notifications(
    client: httpx.AsyncClient, token: str, title: str, body: str
) -> None:

    try:
        response = await client.post(
            "https://exp.host/--/api/v2/push/send",
            json={"to": token, "title": title, "body": body},
        )
        response.raise_for_status()

    except httpx.HTTPError:
        logger.exception(
            "Failed to send push notification for token %s",
            token,
        )
        return

    ticket = response.json()["data"]

    if ticket["status"] != "error":
        return

    error_type = ticket.get("details", {}).get("error")

    if error_type == "DeviceNotRegistered":
        session = SessionLocal()
        try:
            device_token = session.scalar(
                select(DeviceToken).where(DeviceToken.expo_push_token == token)
            )
            if device_token is not None:
                device_token.is_active = False
                session.commit()
        finally:
            session.close()

    logger.warning(
        "Push notification failed for token %s: %s",
        token,
        ticket.get("message"),
    )


async def send_daily_notifications(as_of: date) -> None:
    # Don't send daily notifications on weekends.
    if as_of.weekday() >= 5:
        return

    session = SessionLocal()

    try:
        briefings = session.scalars(select(UserBriefing).where(UserBriefing.date == as_of)).all()

        notifications: list[tuple[str, str]] = []

        for briefing in briefings:
            if not briefing.content["sections"]:
                continue

            device_tokens = session.scalars(
                select(DeviceToken).where(
                    DeviceToken.user_id == briefing.user_id,
                    DeviceToken.is_active.is_(True),
                )
            ).all()

            for device_token in device_tokens:
                notifications.append(
                    (
                        device_token.expo_push_token,
                        briefing.content["headline"],
                    )
                )

    finally:
        session.close()

    semaphore = asyncio.Semaphore(10)

    async with httpx.AsyncClient() as client:

        async def send_one(
            token: str,
            context: str,
        ) -> None:
            async with semaphore:
                await send_push_notifications(
                    client=client,
                    token=token,
                    title="Your Daily Briefing",
                    body=context,
                )

        tasks = [send_one(token, headline) for token, headline in notifications]

        await asyncio.gather(*tasks)
