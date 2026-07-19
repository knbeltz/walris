# Walris System Architecture

**Document:** 02-system-architecture.md
**Version:** 1.0
**Status:** Draft
**Platform:** iOS & Android
**Frontend:** React Native + Expo
**Backend:** FastAPI
**Database:** Supabase PostgreSQL

---

## 1. Architecture Overview

Walris is a mobile-first economic intelligence application that generates a daily briefing
personalized to each user's selected category (Investors, Small Business Owners/Entrepreneurs,
Consumers, Home Owners/Home Buyers, Students, Job Seekers, or "I Want Everything") and optional
additional topics. See `docs/09-personalization-pivot-plan.md` for the full plan.

The system has four major layers:

```text
Mobile App
  ↓
FastAPI Backend
  ↓
Supabase PostgreSQL
  ↓
External Data + AI APIs
```

External APIs:

- **FMP (Financial Modeling Prep)** — market data (index quotes, sector performance, notable movers)
- **FRED** — historical economic data
- **Marketaux** — contextual financial news
- **OpenAI** — event ranking, summaries, synthesis

## 2. High-Level Architecture

```text
React Native / Expo App
  ↓
FastAPI REST API
  ↓
Supabase PostgreSQL
  ↓
Data Processing Services
  ↓
FMP + FRED + Marketaux + OpenAI
```

The mobile app should never call FMP, FRED, Marketaux, or OpenAI directly.

All external API logic belongs in the backend.

## 3. Core Architecture Principle

Walris should separate responsibilities clearly:

**Mobile App** — Displays the briefing.

**FastAPI** — Processes data and serves API responses.

**Supabase** — Stores briefings, events, news, historical context, and device tokens.

**External APIs** — Provide raw source data.

**OpenAI** — Explains and synthesizes retrieved data.

OpenAI should never be treated as the source of truth.

## 4. V1 Authentication Architecture

Walris V1 **includes** user authentication via Clerk — a deliberate change from this project's
original plan (which deferred auth to V2). Personalized, per-category briefings require knowing
who the user is; a local/anonymous preference isn't sufficient once briefings are individually
generated per account. See `docs/09-personalization-pivot-plan.md` §2 for the full reasoning.

```text
User installs app
  ↓
User signs up / signs in via Clerk
  ↓
User selects one category (+ optional additional topics)
  ↓
Selections stored in Supabase, linked to the user's account
  ↓
App asks for notification permission
  ↓
Expo push token is stored, linked to the user's account
  ↓
App loads the user's personalized briefing
```

Users can change their category/topic selections anytime from a settings screen.

## 5. Data Flow: Daily Briefing Generation

A scheduled backend job runs every morning. Full detail in
`docs/09-personalization-pivot-plan.md` §7-9.

```text
Scheduled job starts
  ↓
Fetch all 16 FMP fields (index quotes, sector performance, company spotlights)
  ↓
Fetch latest values for all 39 FRED indicators
  ↓
Search Marketaux for same-day news, once per data field (up to 55 calls)
  ↓
Drop any data field with zero recent news coverage from today's working dataset
  ↓
For each registered user:
    filter the dataset to their category + additional topics
    send to OpenAI, generate their individual briefing
    store as a user_briefings row
  ↓
Schedule deletion of today's raw FRED/Marketaux/FMP data 48 hours from now
```

## 6. Data Flow: App Opening

```text
User opens Walris (signed in via Clerk)
  ↓
Mobile app calls GET /v1/briefings/today (authenticated)
  ↓
FastAPI checks Supabase for today's user_briefings row for this user
  ↓
If briefing exists:
    return briefing
If briefing does not exist yet:
    return empty/loading state
  ↓
Mobile app renders the user's personalized briefing
```

The app should not generate a briefing on demand for each user.

Daily briefings are pre-generated and cached.

## 7. Data Flow: Event Detail Page (obsolete)

This flow assumed discrete, individually-addressable "events" (Finnhub calendar entries). The
personalization pivot has no equivalent concept — a user's briefing is one personalized narrative
per day, not a list of drill-down-able events. No replacement screen/endpoint is currently
planned; revisit only if a future version reintroduces some form of individually-linkable content
within a briefing.

