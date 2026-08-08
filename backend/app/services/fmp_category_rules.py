# Per-category and per-topic FRED indicator sets, transcribed from
# docs/08-personalization-pivot-plan.md §5/§6. FMP content (index quotes,
# sector performances, gainer/loser) deliberately isn't included here yet:
# sector/company item_keys change daily (they're keyed by whichever sector/
# symbol the data turns out to be that day), so they can't be expressed as a
# fixed set of strings the way FRED series IDs can — they need prefix
# matching plus, for some categories, a runtime best/worst computation
# against that day's persisted rows. Index quotes are blocked separately:
# the actual list of index symbols to fetch isn't defined anywhere in the
# codebase yet. All of that needs its own logic, layered on top of these
# two tables rather than folded into them.

from dataclasses import dataclass, field

from app.services.daily_data_service import (
    MARKET_INDEX_SYMBOLS,
    NASDAQ_COMPOSITE_SYMBOL,
    SP_500_SYMBOL,
)

CATEGORY_ITEM_KEYS: dict[str, set[str]] = {
    "investor": {
        # Inflation (1-5)
        "CPIAUCSL",
        "CPILFESL",
        "PCEPI",
        "PCEPILFE",
        "PPIACO",
        # Employment & Labor (9-11, 13-15)
        "PAYEMS",
        "UNRATE",
        "ICSA",
        "CIVPART",
        "CES0500000003",
        "JTSJOL",
        # Economic Growth (16-19)
        "GDP",
        "RSAFS",
        "INDPRO",
        "TCU",
        # Interest Rates & Monetary Policy (22, 24-28)
        "FEDFUNDS",
        "DGS2",
        "DGS10",
        "DGS30",
        "T10Y2Y",
        "M2SL",
        # Housing (30-33)
        "HOUST",
        "PERMIT",
        "EXHOSLUSM495S",
        "HSN1F",
    },
    "small_business_owner": {
        "CPIAUCSL",
        "PPIACO",
        "CPIENGSL",
        "GASREGW",
        "UNRATE",
        "ICSA",
        "CIVPART",
        "CES0500000003",
        "JTSJOL",
        "GDP",
        "RSAFS",
        "INDPRO",
        "TCU",
        "UMCSENT",
        "DSPI",
        "FEDFUNDS",
        "MPRIME",
        "HOUST",
        "PERMIT",
    },
    "consumer": {
        "CPIAUCSL",
        "PCEPI",
        "CUSR0000SEHA",
        "CPIUFDSL",
        "CPIENGSL",
        "GASREGW",
        "UNRATE",
        "ICSA",
        "CES0500000003",
        "DSPI",
        "TERMCBCCALLNS",
        "FEDFUNDS",
        "MPRIME",
        "RSAFS",
        "UMCSENT",
    },
    "home": {
        "MORTGAGE30US",
        "MORTGAGE15US",
        "FEDFUNDS",
        "DGS10",
        "MPRIME",
        "CSUSHPISA",
        "USSTHPI",
        "HOUST",
        "PERMIT",
        "EXHOSLUSM495S",
        "HSN1F",
        "CPIAUCSL",
        "UNRATE",
        "CES0500000003",
        "DSPI",
        "CUSR0000SEHA",
        "POPTHM",
    },
    "student": {
        "UNRATE",
        "ICSA",
        "CCSA",
        "CIVPART",
        "JTSJOL",
        "CES0500000003",
        "CPIAUCSL",
        "CUSR0000SEHA",
        "CPIUFDSL",
        "CPIENGSL",
        "GASREGW",
        "TERMCBCCALLNS",
        "FEDFUNDS",
        "GDP",
        "RSAFS",
        "INDPRO",
        "DSPI",
    },
    "job_seeker": {
        "PAYEMS",
        "UNRATE",
        "ICSA",
        "CCSA",
        "JTSJOL",
        "CIVPART",
        "CES0500000003",
        "GDP",
        "RSAFS",
        "INDPRO",
        "UMCSENT",
        "HOUST",
        "PERMIT",
        "PPIACO",
        "FEDFUNDS",
        "CPIAUCSL",
    },
    "everything": {
        "CPIAUCSL",
        "CPILFESL",
        "PCEPI",
        "PCEPILFE",
        "PPIACO",
        "CUSR0000SEHA",
        "CPIUFDSL",
        "CPIENGSL",
        "PAYEMS",
        "UNRATE",
        "ICSA",
        "CCSA",
        "CIVPART",
        "CES0500000003",
        "JTSJOL",
        "GDP",
        "RSAFS",
        "INDPRO",
        "TCU",
        "UMCSENT",
        "DSPI",
        "FEDFUNDS",
        "MPRIME",
        "DGS2",
        "DGS10",
        "DGS30",
        "T10Y2Y",
        "M2SL",
        "TERMCBCCALLNS",
        "HOUST",
        "PERMIT",
        "EXHOSLUSM495S",
        "HSN1F",
        "MORTGAGE30US",
        "MORTGAGE15US",
        "CSUSHPISA",
        "USSTHPI",
        "POPTHM",
        "GASREGW",
    },
}

