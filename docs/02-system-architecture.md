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

Walris is a mobile-first economic intelligence application that generates a daily briefing of
the top five economic events.

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

Walris V1 does **not** include user authentication.

Users can open the app immediately after installation.

The app may request notification permission and store an anonymous device token.

```text
User installs app
  ↓
User opens app
  ↓
App loads today's briefing
  ↓
App asks for notification permission
  ↓
Expo push token is stored anonymously
```

Authentication is deferred to V2.

## 5. Data Flow: Daily Briefing Generation

A scheduled backend job runs every morning.

```text
Scheduled job starts
  ↓
Fetch today's economic calendar from Finnhub
  ↓
Normalize raw economic events
  ↓
Filter for relevant macroeconomic events
  ↓
Match events to FRED series where possible
  ↓
Fetch historical context from FRED
  ↓
Search Marketaux for related news coverage
  ↓
Send structured payload to OpenAI
  ↓
OpenAI returns enriched event summaries
  ↓
Store briefing and enriched events in Supabase
  ↓
Mobile app fetches completed briefing
```

## 6. Data Flow: App Opening

```text
User opens Walris
  ↓
Mobile app calls GET /briefings/today
  ↓
FastAPI checks Supabase for today's briefing
  ↓
If briefing exists:
    return briefing
If briefing does not exist:
    return empty/loading state
  ↓
Mobile app renders daily briefing
```

The app should not generate a briefing on demand for each user.

Daily briefings are pre-generated and cached.

## 7. Data Flow: Event Detail Page

```text
User taps event card
  ↓
Mobile app calls GET /events/{event_id}
  ↓
FastAPI retrieves:
    event data
    enriched summary
    FRED context
    related news articles
  ↓
Mobile app renders detail screen
```

## 8. Notification Architecture

Walris uses Expo Push Notifications.

```text
User grants notification permission
  ↓
Expo returns push token
  ↓
Mobile app sends token to FastAPI
  ↓
FastAPI stores token in Supabase
  ↓
Morning briefing job completes
  ↓
Notification job sends push notification
  ↓
User taps notification
  ↓
App opens today's briefing
```

Default notification copy:

> View this morning's top 5 economic events.

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

- Orchestrating the full daily briefing pipeline
- Selecting top 5 events
- Storing final results
- Serving completed briefings

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

### `briefings`

Stores daily briefing-level content.

```text
id
briefing_date
title
summary
status
created_at
updated_at
```

### `economic_events`

Stores normalized economic event data from Finnhub.

```text
id
briefing_id
external_event_id
event_name
country
release_time
actual_value
forecast_value
previous_value
unit
source
created_at
updated_at
```

### `enriched_events`

Stores AI-generated summaries and rankings.

```text
id
event_id
importance_score
importance_reason
plain_english_summary
historical_context_summary
news_context_summary
affected_groups
created_at
updated_at
```

### `fred_series`

Stores historical context for events.

```text
id
event_id
series_id
series_name
latest_value
previous_value
ten_year_average
historical_percentile
trend_direction
data_points
created_at
updated_at
```

### `news_articles`

Stores Marketaux article metadata.

```text
id
event_id
headline
source
url
published_at
summary
sentiment
entities
topics
created_at
updated_at
```

### `device_tokens`

Stores anonymous Expo push tokens.

```text
id
expo_push_token
device_id
platform
timezone
is_active
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

### Home Screen

Displays:

- App name
- Date
- Daily briefing title
- Daily summary
- Top 5 event cards

### Event Detail Screen

Displays:

- Event name
- Country
- Release time
- Actual / forecast / previous
- Importance score
- Plain-English summary
- Historical context
- News context
- Affected groups
- Related articles

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

## 21. Caching Strategy

Supabase acts as the primary content cache.

Walris should not call external APIs every time the app opens.

Caching rules:

- Daily briefing: generated once per day
- Economic events: stored once per briefing
- FRED historical data: refreshed daily for relevant events
- Marketaux news: refreshed during briefing generation
- OpenAI summaries: generated once per briefing

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

Since V1 has no authentication, no private user data should be stored except anonymous device
notification tokens.

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

## 29. Future V2 Architecture

When personalization is added, introduce authentication.

Likely V2 additions:

- Clerk authentication
- user profiles
- saved interests
- bookmarked events
- personalized notifications
- custom watchlists
- premium subscription layer

Future authenticated architecture:

```text
React Native
  ↓
Clerk Auth
  ↓
FastAPI
  ↓
Supabase with user-linked records
```

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

The central architectural decision is that Walris pre-generates a daily briefing instead of
generating content live for each user.

This keeps the app:

- Faster
- Cheaper
- Easier to debug
- Easier to scale
- More reliable

The V1 system should prove one thing:

> Users want to open Walris every morning because it is the fastest way to understand what
> matters in the economy.