## 8. Notification Architecture

Walris uses Expo Push Notifications.

```text
User grants notification permission
  ↓
Expo returns push token
  ↓
Mobile app sends token to FastAPI, linked to the signed-in user
  ↓
FastAPI stores token in Supabase (device_tokens.user_id)
  ↓
Per-user briefing generation completes for this user
  ↓
Notification job sends this user's push notification
  ↓
User taps notification
  ↓
App opens the user's personalized briefing
```

Notification copy is no longer a single hardcoded string for everyone — it should reflect the
user's category (e.g. referencing their specific briefing content), not a generic "top 5 events"
line. Exact copy per category is a mobile/notification-milestone implementation detail.

## 9. Main Backend Services

The FastAPI backend should be organized around services.

```text
services/
  fmp_service.py
  fred_service.py
  marketaux_service.py
  openai_service.py
  briefing_service.py
  notification_service.py
```

### FMP Service

Responsible for:

- Fetching a market snapshot (index quotes, e.g. S&P 500)
- Fetching sector performance and identifying the best/worst performing sector
- Fetching a Company Spotlight: pulling biggest gainers/losers, filtering by market cap, and
  selecting the top qualifying mover
- Normalizing raw FMP fields into typed objects
- Handling FMP API errors

### FRED Service

Responsible for:

- Mapping events to FRED series IDs
- Fetching historical observations
- Computing basic context
- Returning historical summaries

### Marketaux Service

Responsible for:

- Searching related news
- Filtering low-relevance articles
- Normalizing article metadata
- Returning top articles per event

### OpenAI Service

Responsible for:

- Ranking events
- Generating explanations
- Summarizing historical context
- Summarizing news coverage
- Producing structured JSON output

### Briefing Service

Responsible for:

- Orchestrating the full daily pipeline (FMP + FRED fetch, Marketaux news, per-user OpenAI
  generation)
- Filtering the shared dataset per user by category + additional topics
- Storing each user's generated briefing
- Serving each user their own completed briefing

### Notification Service

Responsible for:

- Storing Expo push tokens
- Sending daily notifications
- Handling failed tokens

## 10. Backend API Surface

Minimum V1 endpoints:

```text
GET  /health
GET  /briefings/today
GET  /briefings/{date}
GET  /events/{event_id}
POST /notifications/register
POST /admin/generate-briefing
```

### `GET /health`

Checks backend health.

### `GET /briefings/today`

Returns today's full briefing.

### `GET /briefings/{date}`

Returns a briefing for a specific date.

### `GET /events/{event_id}`

Returns full event detail.

### `POST /notifications/register`

Stores anonymous Expo push notification token.

### `POST /admin/generate-briefing`

Manually triggers briefing generation during development.

This endpoint should be protected by an admin secret.

## 11. Database Architecture

Supabase PostgreSQL is used as the central database and content cache.

Core tables:

```text
briefings
economic_events
enriched_events
fred_series
news_articles
device_tokens
job_runs
```

### Relationship Model

```text
briefings
  ↓
economic_events
  ↓
enriched_events

economic_events
  ↓
fred_series

economic_events
  ↓
news_articles
```

## 12. Suggested Database Tables

Superseded by the personalization pivot — see `docs/09-personalization-pivot-plan.md` §8 for the
authoritative, up-to-date schema design and reasoning. Summary:

### `users` (new)

```text
id
clerk_user_id
email
category
additional_topics       (JSONB array)
created_at
updated_at
```

### `daily_data_items` (replaces `economic_events`/`fred_series`)

Temporary — deleted 48 hours after `fetched_at`, not a permanent historical archive.

```text
id
item_key                (stable slug: FRED series ID or FMP field name)
source                  ("fred" or "fmp")
date
value                   (nullable, single-value FRED-style fields)
raw_data                (JSONB, multi-field FMP-style records)
fetched_at
```

### `daily_data_news` (replaces `news_articles`)

Temporary — same 48-hour deletion as `daily_data_items`.

```text
id
item_key
date
headline
source
url
published_at
summary
sentiment
```

### `user_briefings` (replaces the global `briefings`/`enriched_events` tables)