# FRED-backed topics only. "major_market_indicies", "industry_sector_
# performance", and "company_spotlights" are additional_topics values too,
# but their item_keys are FMP-sourced and dynamic per day — see the module
# docstring above. They aren't included as keys here yet.
TOPIC_ITEM_KEYS: dict[str, set[str]] = {
    "inflation": {
        "CPIAUCSL",
        "CPILFESL",
        "PCEPI",
        "PCEPILFE",
        "PPIACO",
        "CUSR0000SEHA",
        "CPIUFDSL",
        "CPIENGSL",
    },
    "employment_labor": {
        "PAYEMS",
        "UNRATE",
        "ICSA",
        "CCSA",
        "CIVPART",
        "CES0500000003",
        "JTSJOL",
    },
    "economic_growth": {
        "GDP",
        "RSAFS",
        "INDPRO",
        "TCU",
        "UMCSENT",
        "DSPI",
    },
    "housing": {
        "HOUST",
        "PERMIT",
        "EXHOSLUSM495S",
        "HSN1F",
        "MORTGAGE30US",
        "MORTGAGE15US",
        "CSUSHPISA",
        "USSTHPI",
        "POPTHM",
    },
    # Item 29 (Credit Card Interest Rate) is dual-tagged in the plan doc
    # (Interest Rates & Monetary Policy / Consumer Costs) — included in both
    # topics below deliberately. A user picking both just gets it once, since
    # this feeds into a set union.
    "interest_rates_monetary_policy": {
        "FEDFUNDS",
        "MPRIME",
        "DGS2",
        "DGS10",
        "DGS30",
        "T10Y2Y",
        "M2SL",
        "TERMCBCCALLNS",
    },
    # Broadened beyond the plan doc's literal "Consumer Costs" tag (which
    # covers only Gas Prices + Credit Card Rate) to match how the Consumers
    # category itself frames "cost of living" — see the Consumers category
    # entry above, which lists the same five inflation-tagged items plus
    # these two.
    "consumer_cost": {
        "CPIAUCSL",
        "PCEPI",
        "CUSR0000SEHA",
        "CPIUFDSL",
        "CPIENGSL",
        "GASREGW",
        "TERMCBCCALLNS",
    },
}


@dataclass(frozen=True, slots=True)
class MarketContentRules:
    wants_all_sectors: bool = False
    wants_best_worst_sector: bool = False
    named_sectors: frozenset[str] = field(default_factory=frozenset)
    wants_company_spotlight: bool = False
    index_symbols: frozenset[str] = field(
        default_factory=frozenset,
    )


CATEGORY_MARKET_CONTENT: dict[str, MarketContentRules] = {
    "investor": MarketContentRules(
        wants_all_sectors=True,
        wants_company_spotlight=True,
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS),
    ),
    "small_business_owner": MarketContentRules(
        wants_best_worst_sector=True,
        index_symbols=frozenset(
            {
                SP_500_SYMBOL,
            }
        ),
    ),
    "consumer": MarketContentRules(),
    "home": MarketContentRules(
        named_sectors=frozenset(
            {
                "Real Estate",
                "Financial Services",
                "Consumer Cyclical",
            }
        ),
        index_symbols=frozenset(
            {
                SP_500_SYMBOL,
            }
        ),
    ),
    "student": MarketContentRules(
        wants_best_worst_sector=True,
        index_symbols=frozenset(
            {
                SP_500_SYMBOL,
                NASDAQ_COMPOSITE_SYMBOL,
            }
        ),
    ),
    "job_seeker": MarketContentRules(
        wants_best_worst_sector=True,
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS),
    ),
    "everything": MarketContentRules(
        wants_all_sectors=True,
        wants_company_spotlight=True,
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS),
    ),
}

TOPIC_MARKET_CONTENT: dict[str, MarketContentRules] = {
    "industry_sector_performance": MarketContentRules(
        wants_all_sectors=True,
    ),
    "company_spotlights": MarketContentRules(
        wants_company_spotlight=True,
    ),
    "major_market_indicies": MarketContentRules(
        index_symbols=frozenset(MARKET_INDEX_SYMBOLS),
    ),
}
