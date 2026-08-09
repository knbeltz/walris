import asyncio
import logging
from datetime import date
from typing import cast

import openai
from openai import AsyncOpenAI
from sqlalchemy import select

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.daily_data_items import DailyDataItem
from app.models.daily_data_news import DailyDataNews
from app.models.user import User
from app.models.user_briefings import UserBriefing
from app.schemas.user_briefing import BriefingContent
from app.services.fmp_category_rules import (
    CATEGORY_ITEM_KEYS,
    CATEGORY_MARKET_CONTENT,
    TOPIC_ITEM_KEYS,
    TOPIC_MARKET_CONTENT,
    MarketContentRules,
)
from app.services.prompt_services import (
    DailyDataItemWithNews,
    build_developer_message,
    build_quiet_day_briefing,
    build_user_message,
)

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

MAX_CONCURRENCY = 10


def get_relevant_fred_item_keys(user: User) -> frozenset[str]:
    """
    Return the FRED item keys relevant to the user's category
    and selected additional topics.
    """
    if user.category is None:
        return frozenset()

    category_keys: frozenset[str] = frozenset(CATEGORY_ITEM_KEYS.get(user.category, set()))

    topic_keys = frozenset().union(
        *(TOPIC_ITEM_KEYS[topic] for topic in user.additional_topics if topic in TOPIC_ITEM_KEYS)
    )

    return frozenset(category_keys | topic_keys)


def merge_market_content_rules(
    base: MarketContentRules,
    extra: MarketContentRules,
) -> MarketContentRules:
    return MarketContentRules(
        wants_all_sectors=(base.wants_all_sectors or extra.wants_all_sectors),
        wants_best_worst_sector=(base.wants_best_worst_sector or extra.wants_best_worst_sector),
        named_sectors=(base.named_sectors | extra.named_sectors),
        wants_company_spotlight=(base.wants_company_spotlight or extra.wants_company_spotlight),
        index_symbols=(base.index_symbols | extra.index_symbols),
    )


def get_relevant_market_content_rules(
    user: User,
) -> MarketContentRules:
    if user.category is None:
        return MarketContentRules()

    rules = CATEGORY_MARKET_CONTENT.get(
        user.category,
        MarketContentRules(),
    )

    for topic in user.additional_topics:
        topic_rules = TOPIC_MARKET_CONTENT.get(topic)

        if topic_rules is not None:
            rules = merge_market_content_rules(
                rules,
                topic_rules,
            )

    return rules


def filter_fmp_items_by_rules(
    fmp_items: list[DailyDataItem],
    rules: MarketContentRules,
) -> list[DailyDataItem]:
    relevant_items: set[DailyDataItem] = set()

    # 1. Indices
    relevant_items.update(item for item in fmp_items if item.item_key in rules.index_symbols)

    # 2. Sector rows
    sector_items = [item for item in fmp_items if item.item_key.startswith("sector:")]

    # All sectors overrides the more specific sector rules
    if rules.wants_all_sectors:
        relevant_items.update(sector_items)

    else:
        if rules.wants_best_worst_sector:
            sector_items_with_values = [item for item in sector_items if item.value is not None]

            if sector_items_with_values:
                relevant_items.add(
                    max(
                        sector_items_with_values,
                        key=lambda item: cast(float, item.value),
                    )
                )

                relevant_items.add(
                    min(
                        sector_items_with_values,
                        key=lambda item: cast(float, item.value),
                    )
                )

        if rules.named_sectors:
            relevant_items.update(
                item
                for item in sector_items
                if item.item_key.removeprefix("sector: ") in rules.named_sectors
            )

    # Companies
    if rules.wants_company_spotlight:
        relevant_items.update(item for item in fmp_items if item.item_key.startswith("company:"))

    return list(relevant_items)


# Need to implement step 4 of the filtering