One row per user per day — the individually-generated OpenAI output.

```text
id
user_id
date
content
fetched_at
```

### `device_tokens` (modified — now linked to a user)

```text
id
expo_push_token
device_id
platform
timezone
is_active
user_id                 (nullable — preserves anonymous-device support)
created_at
updated_at
```

### `job_runs`

Tracks scheduled job execution.

```text
id
job_name
status
started_at
finished_at
error_message
metadata
created_at
```

## 13. Frontend Architecture

The mobile app should be organized around screens, reusable components, API hooks, and theme
tokens.

Suggested structure:

```text
mobile/
  app/
    index.tsx
    event/[id].tsx
  components/
    briefing/
    events/
    news/
    ui/
  hooks/
    useTodayBriefing.ts
    useEventDetail.ts
    useRegisterPushToken.ts
  lib/
    api.ts
    queryClient.ts
    validation.ts
  theme/
    colors.ts
    typography.ts
    spacing.ts
```

## 14. Frontend Screens

Updated for the personalization pivot — see `docs/09-personalization-pivot-plan.md` §3/§10 for
full detail.

### Sign-Up / Sign-In Screens (new)

Clerk-based authentication.

### Category Selection Screen (new)

Single-select from the 7 categories, each explained before the user picks.

### Additional Topics Screen (new)

Optional multi-select from the 8 topic groups, layered on top of the chosen category.

### Home Screen

Displays:

- App name
- Date
- The signed-in user's personalized daily briefing content

### Event Detail Screen — obsolete

Removed under this pivot; no discrete events exist to drill into (see §7).

### Settings Screen (new)

Lets the user change their category and additional topics anytime.

### Empty State

Shown when no briefing exists.

### Error State

Shown when backend request fails.

### Loading State

Shown while fetching data.

## 15. State Management

Use TanStack Query for server state.

TanStack Query should handle:

- Fetching briefings
- Fetching event details
- Loading states
- Error states
- Refetching
- Caching

Avoid global state unless necessary.

## 16. Type Safety Architecture

Type safety is required across the stack.

**Frontend:**

- TypeScript
- Zod response validation
- Generated Supabase types
- Strict mode enabled

**Backend:**

- Python type hints
- Pydantic request/response schemas
- SQLAlchemy models
- No untyped service returns

Data contracts should be validated at API boundaries.

## 17. API Validation Flow

```text
FastAPI returns JSON
  ↓
React Native receives response
  ↓
Zod validates response shape
  ↓
Typed data enters UI components
```

If validation fails, the app should show a controlled error state.

## 18. OpenAI Architecture

OpenAI receives structured data, not raw unbounded text.

Input should include:

```text
event metadata
actual / forecast / previous
FRED historical context
Marketaux news summaries
source URLs
```

OpenAI returns structured JSON:

```text
importance_score
importance_reason
plain_english_summary
historical_context_summary
news_context_summary
affected_groups
```

The backend must validate OpenAI output before storing it.

## 19. Hallucination Prevention

Walris should enforce these rules:

- OpenAI cannot invent actual economic values.
- OpenAI cannot cite sources not provided.
- OpenAI cannot make investment recommendations.
- OpenAI cannot claim certainty about future events.
- OpenAI must communicate uncertainty when appropriate.

If OpenAI output fails validation, the backend should retry once or store a fallback summary.

## 20. External API Strategy

The backend should isolate each external provider behind a service class or module.

This prevents vendor-specific logic from spreading across the codebase.

```text
FMP raw response
  ↓
FMPService
  ↓
Normalized market data (IndexQuote / SectorPerformance / CompanySpotlight)
```

All external API responses should be normalized before being stored or sent to OpenAI.

## 21. Caching / Retention Strategy

Supabase acts as the primary content cache, but retention is now temporary, not permanent — see
`docs/09-personalization-pivot-plan.md` §2/§8.

Walris should not call external APIs every time the app opens.

Rules:

- Raw FMP/FRED/Marketaux data: fetched once per day (shared across all users), deleted 48 hours
  after fetch
- Each user's briefing: generated once per day (per user, via OpenAI), deleted alongside the raw
  data it was built from
