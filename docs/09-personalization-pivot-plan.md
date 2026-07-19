# Walris Personalization Pivot — Planning Document

**Document:** docs/09-personalization-pivot-plan.md
**Status:** Draft — planning reference for the next phase of backend/mobile work
**Created:** 2026-07-19 · **Revised:** 2026-07-19 (incorporated user's detailed category/indicator plan)

---

## 1. Why this pivot

Walris originally planned a single daily briefing built around Finnhub's economic calendar
(discrete "top 5 events," each enriched with FRED history, Marketaux news, and an OpenAI
explanation). Finnhub's calendar turned out to require a paid plan; Financial Modeling Prep's
(FMP) equivalent calendar endpoints were also either paid or fully retired. Milestone 12 was
already rebuilt around FMP's genuinely free market-data endpoints instead (index snapshot, sector
performance, a market-cap-filtered company spotlight) — see `docs/06-resume-prompt.md` for that
full story. That work is done and committed.

This document plans the next, larger pivot: instead of one identical briefing for everyone,
**users sign up, pick the one category that best describes them, optionally add extra topics on
top, and get their own individually-generated daily briefing** — built from FRED historical data,
Marketaux news, and an OpenAI narrative generated fresh for each registered user.

## 2. Confirmed decisions

- **7 categories, single-select**: Investors, Small Business Owners/Entrepreneurs, Consumers,
  Home Owners/Home Buyers, Students, Job Seekers, and **"I Want Everything"** (a 7th category
  that includes every indicator and every FMP market module — not a toggle layered on top of the
  other 6, but a full category in its own right). A user picks **exactly one**.
- **Optional additional topics, layered on top of the single category choice**: after picking a
  category, the user is asked whether they want news on any additional topic groups — Inflation,
  Employment and Labor, Economic Growth, Housing, Consumer Costs, Major Market Indices, Industry
  Sector Performance, Company Spotlights. Purely optional, multi-select.
- **Authentication moves into V1 now, via Clerk (React Native)** — a deliberate reversal of the
  previously documented "no auth in V1, deferred to V2" decision
  (`docs/02-system-architecture.md` §4/§29). This isn't inventing a new direction: §29 already
  named Clerk as the anticipated V2 provider specifically for "when personalization is added" —
  this pivot pulls that forward because category selection needs to be tied to a real account.
- **Preferences are editable anytime** in a settings screen (category + additional topics).
- **Per-user OpenAI generation** — every registered user gets their own individually-generated
  briefing/notification via OpenAI's nano model, even if two users picked identical
  category+topic selections. This is real personalization, not shared/cached text — cost scales
  directly with registered-user count, a deliberate tradeoff accepted over the cheaper
  shared-per-category-text alternative.
- **Data is temporary, not permanently archived**: all fetched FRED/Marketaux/FMP data for a
  given day is deleted from the database **48 hours** after it was fetched. Walris's own database
  is not building a permanent historical archive — FRED itself remains the permanent historical
  source if that's ever needed later.
- **Shared-fetch architecture for raw data** (this part is unchanged from before): every unique
  indicator across every category is fetched from FMP/FRED/Marketaux **once per day**, not once
  per user — the per-user step is only the final OpenAI narrative generation, not the underlying
  data collection.

## 3. Frontend / onboarding flow

1. User signs into the app via Clerk (React Native).
2. User selects **one** category from the 7. Each category screen explains what it represents and
   who it's for before the user selects (per the design system's existing calm/one-question-per-
   screen precedent — the notification-permission interstitial in `docs/04-design-system.md` §12
   is the closest existing pattern to build from).
3. User is then asked whether they want additional, optional topics on top of their category —
   the 8 topic groups listed above.
4. Selections are stored in Supabase against the user's record: their unique ID, their one
   category, and whichever additional topics they opted into.
5. The user can change any of these anytime from a settings screen.

## 4. Provider capabilities (confirmed empirically this session — do not re-verify from docs alone)