def attach_news_to_daily_data_items(
    fred_items: list[DailyDataItem],
    fmp_items: list[DailyDataItem],
) -> list[DailyDataItemWithNews]:
    """
    Combine relevant FRED and FMP items and atach each item's
    linked DailyDataNews rows.
    """

    items = [*fred_items, *fmp_items]

    if not items:
        return []

    item_ids = [item.id for item in items]

    with SessionLocal() as session:
        news_rows = session.scalars(
            select(DailyDataNews).where(DailyDataNews.item_id.in_(item_ids))
        ).all()

    news_by_item_id: dict[
        object,
        list[DailyDataNews],
    ] = {}

    for news in news_rows:
        news_by_item_id.setdefault(
            news.item_id,
            [],
        ).append(news)

    return [
        DailyDataItemWithNews(
            item=item,
            news=tuple(news_by_item_id.get(item.id, [])),
        )
        for item in items
    ]


def get_relevant_fred_items_for_day(
    user: User,
    as_of: date,
) -> list[DailyDataItem]:
    """
    Return FRED DailyDataItem rows relevant to the user
    for the specified day.
    """
    relevant_item_keys = get_relevant_fred_item_keys(user)

    if not relevant_item_keys:
        return []

    with SessionLocal() as session:
        return list(
            session.scalars(
                select(DailyDataItem).where(
                    DailyDataItem.source == "fred",
                    DailyDataItem.date == as_of,
                    DailyDataItem.item_key.in_(relevant_item_keys),
                )
            ).all()
        )


def get_fmp_items_for_day(
    as_of: date,
) -> list[DailyDataItem]:
    """
    Return all FMP DailyDataItem rows for the specified day.
    """
    with SessionLocal() as session:
        return list(
            session.scalars(
                select(DailyDataItem).where(
                    DailyDataItem.source == "fmp",
                    DailyDataItem.date == as_of,
                )
            ).all()
        )


def get_relevant_fmp_items(
    user: User,
    fmp_items: list[DailyDataItem],
) -> list[DailyDataItem]:
    """
    Filter the day's FMP items according to the user's
    category and additional-topic market content rules.
    """

    rules = get_relevant_market_content_rules(user)

    return filter_fmp_items_by_rules(
        fmp_items,
        rules,
    )


def get_user_daily_data_with_news(
    user: User,
    as_of: date,
) -> list[DailyDataItemWithNews]:
    """
    Return the user's relevant FRED and FMP daily data,
    with linked news attached.
    """
    fred_items = get_relevant_fred_items_for_day(user, as_of)
    all_fmp_items = get_fmp_items_for_day(as_of)
    relevant_fmp_items = get_relevant_fmp_items(user, all_fmp_items)

    return attach_news_to_daily_data_items(
        fred_items,
        relevant_fmp_items,
    )


async def generate_briefing_content(user: User, as_of: date) -> BriefingContent:
    """
    Makes the OpenAI call to get the content that will be briefed to the user.
    """

    data = get_user_daily_data_with_news(user, as_of)

    if not data:
        return build_quiet_day_briefing()

    developer_message = build_developer_message(cast(str, user.category))
    user_message = build_user_message(data)

    response = await client.responses.parse(
        model="gpt-5-nano",
        input=[
            {"role": "developer", "content": developer_message},
            {"role": "user", "content": user_message},
        ],
        text_format=BriefingContent,
    )

    if response.output_parsed is None:
        return build_quiet_day_briefing()

    else:
        return response.output_parsed


async def generate_and_persist_all_briefings(as_of: date) -> None:
    with SessionLocal() as session:
        users = session.scalars(select(User).where(User.category.is_not(None))).all()

        already_done_user_ids = set(
            session.scalars(select(UserBriefing.user_id).where(UserBriefing.date == as_of)).all()
        )

        users_needing_briefings = [user for user in users if user.id not in already_done_user_ids]

    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async def generate_one(user: User) -> None:
        async with semaphore:
            try:
                content = await generate_briefing_content(user, as_of)

            except openai.OpenAIError:
                logger.exception(
                    "Failed to generate briefing for user",
                    extra={"user_id": user.id},
                )
                return

            with SessionLocal() as session:
                session.add(
                    UserBriefing(
                        user_id=user.id,
                        date=as_of,
                        content=content.model_dump(mode="json"),
                    )
                )
                session.commit()

    tasks = [generate_one(user) for user in users_needing_briefings]
    await asyncio.gather(*tasks)