- No permanent historical archive is maintained in Walris's own database — FRED itself remains
  the durable historical source if ever needed again later

## 22. Error Handling Strategy

The system should degrade gracefully.

**FMP Failure** — Return previous available briefing or show no-briefing state.

**FRED Failure** — Generate event without historical context.

**Marketaux Failure** — Generate event without news context.

**OpenAI Failure** — Store raw event data and fallback summary.

**Supabase Failure** — Return backend error.

**Notification Failure** — Log failure and mark token inactive if needed.

## 23. Scheduled Jobs

Walris needs at least two scheduled jobs.

**Daily Briefing Job** — Runs every morning. Responsible for generating the daily briefing.

**Notification Job** — Runs after successful briefing generation. Responsible for sending push
notifications.

Recommended V1 schedule:

- Daily briefing generation: 6:00 AM ET
- Push notification: 7:00 AM ET

## 24. Deployment Architecture

Recommended V1 deployment:

**Mobile App:** Expo Application Services

**Backend:** Render, Railway, or Fly.io

**Database:** Supabase

**Scheduled Jobs:** Backend scheduler or hosted cron

**Push Notifications:** Expo Notifications

**External APIs:** FMP, FRED, Marketaux, OpenAI

## 25. Environment Variables

Backend environment variables:

```text
DATABASE_URL
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
FMP_API_KEY
FRED_API_KEY
MARKETAUX_API_KEY
OPENAI_API_KEY
ADMIN_SECRET
EXPO_ACCESS_TOKEN
ENVIRONMENT
```

Mobile environment variables:

```text
EXPO_PUBLIC_API_BASE_URL
```

Never expose external API keys in the mobile app.

## 26. Security Principles

V1 security requirements:

- External API keys only live on backend
- Admin endpoints require secret protection
- Inputs are validated with Pydantic
- Database writes happen through backend
- No secrets committed to GitHub
- HTTPS required in production

V1 now includes authentication (Clerk), so this needs revisiting from the original no-auth
assumption: user identity/session verification happens via Clerk-issued tokens (never re-implement
password/session handling locally); the backend stores real private user data (email, category
preference) which must be protected accordingly (never logged in plaintext, access scoped to the
owning user's own records only); device tokens now link to a user account (nullable, preserving
anonymous-device support) rather than being fully anonymous by design.

## 27. Performance Requirements

Target performance:

- Home briefing load: under 2 seconds
- Event detail load: under 2 seconds
- Cold app open: under 3 seconds
- Backend health check: under 300ms
- Briefing generation: under 5 minutes

The app should feel fast because data is pre-generated.

## 28. Observability

Backend should log:

- briefing job start/end
- external API failures
- OpenAI validation failures
- notification send results
- database errors
- request errors

Use a `job_runs` table to track scheduled job health.

## 29. V1 Authenticated Architecture (pulled forward from the original V2 plan)

This section originally described V2. Clerk authentication, user profiles, and personalized
content are now V1 (see §4 and `docs/09-personalization-pivot-plan.md`), because per-category
briefings require knowing who the user is.

```text
React Native
  ↓
Clerk Auth
  ↓
FastAPI
  ↓
Supabase with user-linked records
```

Still genuinely deferred to V2 or later: bookmarked events (no discrete events exist anymore
under this pivot — see §7), custom watchlists, and a premium subscription layer.

## 30. Summary

Walris V1 should be architected as a simple but professional system:

```text
Expo mobile app
  ↓
FastAPI backend
  ↓
Supabase database/cache
  ↓
FMP + FRED + Marketaux + OpenAI
  ↓
Expo push notifications
```

The central architectural decision is that Walris pre-generates each day's briefings ahead of
time — individually, per registered user, in a scheduled batch job — rather than generating
content live/on-demand when a user opens the app. Personalization does not mean per-request
generation; it means the daily batch job now produces one output per user instead of one shared
output for everyone.

This keeps the app:

- Faster
- Cheaper
- Easier to debug
- Easier to scale
- More reliable

The V1 system should prove one thing:

> Users want to open Walris every morning because it is the fastest way to understand what
> matters in the economy.
