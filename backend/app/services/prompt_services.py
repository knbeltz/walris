from dataclasses import dataclass

from app.models.daily_data_items import DailyDataItem
from app.models.daily_data_news import DailyDataNews

CATEGORY_MAIN_QUESTIONS: dict[str, str] = {
    "investor": (
        "Where is the economy headed, and what does that mean for financial "
        "markets and investment portfolios?"
    ),
    "small_business_owner": (
        "Are business costs, consumer demand, financing conditions, and hiring "
        "conditions improving or worsening?"
    ),
    "consumer": ("What is happening to my cost of living, income, debt, and purchasing power?"),
    "home": (
        "Are homes becoming more affordable, and what's happening to mortgage "
        "rates, housing supply, and property values?"
    ),
    "student": (
        "What does the economy mean for my living costs, borrowing costs, "
        "internships, and ability to find work after graduation?"
    ),
    "job_seeker": (
        "Is hiring improving, where are opportunities emerging, and how much "
        "bargaining power do workers have?"
    ),
    "everything": (
        "What's happening across the entire economy — inflation, employment, "
        "housing, business activity, interest rates, and financial markets?"
    ),
}

DEVELOPER_MESSAGE_TEMPLATE = """\
You are writing a daily economic briefing for Walris, a calm, editorial-style \
app that explains what happened in the economy and why it matters — not a \
trading app, not a news firehose. The reader should be able to read this in \
under five minutes.

The reader you're writing for cares most about this question: {main_question}

You will be given a set of economic data points (FRED indicators and/or FMP \
market data) and, for each one, a handful of recent news articles covering it. \
Use only the data and news you are given — do not state or infer any figure, \
event, or fact that isn't present in what was provided.

Write in a narrative style, not a bulleted list of statistics — but every \
section must include the actual quantitative figures from the data \
(percentages, dollar amounts, index levels, etc.), not vague language like \
"inflation is rising." Ground each section's narrative in the news provided, \
not just the raw number.

Structure your response as:
- One overall headline for the whole briefing.
- A few sections, each covering one theme from the data. Each section has its \
own short heading and a short narrative paragraph (2-4 sentences).

Keep the tone calm and explanatory, never alarmist or speculative.
"""


def build_developer_message(category: str) -> str:
    """
    Build the developer/system message for one briefing generation call,
    interpolating that category's main question.

    Raises KeyError if `category` isn't one of the 7 known category slugs —
    callers are expected to only reach this point for users with a valid,
    already-set category.
    """
    main_question = CATEGORY_MAIN_QUESTIONS[category]

    return DEVELOPER_MESSAGE_TEMPLATE.format(main_question=main_question)


@dataclass(frozen=True, slots=True)
class DailyDataItemWithNews:
    item: DailyDataItem
    news: tuple[DailyDataNews, ...]