**Marketaux** (`https://api.marketaux.com/v1/news/all`, auth via `api_token` query param):
- Free tier: **100 requests/day**, max **3 articles per request** regardless of `limit` param.
- Supports `search` (free-text keyword, works independent of any stock symbol — confirmed
  "inflation" returns general economic news with `entities: []`), `symbols`, `industries`,
  `countries`, `entity_types`, `published_after`, `sort=published_desc`.
- **Recency filtering is required** — without `published_after`/`sort`, results can be 2-5 years
  old. With them, genuinely current results came back (e.g. real July 2026 CPI/Fed commentary).
- The daily job makes **one Marketaux call per data field** (all 39 FRED indicators + all 16 FMP
  fields = up to 55 calls — see §5's corrected count), searching for articles **one day old or
  less**, to catch news specifically about that day's update to each metric. This fits inside the
  100/day budget with real headroom to spare. Some fields will legitimately return zero results on
  a given day (e.g. monthly-only releases between their release dates) — **only fields that
  returned at least one recent article get included in that day's full dataset**; fields with no
  fresh coverage are dropped for the day rather than shown stale/uncommented.

**FRED** (`https://api.stlouisfed.org/fred/`, auth via `api_key` query param):
- Genuinely free, no daily cap (generous per-minute limits only) — over 800,000 series exist;
  `/fred/series/search` is the practical way to discover series, with a `popularity` score to
  distinguish standard/well-known series from obscure variants.
- `/fred/series` gives metadata (title, units, frequency, seasonal adjustment, observation
  start/end, plain-English `notes`). `/fred/series/observations` gives the actual historical data
  points (confirmed: CPIAUCSL alone has 954 monthly observations back to 1947) — the source of
  each indicator's "latest value."

**FMP** (Milestone 12, already implemented and verified end-to-end against the live API) —
unchanged. Three functions in `backend/app/services/fmp_service.py`, returning three schemas from
`backend/app/schemas/fmp_data.py`, together making up 16 distinct data fields:

- `fetch_market_snapshot(symbols: list[str]) -> list[IndexQuote]` — **3 fields**: S&P 500 (`^GSPC`),
  Dow (`^DJI`), Nasdaq (`^IXIC`). Each `IndexQuote`: `symbol`, `name`, `price`, `change`,
  `change_percentage`.
- `fetch_sector_performance(as_of: date) -> list[SectorPerformance]` — **11 fields**, one per GICS
  sector. Each `SectorPerformance`: `sector`, `average_change`, `date`. Paired with
  `pick_best_and_worst(sectors)` to surface the day's best/worst-performing sector.
- `fetch_top_gainer_spotlight`/`fetch_top_loser_spotlight` — **2 fields**: the day's biggest
  qualifying mover in each direction, filtered to $10B+ market cap, `None` if nothing clears the
  threshold. Each `CompanySpotlight`: `symbol`, `name`, `price`, `change`, `change_percentage`,
  `market_cap`, `direction`.

3 + 11 + 2 = **16 FMP fields**, fetched once via a plain `GET` (no Marketaux/FRED involved in the
fetch itself), then each of those 16 also gets its own same-day Marketaux news search per §4
above, same as the FRED indicators.

## 5. Verified master indicator list (FRED)

Every series ID below was checked directly against the live FRED API this session
(`/fred/series?series_id=...`) — none of these are guessed.

**Correction from the first draft of this plan**: `TERMCBCCALLNS` (Credit Card Interest Rate) had
been listed twice (once under "Interest Rates," once under "Consumer Costs"). It's one indicator,
appearing in two topic groups. **The real total is 39 unique FRED indicators**, not 40.

| # | Indicator | FRED Series ID | Frequency | Topic Group |
|---|---|---|---|---|
| 1 | Consumer Price Index | `CPIAUCSL` | Monthly | Inflation |
| 2 | Core CPI | `CPILFESL` | Monthly | Inflation |
| 3 | PCE Price Index | `PCEPI` | Monthly | Inflation |
| 4 | Core PCE Price Index | `PCEPILFE` | Monthly | Inflation |
| 5 | Producer Price Index | `PPIACO` | Monthly | Inflation |
| 6 | Rent/Shelter Inflation | `CUSR0000SEHA` | Monthly | Inflation |
| 7 | Food Inflation | `CPIUFDSL` | Monthly | Inflation |
| 8 | Energy CPI | `CPIENGSL` | Monthly | Inflation |
| 9 | Nonfarm Payrolls | `PAYEMS` | Monthly | Employment & Labor |
| 10 | Unemployment Rate | `UNRATE` | Monthly | Employment & Labor |
| 11 | Initial Jobless Claims | `ICSA` | Weekly | Employment & Labor |
| 12 | Continuing Jobless Claims | `CCSA` | Weekly | Employment & Labor |
| 13 | Labor Force Participation Rate | `CIVPART` | Monthly | Employment & Labor |
| 14 | Average Hourly Earnings | `CES0500000003` | Monthly | Employment & Labor |
| 15 | JOLTS Job Openings | `JTSJOL` | Monthly | Employment & Labor |
| 16 | Gross Domestic Product | `GDP` | Quarterly | Economic Growth |
| 17 | Retail Sales | `RSAFS` | Monthly | Economic Growth |
| 18 | Industrial Production | `INDPRO` | Monthly | Economic Growth |
| 19 | Capacity Utilization | `TCU` | Monthly | Economic Growth |
| 20 | U Mich Consumer Sentiment | `UMCSENT` | Monthly | Economic Growth |
| 21 | Disposable Personal Income | `DSPI` | Monthly | Economic Growth |
| 22 | Federal Funds Rate | `FEDFUNDS` | Monthly | Interest Rates & Monetary Policy |
| 23 | Prime Rate | `MPRIME` | Monthly | Interest Rates & Monetary Policy |
| 24 | 2-Year Treasury Yield | `DGS2` | Daily | Interest Rates & Monetary Policy |
| 25 | 10-Year Treasury Yield | `DGS10` | Daily | Interest Rates & Monetary Policy |
| 26 | 30-Year Treasury Yield | `DGS30` | Daily | Interest Rates & Monetary Policy |
| 27 | Yield Curve (10Y-2Y) | `T10Y2Y` | Daily | Interest Rates & Monetary Policy |
| 28 | M2 Money Supply | `M2SL` | Monthly | Interest Rates & Monetary Policy |
| 29 | Credit Card Interest Rate | `TERMCBCCALLNS` | Monthly | Interest Rates & Monetary Policy / Consumer Costs |
| 30 | Housing Starts | `HOUST` | Monthly | Housing |
| 31 | Building Permits | `PERMIT` | Monthly | Housing |
| 32 | Existing Home Sales | `EXHOSLUSM495S` | Monthly | Housing |
| 33 | New Home Sales | `HSN1F` | Monthly | Housing |
| 34 | 30-Year Fixed Mortgage Rate | `MORTGAGE30US` | Weekly | Housing |
| 35 | 15-Year Fixed Mortgage Rate | `MORTGAGE15US` | Weekly | Housing |
| 36 | Case-Shiller Home Price Index | `CSUSHPISA` | Monthly | Housing |
| 37 | FHFA House Price Index | `USSTHPI` | Quarterly | Housing |
| 38 | Population | `POPTHM` | Monthly | Housing (population growth computed as % change, not a separate series) |
| 39 | Regular Gas Prices | `GASREGW` | Weekly | Consumer Costs |

**39 FRED indicators + 16 FMP fields = 55 total daily data items**, each getting its own same-day
Marketaux search — 55 of the 100 available daily requests, comfortable headroom remaining.

**Not available on FRED — confirmed, not included above:**
- **GDPNow** (Atlanta Fed's own model, not FRED-distributed), **NFIB Small Business Optimism
  Index** (not on FRED), **Dollar Index/DXY** (not on FRED), **ISM Manufacturing/Services PMI**
  (confirmed via live FRED search this session — zero relevant results for either; ISM data is
  proprietary/licensed). None of these are in the 39 above. If any matter enough to include later,
  they'd need a different, likely paid, data source.

## 6. Categories — indicators, financial-market content, and framing

### 1. Investors
**Main question:** Where is the economy headed, and what does that mean for financial markets and
investment portfolios?
**FRED indicators:** all of Inflation (1-5), all of Employment & Labor (9-11, 13-15), all of
Economic Growth (16-19), all of Interest Rates & Monetary Policy (22, 24-28), all of Housing
(30-33).
**Financial-market content (full package):** S&P 500, Dow, Nasdaq, all 11 sector performances,
best/worst sector, top qualifying gainer, top qualifying loser.

### 2. Small Business Owners / Entrepreneurs
**Main question:** Are business costs, consumer demand, financing conditions, and hiring
conditions improving or worsening?
**FRED indicators:** CPI, PPI, Energy CPI, Gas Prices (costs); Unemployment Rate, Initial Jobless
Claims, Labor Force Participation, Average Hourly Earnings, JOLTS (labor); GDP, Retail Sales,
Industrial Production, Capacity Utilization, U Mich Consumer Sentiment, Disposable Personal Income
(demand/activity); Federal Funds Rate, Prime Rate (financing); Housing Starts, Building Permits
(construction demand signal).
**Financial-market content:** brief S&P 500 summary, best/worst sector. **No individual company
gainer/loser by default** unless the user also opted into the Investors-style content via
additional topics.

### 3. Consumers
**Main question:** What is happening to my cost of living, income, debt, and purchasing power?
**FRED indicators:** CPI, PCE, Rent/Shelter, Food, Energy CPI, Gas Prices (cost of living);
Unemployment Rate, Initial Jobless Claims, Average Hourly Earnings, Disposable Personal Income
(income); Credit Card Interest Rate, Federal Funds Rate, Prime Rate (borrowing costs); Retail
Sales, U Mich Consumer Sentiment (consumer conditions).
**Financial-market content:** none by default. A short market summary only surfaces when there's
an unusually large/notable market move that day.

### 4. Home Owners / Home Buyers
**Main question:** Are homes becoming more affordable, and what's happening to mortgage rates,
housing supply, and property values?
**FRED indicators:** 30Y/15Y Mortgage Rate, Federal Funds Rate, 10Y Treasury Yield, Prime Rate
(financing); Case-Shiller, FHFA HPI (prices); Housing Starts, Building Permits, Existing/New Home
Sales (supply); CPI, Unemployment Rate, Average Hourly Earnings, Disposable Personal Income,
Rent/Shelter (affordability); Population (long-term demand).
**Financial-market content:** brief S&P 500 summary, Real Estate sector, Financial sector,
Consumer Discretionary sector when relevant. No individual gainer/loser by default.

### 5. Students
**Main question:** What does the economy mean for my living costs, borrowing costs, internships,
and ability to find work after graduation?
**FRED indicators:** Unemployment Rate, Initial + Continuing Jobless Claims, Labor Force
Participation, JOLTS, Average Hourly Earnings (opportunities); CPI, Rent/Shelter, Food, Energy CPI,
Gas Prices (cost of living); Credit Card Interest Rate, Federal Funds Rate (borrowing); GDP, Retail
Sales, Industrial Production, Disposable Personal Income (broader conditions).
**Financial-market content:** brief S&P 500 + Nasdaq summaries, best/worst sector — framed
explicitly as general market conditions, **not** direct evidence of hiring.

### 6. Job Seekers
**Main question:** Is hiring improving, where are opportunities emerging, and how much bargaining
power do workers have?
**FRED indicators:** Nonfarm Payrolls, Unemployment Rate, Initial + Continuing Jobless Claims,
JOLTS, Labor Force Participation, Average Hourly Earnings (hiring); GDP, Retail Sales, Industrial
Production, U Mich Consumer Sentiment (conditions); Housing Starts, Building Permits, PPI, Federal
Funds Rate (sector-specific hiring context); CPI (purchasing power).
**Financial-market content:** brief S&P 500 + Nasdaq + Dow summaries, best/worst sector — framed
as market expectations/business confidence, not a direct jobs signal.

### 7. "I Want Everything"
**Main question:** What's happening across the entire economy — inflation, employment, housing,
business activity, interest rates, and financial markets?
**FRED indicators:** all 39.
**Financial-market content:** the full package — S&P 500, Dow, Nasdaq, all 11 sectors,
best/worst sector, top gainer, top loser.

## 7. Backend daily data flow

1. **FMP fetch**: one pass through `fmp_service.py`'s existing functions → all 16 FMP fields,
   stored temporarily.
2. **Marketaux fetch**: up to 55 calls (one per FRED indicator + one per FMP field), each searching
   for articles published within the last day, to catch commentary tied to that day's update.
   Stored temporarily.
3. **Filter**: any data field (FRED or FMP) that returned **zero** recent Marketaux articles is
   dropped from that day's working dataset — only fields with fresh news coverage carry forward.
4. **Per-user generation**: for each registered user, OpenAI's nano model generates one custom
   response, built from whichever data fields are relevant to that user's category + any
   additional topics they opted into, using the filtered dataset from step 3.
5. **Cleanup**: 48 hours after the fetch, all of that day's temporary FRED/Marketaux/FMP data is
   deleted from the database.
6. **Delivery**: users get a push notification with their new econ briefing at 7:00 AM daily
   (matches the existing recommended V1 schedule in `docs/02-system-architecture.md` §23).

## 8. Database schema changes

Existing 7 tables (`briefings`, `economic_events`, `enriched_events`, `fred_series`,
`news_articles`, `device_tokens`, `job_runs`) were designed around the abandoned discrete-events
model. Proposed changes, following this codebase's existing conventions (UUID PKs via Python-side
`default=uuid.uuid4`, `TimestampMixin`, flat `ForeignKey()` columns, no ORM `relationship()`
objects anywhere, JSONB for list-like fields):

- **New `users` table**: `id` (UUID PK), `clerk_user_id` (str, unique), `email` (str), `category`
  (str — exactly one of the 7), `additional_topics: Mapped[list[str]] = mapped_column(JSONB)`
  (the optional topic-group selections), plus `TimestampMixin`. Matches this codebase's existing
  JSONB-array-for-list-data pattern (`enriched_events.affected_groups` already does this).
- **`device_tokens`**: add nullable `user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))`
  to preserve anonymous-device support while allowing linkage once signed in.
- **Replace `economic_events`/`enriched_events`/`fred_series`/`news_articles`** with **temporary,
  auto-expiring** tables (given the 48-hour deletion requirement — this is a real difference from
  a permanent historical archive):
  - `daily_data_items`: `id` (UUID), `item_key` (str — a stable slug, FRED series ID or FMP field
    name), `source` (`"fred"` or `"fmp"`), `date` (Date), `value` (float | None, for FRED-style
    single-value fields), `raw_data` (JSONB, for FMP-style multi-field records like
    `CompanySpotlight`), `fetched_at` (timestamptz). Natural key: `(item_key, date)`.
  - `daily_data_news`: `id` (UUID), `item_key` (str), `date` (Date), `headline`, `source`, `url`,
    `published_at`, `summary`, `sentiment` (float | None) — up to 3 rows per `(item_key, date)`.
  - `user_briefings` (replaces the old single global `briefings` table's role): `id` (UUID),
    `user_id` (FK), `date` (Date), `content` (the OpenAI-generated text), `fetched_at`. One row per
    user per day.
  - A scheduled cleanup job (or a Postgres-level TTL approach — decide at implementation time)
    deletes rows from all three of the above tables once `fetched_at`/`date` is more than 48 hours
    old.

## 9. Backend service architecture

New services, following the existing `fmp_service.py` conventions (plain module-level functions,
sync `httpx`, module `logger`, log-then-bare-`raise` on failure, no custom exception classes):

- `services/fred_service.py` — fetch latest value for each of the 39 series IDs.
- `services/marketaux_service.py` — one same-day news search per data item (55 calls/day total),
  handling zero-results gracefully.
- `services/openai_service.py` — **per-user** generation: takes one user's category + additional
  topics, filters the day's dataset to the relevant fields, produces one personalized response.
  Called once per registered user, not once per category.
- `services/briefing_service.py` (orchestrator) — the daily job: FMP fetch → Marketaux fetch →
  filter → loop over all registered users calling `openai_service` per user → cleanup job scheduled
  for 48 hours later.
- Auth dependency (e.g. `get_current_user`, modeled on the existing `get_db` dependency) —
  verifies a Clerk-issued token, resolves it to a `users` row.

**New `Settings` fields needed**: `clerk_secret_key`, `clerk_publishable_key`, `openai_api_key`
(already reserved in `.env.example`, not yet wired).

## 10. Mobile app changes

Current state: bare Expo Router `<Stack />`, one route (`index.tsx`), no auth libraries, no route
groups, only `button`/`card`/`badge`/`separator`/`text` UI primitives exist.

- Add `@clerk/clerk-expo` (or current equivalent), `expo-secure-store` (session persistence).
- New route structure: `app/(auth)/sign-up.tsx` + `sign-in.tsx`, an
  `app/(onboarding)/category.tsx` (single-select category screen, one explanation per category
  before picking), `app/(onboarding)/topics.tsx` (optional multi-select topic screen), a Settings
  screen for changing these later.
- New UI primitives needed: a single-select card/radio-style component for the category screen,
  and a multi-select toggle/chip component for the optional-topics screen — neither exists yet.
  The closest precedent for the chip style is the read-only "Affected Group Chips" in the design
  system, which would need to become interactive.
- Screen tone: match the existing two-button notification-permission interstitial
  (`docs/04-design-system.md` §12) — calm, one question per screen, per "Simplicity Wins."

## 11. Open items to resolve before/during implementation

- Exact current OpenAI model name for the "nano"/cheapest tier — verify against OpenAI's docs at
  implementation time, not from this planning doc.
- Whether ISM PMI / GDPNow / NFIB / DXY are worth pursuing via an alternate paid/licensed source,
  or simply left out.
- Exact Clerk backend verification approach (JWKS caching, session vs. JWT template).
- Exact cleanup mechanism for the 48-hour data expiry (scheduled job vs. Postgres-native TTL) —
  an implementation-time decision.
- Per-user OpenAI generation cost should be sanity-checked against expected user counts once real
  usage numbers exist, given cost scales directly with registered users (a deliberate tradeoff,
  but worth monitoring in practice).

## 12. Milestone breakdown (replaces old Milestones 13-24)

Numbered continuing from Milestone 12 (already complete). Each should get its own Phase 1-7
mentor-workflow pass when actually started, same as every milestone so far.

1. **M13 — User Accounts & Clerk Integration**: `users` table + migration, Clerk backend
   verification dependency, `Settings` fields, mobile Clerk SDK + sign-up/sign-in screens.
2. **M14 — Category & Topic Selection**: `category`/`additional_topics` columns, the two
   onboarding screens + new UI primitives, `GET/PUT /v1/users/me/preferences` endpoint, settings
   screen for changing preferences later.
3. **M15 — FRED Service**: `fred_service.py`, verified against the real API (per §4/§5 above).
4. **M16 — Marketaux Service**: `marketaux_service.py`, same-day recency-filtered search per data
   item.
5. **M17 — Daily Data Pipeline & Storage**: `daily_data_items`/`daily_data_news` tables +
   migrations, the fetch-and-filter steps (§7 steps 1-3), the 48-hour cleanup mechanism.
6. **M18 — Per-User OpenAI Briefing Generation**: `openai_service.py`, `user_briefings` table +
   migration, the per-user generation loop.
7. **M19 — Daily Briefing Orchestrator**: `briefing_service.py` wiring M15-18 together end to end,
   one `job_runs` row per run.
8. **M20 — Personalized Briefing API**: endpoint serving a signed-in user's own `user_briefings`
   row, replacing the old single-briefing `GET /briefings/today` design.
9. **M21 — Personalized Notifications**: `device_tokens.user_id` migration, 7:00 AM daily
   notification triggering per-user briefing delivery.
10. **M22 — Backend Integration Test Pass**: end-to-end verification of the full new pipeline.

This replaces Milestones 13-24 and touches what were Milestones 27-45 (mobile UI, notifications)
— those should be re-read and adjusted once you reach them, since they currently assume zero auth
and one global briefing throughout.
