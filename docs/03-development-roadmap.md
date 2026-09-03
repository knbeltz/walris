# Walris Development Roadmap

**Document:** docs/03-development-roadmap.md
**Version:** 1.0
**Phase:** Part 1 – Foundation

---

## Purpose

This roadmap defines the order in which Walris should be built.

Each milestone should produce a working, testable increment of the application while minimizing
technical debt.

Every milestone follows the same structure:

- Objective
- Why it matters
- Deliverables
- Files to create or modify
- Acceptance Criteria
- Definition of Done
- Suggested Git Commit
- Claude Code Tutor Prompt

**Important Principle**

Do **not** skip milestones.

Every milestone builds upon previous work.

---

## Milestone 1 — Repository & Project Setup

### Objective

Create the initial project structure and initialize version control.

### Why

A clean project structure from the beginning prevents architectural drift as the project grows.

### Deliverables

Create:

```text
walris/
  mobile/
  backend/
  docs/
  README.md
  .gitignore
```

Initialize:

- Git repository
- GitHub repository
- Python virtual environment
- Node project
- Initial README

### Acceptance Criteria

- Repository successfully pushed to GitHub
- Mobile and backend folders exist
- Project builds without errors
- README includes project description

### Definition of Done

A new contributor can clone the repository and understand the overall project layout.

### Suggested Commit

`chore: initialize Walris repository`

### Claude Code Tutor Prompt

> Help me create the initial repository structure for Walris. Do not generate unnecessary code.
> Explain why each directory exists and follow professional software engineering conventions.

---

## Milestone 2 — Documentation Foundation

### Objective

Create the documentation structure.

### Deliverables

Create:

```text
docs/
  01-product-requirements.md
  02-system-architecture.md
  03-development-roadmap.md
  04-design-system.md
  05-engineering-journal.md
```

### Acceptance Criteria

Documentation folder committed.

### Definition of Done

Project documentation exists in version control.

### Suggested Commit

`docs: add project documentation structure`

### Claude Code Tutor Prompt

> Help me organize the documentation structure for a production-ready software project. Explain
> the purpose of each document.

---

## Milestone 3 — Backend Foundation

### Objective

Scaffold the FastAPI application.

### Deliverables

Create:

```text
backend/
  app/
    main.py
    core/
    routers/
    services/
    schemas/
    models/
    utils/
```

Implement:

- FastAPI app
- Health endpoint
- Environment configuration
- Logging
- Dependency management

### Acceptance Criteria

Running:

```bash
uvicorn app.main:app --reload
```

starts successfully.

Health endpoint returns HTTP 200.

### Definition of Done

Backend can start locally.

### Suggested Commit

`feat: scaffold FastAPI backend`

### Claude Code Tutor Prompt

> Walk me through creating a production-ready FastAPI project structure. Explain why each folder
> exists before we write any business logic.

---

## Milestone 4 — React Native Foundation

### Objective

Initialize the mobile application.

### Deliverables

Create Expo project using TypeScript.

Install:

- Expo Router
- NativeWind
- React Native Reusables
- TanStack Query

Implement:

- Home screen
- Navigation foundation
- Theme configuration

### Acceptance Criteria

Application launches on simulator.

### Definition of Done

Blank application opens successfully.

### Suggested Commit

`feat: initialize React Native application`

### Claude Code Tutor Prompt

> Help me scaffold a production-ready React Native + Expo application using TypeScript. Explain
> every dependency before installing it.

---

## Milestone 5 — Development Environment

### Objective

Standardize the local development environment.

### Deliverables

Backend:

- Ruff
- Black
- mypy

Frontend:

- ESLint
- Prettier
- TypeScript strict mode

Create `.env.example` for backend.

Create `.env.local.example` for mobile.

### Acceptance Criteria

Formatting and linting run without errors.

### Definition of Done

Entire project follows consistent formatting.

### Suggested Commit

`chore: configure development tooling`

### Claude Code Tutor Prompt

> Help me configure linting, formatting, and static analysis for both Python and React Native.
> Explain why each tool is important.

---

## Milestone 6 — Supabase Setup

### Objective

Create the project database.

### Deliverables

Create Supabase project.

Configure local connection.

Create migration system.

Create initial tables:

- briefings
- economic_events
- enriched_events
- fred_series
- news_articles
- device_tokens
- job_runs

### Acceptance Criteria

Backend connects successfully.

### Definition of Done

Database reachable from FastAPI.

### Suggested Commit

`feat: configure Supabase database`

### Claude Code Tutor Prompt

> Help me set up Supabase for Walris. Explain why PostgreSQL is the correct database for this
> application and walk me through creating the initial schema.

---

## Milestone 7 — Configuration System

### Objective

Centralize application configuration.

### Deliverables

Create configuration module.

Store:

- API keys
- Database URL
- Environment
- Secrets

using environment variables.

Implement configuration validation using Pydantic.

### Acceptance Criteria

Application fails gracefully when required variables are missing.

### Definition of Done

No secrets are hardcoded.

### Suggested Commit

`feat: implement configuration management`

### Claude Code Tutor Prompt

> Help me build a configuration system using Pydantic Settings. Explain how configuration
> management works in production environments.

---

## Milestone 8 — Continuous Integration

### Objective

Automate code quality.

### Deliverables

Configure GitHub Actions.

Checks:

Backend

- Ruff
- Black
- mypy

Frontend

- ESLint
- TypeScript

Run on every pull request.

### Acceptance Criteria

Pipeline passes.

### Definition of Done

Pull requests automatically validate code quality.

### Suggested Commit

`ci: add GitHub Actions workflow`

### Claude Code Tutor Prompt

> Help me build a CI pipeline for Walris. Explain what should run automatically before code is
> merged.

---

## Milestone 9 — API Foundation

### Objective

Create reusable backend infrastructure.

### Deliverables

Implement:

- API versioning
- Error responses
- Response models
- Logging middleware
- Request validation
- Global exception handling

### Acceptance Criteria

All endpoints return standardized responses.

### Definition of Done

Backend infrastructure is production-ready.

### Suggested Commit

`feat: build API infrastructure`

### Claude Code Tutor Prompt

> Help me design a clean REST API architecture using FastAPI. Explain best practices for response
> models, validation, middleware, and exception handling.

---

## Milestone 10 — First End-to-End Connection

### Objective

Verify that the mobile application communicates successfully with the backend.

### Deliverables

Implement:

Backend: `GET /health`

Frontend: Call the endpoint using TanStack Query.

Display:

```text
Backend Connected
Status: Healthy
```

Handle:

- Loading state
- Error state
- Success state

### Acceptance Criteria

React Native successfully communicates with FastAPI.

### Definition of Done

The complete request/response pipeline is working.

At this point:

- Mobile app works.
- Backend works.
- Database works.
- CI works.
- Documentation exists.

The project is now ready for real feature development.

### Suggested Commit

`feat: connect mobile app to backend`

### Claude Code Tutor Prompt

> Help me connect the React Native frontend to the FastAPI backend using TanStack Query. I want to
> understand every step of the networking process instead of just copying code.

---

## Foundation Phase Complete

After Milestone 10, Walris will have:

- Professional repository structure
- FastAPI backend
- React Native mobile app
- Supabase database
- CI/CD pipeline
- Configuration management
- Logging
- Type safety
- API foundation
- Mobile ↔ Backend communication

No business logic has been implemented yet.

This is intentional.

The foundation phase exists to ensure future development happens on a stable, maintainable
architecture.

The next phase, **Core Backend**, begins implementing Walris's actual functionality, starting
with database models and integrating Finnhub to fetch today's economic events.

---

# Walris Development Roadmap

**Document:** docs/03-development-roadmap.md
**Version:** 1.0
**Phase:** Part 2 – Core Backend

---

## Part 2 Overview

Part 2 builds the core backend functionality that powers Walris.

By the end of this phase, the backend should be able to:

- Fetch economic calendar events from Finnhub
- Store normalized events in Supabase
- Fetch historical context from FRED
- Fetch related news from Marketaux
- Generate AI-enriched summaries with OpenAI
- Store a complete daily briefing
- Serve the briefing through an API endpoint

---

## Milestone 11 — Database Models & Migrations

### Objective

Create the backend database models and migrations for Walris core data.

### Deliverables

Implement models for:

```text
briefings
economic_events
enriched_events
fred_series
news_articles
device_tokens
job_runs
```

Create Alembic migrations.

### Acceptance Criteria

- Tables exist in Supabase.
- Backend can create and query records.
- Migration runs successfully from a clean database.

### Definition of Done

Database schema is ready for the core briefing pipeline.

### Suggested Commit

`feat: add core database models and migrations`

### Claude Code Tutor Prompt

> Help me implement SQLAlchemy models and Alembic migrations for Walris. Explain each
> relationship and why the schema is structured this way.

---

## Milestone 12 — FMP Market Data Service

### Objective

Create the service responsible for fetching daily market data: an index market snapshot, sector
performance, and a market-cap-filtered "Company Spotlight" mover of the day.

### Why

Originally scoped around Finnhub's economic calendar. Finnhub's calendar endpoint turned out to
require a paid plan ($50/month), and Financial Modeling Prep's (FMP) equivalent calendar
endpoints are either paid or fully retired — no viable free calendar-style data source was found
across either provider. Pivoted to FMP's free-tier market-data endpoints instead, reframing the
daily briefing's data layer around market snapshot + sector performance + a notable large-cap
mover, rather than a calendar of scheduled economic releases.

### Deliverables

Create:

```text
services/fmp_service.py
schemas/market_data.py
```

Service should:

- Fetch an index market snapshot (e.g. S&P 500) via FMP's `/stable/quote`
- Fetch sector performance via FMP's `/stable/sector-performance-snapshot`, identifying the
  best- and worst-performing sector of the day
- Fetch a Company Spotlight: pull FMP's `/stable/biggest-gainers` and `/stable/biggest-losers`,
  filter by market cap (via `/stable/profile`, threshold $10B+) to exclude small/obscure
  companies, and select the top qualifying gainer/loser
- Normalize all raw FMP fields into typed schema objects (`IndexQuote`, `SectorPerformance`,
  `CompanySpotlight`)
- Handle failed requests: log clearly, let exceptions propagate (no silent fallback to an empty
  result)

### Acceptance Criteria

- Service returns normalized market snapshot, sector performance, and company spotlight data.
- No raw FMP response leaks into the rest of the app.
- Errors are logged clearly.

### Definition of Done

Backend can retrieve today's market snapshot, sector movers, and a market-cap-filtered company
spotlight.

### Suggested Commit

`feat: integrate FMP market data (snapshot, sector movers, company spotlight)`

### Claude Code Tutor Prompt

> Help me build the FMP market data service for Walris. I want to understand how to isolate
> external API logic behind a clean service layer.

---

## Milestones 13–22 — Personalization Pivot

**Replaces the original Milestones 13-24** (which were built around Finnhub's abandoned discrete
economic-events calendar). Full plan, reasoning, verified FRED series IDs, and category/indicator
mapping: `docs/08-personalization-pivot-plan.md`. Summary of each milestone below; expand each
into full Objective/Deliverables/Acceptance-Criteria detail when it's actually started, same
mentor workflow as every prior milestone.

### Milestone 13 — User Accounts & Clerk Integration

`users` table + migration, Clerk backend token-verification dependency, new `Settings` fields
(`clerk_secret_key`, `clerk_publishable_key`), mobile Clerk SDK + sign-up/sign-in screens.

### Milestone 14 — Category & Topic Selection

`category`/`additional_topics` columns on `users`, the category-selection and additional-topics
onboarding screens (new single-select and multi-select UI primitives needed),
`GET/PUT /v1/users/me/preferences` endpoint, a settings screen for changing these later.

### Milestone 15 — FRED Service

`services/fred_service.py` — fetch latest values for the 39 verified indicators in
`docs/08-personalization-pivot-plan.md` §5.

### Milestone 16 — Marketaux Service

`services/marketaux_service.py` — one same-day recency-filtered search per data field (up to 55
calls/day across all 39 FRED indicators + 16 FMP fields), gracefully handling zero-result days.

### Milestone 17 — Daily Data Pipeline & Storage

`daily_data_items`/`daily_data_news` tables + migrations, the fetch-and-filter steps (FMP fetch →
FRED fetch → Marketaux fetch → drop fields with no fresh coverage), and the 48-hour deletion
mechanism for this temporary data.

### Milestone 18 — Per-User OpenAI Briefing Generation

`services/openai_service.py`, `user_briefings` table + migration — one OpenAI call per registered
user, filtering the day's dataset to that user's category + additional topics.

### Milestone 19 — Daily Briefing Orchestrator

`services/briefing_service.py` wiring Milestones 15-18 (plus Milestone 12's existing
`fmp_service.py`) together end to end; one `job_runs` row per run.

### Milestone 20 — Personalized Briefing API

Endpoint serving a signed-in user's own `user_briefings` row for today, replacing the old
single-briefing `GET /briefings/today` design (now authenticated, per-user).

### Milestone 21 — Personalized Notifications

`device_tokens.user_id` migration, notification copy that reflects the user's own briefing
content instead of a single hardcoded string.

### Milestone 22 — Backend Integration Test Pass

End-to-end verification of the full new pipeline (equivalent to the original roadmap's old
Milestone 26).

---

## Milestone 23 — Scheduled Personalization Job

### Objective

Automate the daily pipeline (Milestones 15-19) so it runs without manual intervention, generating
every registered user's personalized briefing automatically.

### Deliverables

Implement scheduled job using APScheduler, or hosted cron calling an admin-triggered endpoint that
runs the full `briefing_service.py` orchestration (FMP + FRED + Marketaux fetch, per-user OpenAI
generation, notification dispatch, and scheduling the 48-hour data cleanup).

Recommended schedule: pipeline completes well before 7:00 AM daily notification delivery
(`docs/02-system-architecture.md` §23).

### Acceptance Criteria

- The job runs automatically and produces a `user_briefings` row for every registered user.
- Job execution is logged, visible in `job_runs`.
- A failure generating one user's briefing doesn't block the rest.
- Manual trigger still works for testing.

### Definition of Done

Walris can generate every user's personalized daily briefing without manual intervention.

### Suggested Commit

`feat: schedule daily personalization pipeline`

### Claude Code Tutor Prompt

> Help me schedule the daily personalization pipeline. Explain how to keep one user's failure from
> blocking everyone else's briefing generation.

---

## Core Backend Phase Complete

After Milestone 23 (of the personalization pivot — see `docs/08-personalization-pivot-plan.md`),
Walris will have:

- Supabase schema including user accounts and preferences
- Clerk authentication
- FMP market data (Milestone 12)
- FRED historical indicators
- Marketaux news context
- Per-user OpenAI briefing generation
- Personalized briefing API
- Personalized notifications
- Scheduled, automated daily pipeline
- End-to-end backend validation

At this point, Walris has its core personalized intelligence engine.

The next phase should focus on building the mobile app experience that consumes this backend —
Part 3 (Milestones 24-34) and Part 4 (Milestones 35-50) have both now been re-scoped against this
pivot; see those sections below. No outstanding stale-milestone caveats remain in this document.

---

# Walris Development Roadmap

**Document:** docs/03-development-roadmap.md
**Version:** 1.0
**Phase:** Part 3 – Mobile App (Personalization Pivot)

---

## Part 3 Overview

**Replaces the original Milestones 27-40** (scoped around a shared "top 5 events" list with
individual event detail pages — abandoned along with the rest of the pre-pivot event model).
Renumbered from 24 to close the gap left by the Part 2 pivot (`docs/03` §"Milestones 13–22", which
replaced the old 12-milestone event pipeline with 11 milestones, 13-23). Full basis:
`docs/02-system-architecture.md` §13/14, `docs/08-personalization-pivot-plan.md` §3/§10. Expand
each into full Objective/Deliverables/Acceptance-Criteria detail when it's actually started, same
mentor workflow as every prior milestone.

By the end of this phase, the React Native app should be able to:

- Authenticate every backend request with the signed-in user's Clerk session token
- Fetch and render the signed-in user's personalized daily briefing: the AI-generated narrative,
  supporting key-indicator chart(s), and supporting news links — replacing the old shared "top 5
  events" list and its per-event detail page
- Render loading, empty, and error states
- Apply the Walris design system
- Validate backend API responses with Zod
- Feel polished enough for early beta testing

Part 4 (Milestones 35-50: notifications, QA, deployment, launch) has also been re-scoped against
this pivot — see that section below. No outstanding stale-milestone caveats remain in this
document.

---

## Milestone 24 — Mobile API Client

### Objective

Give the mobile app one shared, authenticated fetch wrapper instead of each screen hand-rolling its
own `fetch` call — same shape as the original Milestone 27, plus one addition the personalization
pivot requires: nearly every endpoint is now per-user, so authenticated requests need the
signed-in user's Clerk session token attached as an `Authorization: Bearer` header.

### Deliverables

A base API client (e.g. `mobile/lib/apiClient.ts`) that:

- Reads `EXPO_PUBLIC_API_BASE_URL` once, in one place, instead of every call site checking
  `process.env.EXPO_PUBLIC_API_BASE_URL` itself (as `(onboarding)/category.tsx` and
  `(onboarding)/topics.tsx` currently do).
- Accepts a Clerk `getToken()` result (from `useAuth()`, `@clerk/expo`) and attaches it as
  `Authorization: Bearer <token>` for endpoints that need it — every `/v1/users/me/*` and
  `/v1/notifications/*` route, per `backend/app/routers/__init__.py`. `GET /health` stays
  unauthenticated.
- Applies a request timeout (`AbortController`) so a hung backend doesn't hang the UI forever.
- Normalizes non-OK responses into a single thrown error shape the caller can branch on, replacing
  the ad hoc `if (!response.ok) throw new Error(...)` repeated per call site.
- Holds no external API keys (FMP/FRED/Marketaux/OpenAI/admin secret) — those stay backend-only.

Existing ad hoc fetch call sites (`useHealthCheck.ts`, the onboarding screens' category/topics
submit handlers) get migrated onto the new client so there's one fetch path, not two.

### Acceptance Criteria

- A signed-in request made through the client reaches a `/v1/users/me/*` route and the backend's
  Clerk auth dependency accepts the attached token (verified against the real running backend, not
  mocked).
- An expired/missing/invalid token produces the same normalized error shape as any other failed
  request — no unhandled promise rejection.
- A request against a deliberately unreachable backend times out instead of hanging.
- `useHealthCheck.ts` and the onboarding screens' submit calls are migrated onto the shared client
  and still work end-to-end on a physical device against the real backend.

### Definition of Done

Every mobile network call — authenticated or not — goes through one client, and no screen
constructs its own `Authorization` header or reads `EXPO_PUBLIC_API_BASE_URL` directly.

### Suggested Commit

`feat: add authenticated mobile API client`

### Claude Code Tutor Prompt

> Help me build a shared, authenticated fetch wrapper for the Walris mobile app. Explain how to
> attach a Clerk session token to outgoing requests and how to normalize errors so every screen can
> handle them the same way.

## Milestone 25 — Frontend Response Schemas

### Objective

Give the mobile app compile-time *and* runtime confidence in backend response shapes: Zod schemas
that parse and validate what `GET /v1/users/me/briefing` and `GET`/`PUT /v1/users/me/preferences`
actually return, instead of trusting `response.json()`'s `any` type the way the current onboarding
screens and `useHealthCheck.ts` do.

**Scope correction from this section's original draft:** the earlier version of this milestone
described schemas for "AI-generated narrative text, supporting indicator values, supporting news
items." That doesn't match what the backend actually returns today —
`backend/app/schemas/user_briefing.py`'s `UserBriefingResponse` is just `date` + `content.headline`
+ `content.sections[].{heading, body}`. There's no structured indicator-value or news-item data in
the response at all; that content only exists as prose inside each section's `body` text. Milestone
30 (Key Indicator Chart Component) and Milestone 31 (Supporting News Cards) will need *something*
structured to render from — a real gap between the plan and the current API surface, not something
to paper over with a schema for fields that don't exist. This milestone validates the real current
shape; the M30/M31 gap needs an explicit decision before those milestones start (see Deliverables).

### Deliverables

- Add `zod` as a mobile dependency (not yet installed — `npm install zod` in `mobile/`).
- `UserBriefingResponse` schema matching the real API response:
  - `date: string` (ISO date, as FastAPI serializes Pydantic's `date`)
  - `content.headline: string`
  - `content.sections: { heading: string; body: string }[]`
- `UserPreferences` schema matching `backend/app/schemas/user.py`:
  - `category: string | null`
  - `additional_topics: string[]`
- Parse (not just type-assert) `apiFetch`'s JSON responses through these schemas at the call site,
  so a shape mismatch fails loudly (a caught, normalized error) instead of silently producing
  `undefined`s deep in a component.
- A short written note (in this section or `docs/05-resume-prompt.md`'s Known Issues) flagging the
  M30/M31 structured-data gap above for a real decision later: either the backend gains
  structured indicator/news fields on `UserBriefingResponse`, or the mobile app derives them some
  other way. Not this milestone's problem to solve, but not to be silently forgotten either.

### Acceptance Criteria

- A real response from `GET /v1/users/me/briefing` (both branches — an existing briefing and the
  no-briefing-yet fallback) parses successfully against the schema, verified against the live
  local backend, not just asserted in isolation.
- A real response from `GET /v1/users/me/preferences` parses successfully, for both a user with a
  category already set and a freshly-signed-up user with `category: null`.
- A deliberately malformed/unexpected response shape fails Zod parsing with a clear error, rather
  than silently coercing into `undefined` fields.

### Definition of Done

Every response the mobile app reads from `/v1/users/me/briefing` and `/v1/users/me/preferences`
is validated at runtime, not just assumed to match its TypeScript type.

### Suggested Commit

`feat: add Zod schemas for briefing and preferences responses`

### Claude Code Tutor Prompt

> Help me write Zod schemas for Walris's briefing and preferences API responses. Explain why
> validating a response at runtime catches bugs that TypeScript's compile-time types alone can't.

## Milestone 26 — TanStack Query Hooks

### Objective

Give the Home Screen (M32) a single, reusable hook for the signed-in user's personalized daily
briefing — `useTodayBriefing` — instead of a screen calling `apiFetch` and parsing the response
itself the way the onboarding screens currently do. This is also where `UserBriefingResponseSchema`
(built and verified in M25, but deliberately left unwired since nothing consumed it yet) gets wired
into a real call site for the first time.

**Scope note:** `docs/02` §15 (State Management) still lists "Fetching event details" as something
TanStack Query should handle — stale, from the pre-pivot single-shared-briefing design. There's no
discrete event left to fetch (per this section's own long-standing title), so no `useEventDetail`
exists or is planned.

### Deliverables

- `mobile/hooks/useTodayBriefing.ts`, following the same shape as the existing
  `mobile/hooks/useHealthCheck.ts`:
  - Calls `useAuth()` (`@clerk/expo`) internally for `getToken`/`isLoaded`/`isSignedIn`, so callers
    don't have to thread Clerk state through themselves.
  - Query function: `apiFetch('/v1/users/me/briefing', getToken)` → `await response.json()` →
    `UserBriefingResponseSchema.parse(...)`, so a shape mismatch fails loudly through the query's
    `error` state instead of producing `undefined`s in a rendered screen.
  - `enabled: isLoaded && isSignedIn` — mirrors the guard `topics.tsx` already uses before fetching,
    so the hook doesn't fire a doomed authenticated request before Clerk is ready.
  - A stable query key (e.g. `['briefing', 'today']` — no date parameter needed, since the endpoint
    always resolves "today" server-side from the signed-in user's session).
- No `useEventDetail` (see Scope note above) and no client-side caching/staleness tuning beyond
  `queryClient`'s current defaults — not needed until a real screen surfaces a caching problem.

### Acceptance Criteria

- The hook's query function, called directly (not just type-checked), successfully parses a real
  response from `GET /v1/users/me/briefing` for both branches — a real generated briefing, and the
  no-briefing-yet fallback — the same two real-data cases M25 already verified the schema against.
- `isPending`/`isError`/`data`/`refetch` all behave as expected from a real `useQuery` consumer
  (a throwaway test screen or console log is enough — Milestone 32 owns the real Home Screen UI).
- The hook doesn't fire before Clerk's session is ready (verified by confirming no request goes out
  while `isLoaded` is `false`).

### Definition of Done

Any screen that needs the signed-in user's today briefing can call `useTodayBriefing()` and get
back a validated, typed result with standard TanStack Query loading/error/refetch semantics — no
screen constructs its own `apiFetch` + parsing logic for this endpoint.

### Suggested Commit

`feat: add useTodayBriefing query hook`

### Claude Code Tutor Prompt

> Help me build a TanStack Query hook for Walris's personalized briefing endpoint. Explain how to
> combine a Zod-validated query function with Clerk's auth state so the hook doesn't fire requests
> before the user's session is ready.

## Milestone 27 — Walris Theme Tokens

### Objective

Make `docs/04-design-system.md`'s approved typography, spacing, and shape system real, usable
tokens in the mobile app — the same way its color system already is.

**Scope correction from this section's original draft:** it assumed colors, typography, spacing,
and radius all needed to be built from scratch under a single `mobile/theme/` folder. Checking the
actual codebase first: **colors are already done.** `mobile/global.css`'s CSS variables,
`tailwind.config.js`'s color mappings, and `mobile/lib/theme.ts` (React Navigation's theme) all
carry real Walris brand values, not placeholder/default ones — verified by converting
`docs/04`'s hex values back from the HSL stored in `global.css` (e.g. `--background: 231 100%
98.6%` is exactly `#f8f9ff`). This must have been seeded correctly during Milestone 4's scaffolding.
Forcing those into a second `mobile/theme/` copy would just create a duplicate source of truth
fighting NativeWind's own CSS-variable-based theming model — so this milestone leaves colors
untouched and scopes to what's actually missing: typography and the rest of the shape/spacing
system. (User decision, 2026-08-20: keep colors where they are; don't consolidate.)

### Deliverables

- Load the three approved typefaces (`docs/04` §5) via `@expo-google-fonts/*` — all three
  (`libre-caslon-text`, `inter`, `jetbrains-mono`) are published packages, confirmed on the npm
  registry, so no manual font-file sourcing is needed.
- `mobile/theme/typography.ts` — one exported style object per type-scale token (`displayLg`,
  `displayLgMobile`, `headlineMd`, `headlineSm`, `bodyLg`, `bodyMd`, `caption`, `dataLabel`),
  bundling `fontFamily`/`fontSize`/`fontWeight`/`lineHeight`/`letterSpacing` per `docs/04` §5.1–5.3.
  Plain TS objects rather than Tailwind classes, since NativeWind's `text-*` utilities only cover
  `fontSize` — Walris's tokens are multi-property bundles.
- Extend `tailwind.config.js`'s `theme.extend`:
  - `spacing` aliases (`xs`/`sm`/`md`/`lg`/`xl`/`2xl`/`3xl`) matching `docs/04` §6's 8px scale —
    Tailwind's numeric scale already produces the right pixel values (`p-4`=16px, `p-6`=24px,
    `p-8`=32px), this just adds the named vocabulary `docs/04` uses.
  - `borderRadius` scale (`sm`/`DEFAULT`/`md`/`lg`/`xl`/`full`) per `docs/04` §8, replacing the
    current setup where only one `--radius` CSS variable exists and `lg`/`md`/`sm` are all derived
    from it via `calc()`.

### Acceptance Criteria

- All three fonts render correctly on a physical device (not just configured) — a quick temporary
  render of one string per typeface is enough to confirm, same verification style used for M26's
  `BriefingDebug`.
- Each typography token in `mobile/theme/typography.ts` matches `docs/04`'s exact
  size/weight/lineHeight/letterSpacing values.
- The new spacing/radius Tailwind classes are usable in a component (e.g. `p-lg`, `rounded-md`) and
  render the expected pixel values.

### Definition of Done

Every typeface, spacing value, and corner radius `docs/04-design-system.md` specifies is available
as a real, reusable token — colors already were, this closes the remaining gap — so no future
screen milestone needs to hardcode a font, spacing value, or radius by hand.

### Suggested Commit

`feat: add typography, spacing, and radius theme tokens`

### Claude Code Tutor Prompt

> Help me load custom fonts in Expo and turn Walris's typography scale into reusable style tokens.
> Explain why a multi-property type-scale token doesn't map cleanly onto Tailwind's single-value
> font-size utilities.

## Milestone 28 — App Layout Shell

### Objective

Give every screen one shared layout wrapper instead of each handling safe areas, scrolling, and
page margins independently — which right now they do inconsistently. Checked the actual code
first: `app/index.tsx` wraps in `SafeAreaView` with no margin at all; `(onboarding)/category.tsx`
and `(onboarding)/topics.tsx` wrap in `ScrollView` directly with **no `SafeAreaView`** and no
margin either. This isn't a hypothetical future problem — it's the current state.

### Deliverables

- `mobile/components/ui/screen.tsx` — a `Screen` component (kebab-case filename, matching every
  other file in `components/ui/`) combining:
  - `SafeAreaView` (`react-native-safe-area-context`, already a dependency and already used in
    `index.tsx`).
  - Optional scrolling via a `scroll?: boolean` prop — `index.tsx` currently doesn't scroll,
    `category.tsx`/`topics.tsx` do, so this needs to stay a per-screen choice, not hardcoded either
    way.
  - Horizontal page margin using M27's `md` spacing token (`1rem`/16px), matching `docs/04` §7.1's
    mobile margin spec exactly.
- Migrate the three existing screens (`index.tsx`, `category.tsx`, `topics.tsx`) onto `Screen`,
  removing their own ad hoc `SafeAreaView`/`ScrollView` usage.

### Acceptance Criteria

- All three migrated screens render correctly on a physical device: safe area respected
  (no content under the notch/status bar), consistent 16px horizontal margin, and scroll behavior
  unchanged from before the migration (`index.tsx` still doesn't scroll, the onboarding screens
  still do).
- No screen in the app constructs its own `SafeAreaView` directly anymore.

### Definition of Done

Every screen gets consistent safe-area handling and page margins through one shared component, and
adding a new screen never requires re-deciding how to handle either.

### Suggested Commit

`feat: add shared Screen layout component`

### Claude Code Tutor Prompt

> Help me build a reusable screen layout wrapper for Walris that handles safe areas, optional
> scrolling, and consistent page margins. Explain why hardcoding scroll behavior into the wrapper
> would be the wrong call here.

## Milestone 29 — Daily Briefing Header

### Objective

Build the identity header every screen-content milestone from here on can sit under: app name,
current date, and a greeting — replacing the old generic version, which had no concept of a
signed-in user to greet.

**Scope note:** `docs/04` §10.2 describes a richer "Daily Briefing Header" — logo/name, date,
briefing title, briefing summary, generated timestamp. The roadmap already narrows this milestone
to just app name/date/greeting, deferring the actual briefing content (headline, sections) to
Milestone 32's Home Screen — a sensible split (this = identity header, M32 = real content), kept as
originally scoped.

**Scope decision (2026-08-21):** the greeting is a generic time-of-day greeting ("Good morning" /
"Good afternoon" / "Good evening" based on device time), not personalized with the user's name.
`User.name` exists as a DB column, but nothing in the app currently sets it — it's the still-open
Milestone 14 loose end (a name field, deliberately deferred to onboarding, not yet built), and
there's no API endpoint exposing it either. Building a name-based greeting now would mean either
faking data or extending the backend for a field nothing populates yet. Name-based personalization
becomes a real follow-up once M14's name field actually exists.

### Deliverables

- `mobile/components/ui/daily-briefing-header.tsx` — a `DailyBriefingHeader` component:
  - App name ("Walris"), styled with M27's `headlineMd`/`headlineSm` typography token (Libre
    Caslon Text, per `docs/04` §10.2's "serif title" style guidance).
  - Current date, formatted via the built-in `Intl`/`Date` APIs (no new date-library dependency
    needed for this).
  - A time-of-day greeting, computed from the device's local hour.
- Wire it into `app/index.tsx` above the existing debug blocks, inside `Screen`, as the first real
  use of both M27's typography tokens and M28's layout shell together outside the debug scaffolding.

### Acceptance Criteria

- Renders correctly on a physical device: correct date for "today," a greeting that matches the
  actual time of day (verified by checking at a couple of different times, not just once).
- Uses `Screen`/typography tokens rather than hardcoded styles or ad hoc `Text` styling.

### Definition of Done

Every screen that needs the app's identity header (starting with the home screen, extending to
whichever future screens need it) can render `DailyBriefingHeader` instead of hand-rolling app
name/date/greeting markup.

### Suggested Commit

`feat: add DailyBriefingHeader component`

### Claude Code Tutor Prompt

> Help me build a header component for Walris that shows the app name, today's date, and a
> time-of-day greeting. Explain how to compute a greeting from the device's local time without
> pulling in a date-formatting library for something this simple.

## Milestone 30 — Key Indicator Chart Component

**Deferred (2026-08-24), not part of V1.** After scoping this out (below), decided the chart isn't
worth shipping yet: most indicators only have 1-2 data points right now (the 400-day retention
just started), so a chart showing the same near-static picture every single day doesn't earn its
place on a screen a user opens daily — it directly conflicts with `docs/04`'s own "don't make the
chart dominant" rule in a different way than expected (dominant by repetition/staleness, not by
size). Revisit once enough real history has accumulated for a trend to actually be visible
day-to-day. The scoping work below (indicator-selection logic, chart library choice) stays as
reference for whenever this gets picked back up — the backend `indicators` data itself (Milestone
30's actual blocker) is already shipped and useful regardless. Milestone 32 (Home Screen) no longer
assembles a chart — see its updated scope.

### Objective

Replaces the old "Basic Historical Chart" (previously an event-detail-page feature, Milestone 38).
Now a Home Screen building block: a lightweight chart rendering the user's single key FRED
indicator, per `docs/04` §10.8's rules — simple, not the dominant element on the screen, trend
clearly visible.

**Scope decision (2026-08-24):** the backend extension (see `docs/05`'s write-up) returns up to 32
relevant indicators per user — but the milestone's own name is *"Key Indicator"* (singular), and
`docs/04` explicitly says not to let the chart dominate. There's no existing "most important
indicator" ranking anywhere in the codebase — `get_relevant_fred_item_keys` returns everything
relevant to a category/topic, unranked. Rather than charting all 32 (violates "keep it simple") or
picking an arbitrary one (the first alphabetically, meaningless), this milestone adds a small,
explicit `CATEGORY_PRIMARY_INDICATOR` mapping — one deliberately-chosen FRED series per category,
confirmed already present in that category's relevant set:

```text
investor              -> DGS10          (10-Year Treasury Yield)
small_business_owner  -> MPRIME         (Prime Rate)
consumer               -> CPIAUCSL       (Consumer Price Index)
home                   -> MORTGAGE30US   (30-Year Fixed Mortgage Rate)
student                -> UNRATE         (Unemployment Rate)
job_seeker             -> UNRATE         (Unemployment Rate)
everything             -> CPIAUCSL       (Consumer Price Index)
```

**Real data caveat:** the backend's 400-day retention only started 2026-08-24 (see `docs/05`) —
most indicators currently have just 1-2 data points, not a real trend line yet. The chart needs to
render sensibly with sparse data (e.g. a single point, or two) today, and grow into a real trend
view as history accumulates. Not something to fake or pad with synthetic points.

### Deliverables

- Backend: `CATEGORY_PRIMARY_INDICATOR: dict[str, str]` (likely in `fmp_category_rules.py`,
  alongside the existing `CATEGORY_ITEM_KEYS`), and a small addition to `get_todays_briefing` (or a
  new field on the response) surfacing which of the returned `indicators` is the user's primary
  one — e.g. a `primary_item_key: str | None` field on `UserBriefingResponse`, so the mobile app
  doesn't need to duplicate the category→indicator mapping client-side.
- Mobile: install a charting dependency — `react-native-svg` (`npx expo install react-native-svg`)
  is the recommended choice: lightweight, no heavy native charting engine, and gives full control
  to hand-build a simple line/sparkline matching `docs/04`'s "keep it simple" directive, rather
  than pulling in a full charting library's defaults (axes, legends, etc.) that would need
  stripping down anyway.
- `mobile/components/ui/key-indicator-chart.tsx` — a `KeyIndicatorChart` component: given an
  `IndicatorSeries`, renders a simple SVG line (or a single labeled point when there's only one
  data point), the indicator's `label`, and its latest value — matching §10.8's "include latest
  value context" rule.
- Wire it into `app/index.tsx` (temporarily, same pattern as the other debug/verification blocks)
  using `useTodayBriefing`'s data and the new `primary_item_key` to pick the right series out of
  `indicators`.

### Acceptance Criteria

- Renders correctly on a physical device for the real test user's actual primary indicator and
  real (currently sparse) data — not a mocked/synthetic dataset.
- Doesn't crash or render nonsensically with only 1 data point.
- Visually matches `docs/04` §10.8: no excessive axes/labels, chart isn't the dominant element,
  latest value is legible.

### Definition of Done

A user's key indicator — chosen deterministically by their category, not arbitrarily — renders as
a real, simple chart using real backend data, ready for Milestone 32 to place on the actual Home
Screen.

### Suggested Commit

`feat: add KeyIndicatorChart component`

### Claude Code Tutor Prompt

> Help me build a simple line chart for Walris using react-native-svg. Explain how to handle the
> case where an indicator only has one data point instead of a real trend line.

## Milestone 31 — Supporting News Cards

### Objective

Replaces "News Article Cards" (previously Milestone 37, tied to an individual event's detail page).
Cards linking out to the source Marketaux articles behind that day's personalized narrative — same
data-availability gap as Milestone 30 had: `DailyDataNews` (real Marketaux articles, headline,
source, summary, published time, sentiment, URL) exists in the database, linked to
`DailyDataItem` rows, but is never exposed through any API endpoint. This milestone closes that
gap and builds the cards.

**Scope decision (2026-08-24):** tested against a real date with actual fetched data (2026-08-17,
since today hasn't been fetched yet) — one user's relevant news came back as **125 rows, 96 unique
URLs**. The milestone's own name is "Supporting" cards, not a full feed — showing all of them would
dominate the screen the same way M30's chart would have. There's also no existing ranking; the
backend function returns them in arbitrary query order. Resolved: dedupe by `url`, sort by
`published_at` descending, cap at **5** cards — simple, defensible ("most recent first"), no new
ranking logic needed.

### Deliverables

- Backend: reuse `openai_service.py`'s existing `get_user_daily_data_with_news(user, as_of)` — the
  same function that already combines relevant FRED + FMP items with their linked news for the AI
  prompt, called read-only from the router (same pattern M30's indicator extension used with
  `get_relevant_fred_item_keys`, not a modification of the existing function).
  - New `NewsItem` schema (`backend/app/schemas/user_briefing.py`): `headline`, `source`,
    `summary`, `published_at`, `url`, `sentiment: float | None` — matching `docs/04` §10.7's
    required fields (Publisher, headline, summary, published time, sentiment tag) except "topic,"
    which doesn't exist as a field on `DailyDataNews` — `sentiment` is the only tag data available.
  - `UserBriefingResponse` extended with `news: list[NewsItem]`.
  - `briefings.py`: flatten `get_user_daily_data_with_news(user, today).news` across all relevant
    items, dedupe by `url`, sort by `published_at` descending, take the first 5.
- Mobile: `mobile/schemas/briefings.ts`'s `NewsItemSchema` + `UserBriefingResponseSchema` extended
  with `news`, mirroring the backend.
- `mobile/components/ui/news-card.tsx` — a `NewsCard` component per `docs/04` §10.7's style rules:
  12px radius (M27's `md` radius token), subtle border, headline in `headlineSm` (Libre Caslon
  Text), summary in `bodyMd` (Inter), source/sentiment tag in `dataLabel` (JetBrains Mono). Tapping
  a card opens `url` (`Linking.openURL`).
- Wire a list of `NewsCard`s into `app/index.tsx` (temporarily, same debug-block pattern as the
  rest of Part 3) using `useTodayBriefing`'s new `news` field.

### Acceptance Criteria

- Renders correctly on a physical device against real data — verified against an actual date with
  fetched news (today's data won't exist until the daily pipeline runs again), not a mocked list.
- Never shows duplicate articles (same `url` twice) and never shows more than 5.
- Tapping a card actually opens the article's real URL.

### Definition of Done

A user's daily briefing surfaces up to 5 real, deduplicated, recent supporting news articles as
tappable cards, matching `docs/04`'s News Card style — ready for Milestone 32 to place on the real
Home Screen.

### Suggested Commit

`feat: add supporting news cards`

### Claude Code Tutor Prompt

> Help me expose Walris's linked news articles through the briefing API and render them as cards.
> Explain why deduplicating by URL matters when the same article can be linked to multiple relevant
> data items.

## Milestone 32 — Home Screen

### Objective

Replace `app/index.tsx`'s M10-M31 verification scaffolding (`HealthProfile`, `BriefingDebug`,
`TypographyDebug`) with the actual Home Screen: assembles Milestones 29 and 31 into one real
screen — header, the AI-generated narrative, supporting news cards, working loading/empty/error
states, and pull-to-refresh. **No key-indicator chart** — Milestone 30 is deferred (see its
section above); the underlying `indicators` data is still available in the API response for
whenever that's revisited.

**Scope notes:**

- `docs/04` §20's Home Screen spec ("top 5 events," "notification CTA if not enabled") is stale,
  pre-pivot text — the roadmap's own description above is what's actually being built; there's no
  per-event navigation, since Milestones 35/36 from the original Part 3 (event detail route +
  content sections) no longer apply under this model, and notification permission/registration
  doesn't exist yet (that's Milestones 35-37, later in the roadmap) so a CTA for it would have
  nothing to link to.
- **Real gap found while scoping:** `index.tsx` currently has no signed-in/signed-out branching at
  all — every visitor, authenticated or not, sees the same `HealthProfile` block (backend status +
  sign-in/sign-up links) regardless of session state. There's also no route guard anywhere in
  `app/_layout.tsx` redirecting a signed-out user away from `/`. This means `/` is the *only*
  reachable entry point for a signed-out user to reach sign-in/sign-up — the real Home Screen this
  milestone builds needs an `isSignedIn` check (`useAuth()`, already used elsewhere in the app) to
  decide whether to render the sign-in/sign-up prompt or the real briefing UI, not just delete the
  auth links outright.
- **Loading/empty/error states here should stay functional, not polished** — Milestone 33 (next)
  is explicitly scoped to the real designed versions of these states (`docs/04` §10.9/§10.10) plus
  a shared retry mechanism. Building throwaway polish now that M33 immediately replaces would be
  wasted work.

### Deliverables

- `mobile/components/ui/screen.tsx`: extend `Screen` with an optional `refreshControl` prop
  (`ReactElement`), forwarded to its internal `ScrollView` — the only way React Native supports
  pull-to-refresh, and `Screen` currently has no way to pass one through.
- `mobile/components/ui/briefing-narrative.tsx` — a new `BriefingNarrative` component rendering
  `content.headline` (`headlineMd`/`headlineSm` typography) and each `content.sections[]` entry
  (heading + body, `bodyMd` for body text) — the actual AI-generated narrative has never been
  rendered anywhere yet; `BriefingDebug` only ever showed a headline string and a section count.
- Rewrite `app/index.tsx`'s `Home()`:
  - `useAuth()`'s `isSignedIn` branches between the sign-in/sign-up prompt and the real screen.
  - Signed-in: `DailyBriefingHeader`, `BriefingNarrative`, a list of `NewsCard`s from `news`, all
    inside `Screen scroll` with a `RefreshControl` wired to `useTodayBriefing`'s `refetch`/
    `isRefetching`.
  - Basic, functional (not yet `docs/04`-styled) loading/empty/error states — no crash, no
    infinite spinner, an empty-briefing day reads as "not available yet," not as broken.
  - Remove `HealthProfile`'s "Backend Connected" debug text, `BriefingDebug`, and
    `TypographyDebug` entirely — this milestone is what all three were scaffolding toward.

### Acceptance Criteria

- Verified live on a physical device: a signed-in user with a real generated briefing sees the
  real headline, section text, and news cards; a signed-in user with no briefing yet sees a
  reasonable empty state, not a crash; a signed-out user sees the sign-in/sign-up prompt, not the
  briefing UI.
- Pull-to-refresh actually triggers a real refetch and updates the screen when new data differs.
- No leftover references to `useHealthCheck`, `BriefingDebug`, or `TypographyDebug` anywhere in
  `app/index.tsx`.

### Definition of Done

Opening the app as a signed-in user with a category selected shows their actual personalized daily
briefing — the real thing this entire project has been building toward — not a debug scaffold.

### Suggested Commit

`feat: build real Home Screen from M29/M31 components`

### Claude Code Tutor Prompt

> Help me assemble Walris's real Home Screen from the header, narrative, and news card
> components we've already built. Explain how pull-to-refresh works with TanStack Query's
> `refetch` and why `Screen` needs a new prop to support it.

## Milestone 33 — Empty, Error, and Loading States

### Objective

Replace `TodayBriefing`'s (`app/index.tsx`) placeholder loading/error handling — `<Text>Loading...</Text>`
and a raw `<Text>{error.message}</Text>` dump — with real, designed states per `docs/04` §10.9
(Empty State) and §10.10 (Error State), plus a consistent, reusable way to retry a failed request.
Deliberately deferred from M32 to avoid polishing something that milestone was always going to
hand off.

**Real distinction found while scoping:** "empty" and "no data yet" are two different states that
currently look identical. The backend has two separate fallback paths that both produce
`content.sections: []` — `briefings.py`'s "no briefing generated yet" fallback (headline: "No
briefing available yet for today.") and `prompt_services.py`'s `build_quiet_day_briefing` (headline:
"Nothing notable to report today.", for a user whose filtered dataset was genuinely empty that day).
A **real** generated briefing always has non-empty `sections` (M18's OpenAI generation always
produces themed sections) — so `content.sections.length === 0` is a reliable signal to treat as the
empty state, rather than rendering the fallback headline dressed up as if it were real narrative
content (which is what happens today).

### Deliverables

- `mobile/components/ui/empty-state.tsx` — `EmptyState`, per `docs/04` §10.9's tone (calm, helpful,
  non-alarming) and example copy ("Today's briefing is not available yet. Check back shortly.").
- `mobile/components/ui/error-state.tsx` — `ErrorState`, per `docs/04` §10.10's tone (clear, honest,
  recoverable) and example copy ("We couldn't load today's briefing. Please try again."), with a
  required retry action — a button/pressable calling an `onRetry` prop. This is the "consistent way
  to retry" the milestone calls for: any screen can reuse this component instead of inventing its
  own retry UI.
- `mobile/components/ui/loading-state.tsx` — `LoadingState`, a minimal, calm loading indicator
  (`ActivityIndicator`, not just literal "Loading..." text) — `docs/04` has no dedicated spec for
  this one beyond its QA checklist asking that loading states exist at all, so this is a reasonable
  default rather than a strict requirement.
- `TodayBriefing` updated to use all three: `LoadingState` for `isPending`, `ErrorState` (wired to
  `useTodayBriefing`'s `refetch`) for `isError`, and `EmptyState` when `data.content.sections.length
  === 0`, falling through to the real `BriefingNarrative`/`NewsCard`s otherwise.

**Scope boundary:** the onboarding screens (`category.tsx`/`topics.tsx`) have their own ad hoc
error handling (`setErrorMessage` + inline `<Text>`) for different concerns (form validation, not
just network retry) — not being retrofitted onto these new components as part of this milestone.
`ErrorState`/`EmptyState`/`LoadingState` are built for reuse by future screens, not a mandate to
touch every existing one now.

### Acceptance Criteria

- Verified live on a physical device: a user with a real generated briefing sees the real content
  (unchanged from M32); a user whose briefing is a quiet-day/not-yet-generated fallback sees the
  calm `EmptyState`, not a headline styled like real content; a deliberately-triggered failure
  (e.g. killing the backend mid-request) shows `ErrorState`, and tapping its retry action actually
  triggers a new request and recovers once the backend is back.

### Definition of Done

Every state `useTodayBriefing` can be in — loading, a real error, empty/no-content, and success —
has its own real, `docs/04`-styled treatment, and failed requests are recoverable without
force-quitting or reloading the app.

### Suggested Commit

`feat: add designed empty, error, and loading states`

### Claude Code Tutor Prompt

> Help me build reusable empty and error state components for Walris, following the tone and copy
> guidelines in the design system. Explain how to distinguish "no data yet" from "a real error"
> using what the API actually returns, rather than guessing from the error message.

## Milestone 34 — Mobile Integration Test Pass

### Objective

End-to-end verification of the full personalized flow, run as one continuous journey rather than
the piece-by-piece verification every milestone from M24-M33 already did individually: sign-up/
sign-in → onboarding (category/topics) → Home Screen fetch → real backend data → sign-out, on a
real device, including the backend-down state.

**Scope decision (2026-09-02): iOS-only for now, not part of V1's blocker list.** `docs/03`'s
original scope calls for "both iOS and Android," but this project has never had Android tooling
set up — no Android Studio, no emulator, no physical Android device (see Known Issues). Rather
than silently dropping that half of the milestone or blocking on setting up an entire second
platform's tooling right now, M34 is explicitly scoped to iOS (the only platform this project has
ever run on, via Expo Go on a physical iPhone) — Android becomes a tracked, explicit follow-up
once a device/emulator is available, not a silent gap.

**What this milestone actually adds, given how much has already been verified live:** M24-M33 each
verified their own piece in isolation (auth methods individually, the Home Screen's states
individually, sign-out on its own). What hasn't been confirmed is all of it working *together*, in
one uninterrupted run, on a genuinely fresh account — catching integration issues that only show up
when one milestone's output feeds directly into the next (e.g., does the exact category/topics a
user picks during onboarding actually show up correctly in that user's first real Home Screen
fetch, in the same session, without any manual database resets in between).

### Deliverables

- One documented, uninterrupted test run: sign up with a genuinely new account (not the existing
  reused test user) → verify `redirectAfterAuth` sends a brand-new user to `/category` → complete
  category + topic selection → land on the real Home Screen → confirm the empty state (a fresh
  account has no generated briefing) → sign out → sign back in → confirm `redirectAfterAuth` sends
  a returning user straight to `/` this time, not back through onboarding.
- Confirm the backend-down state within this same continuous run (stop the backend mid-session, not
  just in isolation as M33 already verified) — reconfirms `ErrorState`'s retry recovers without
  needing to restart the app.

### Acceptance Criteria

- The full run above completes on a physical iPhone with no manual workarounds (no ad hoc database
  resets required to reach any step) and no unexpected errors.
- A genuinely new account's category/topics correctly persist and correctly gate `redirectAfterAuth`'s
  routing decision on the very next sign-in, in the same test session.

### Definition of Done

The complete personalized mobile flow — from a brand-new sign-up through to a real signed-in Home
Screen and back to sign-out — works as one continuous journey on a real device, with Android
explicitly tracked as a follow-up rather than silently untested.

### Suggested Commit

`docs: record Milestone 34 integration test pass`

### Claude Code Tutor Prompt

> Help me plan an end-to-end integration test for Walris covering sign-up through the Home Screen.
> Explain why testing each piece individually doesn't guarantee the full journey works together.

## Mobile App Phase Complete

After Milestone 34, Walris will have:

- React Native frontend API layer, with Clerk-authenticated requests
- Runtime response validation with Zod
- TanStack Query data fetching for the personalized briefing
- Walris theme tokens
- Home screen rendering the personalized narrative, supporting chart(s), and supporting news
- Loading, empty, and error states
- End-to-end mobile/backend integration, verified on iOS and Android

At this point, Walris should feel like a real, personalized mobile product.

The next phase should focus on:

- Push notifications
- QA
- Performance
- Polish
- Deployment
- App Store / Google Play preparation

(See this section's note above — Part 4 below still needs its own re-scoping pass before starting.)

---

# Walris Development Roadmap

**Document:** docs/03-development-roadmap.md
**Version:** 1.0
**Phase:** Part 4 – Notifications, QA, Deployment & Launch (Personalization Pivot)

---

## Part 4 Overview

**Replaces the original Milestones 41-56.** Renumbered from 35 to close the gap left by Part 3
shrinking from 14 milestones (27-40) to 11 (24-34). The content itself mostly carries over
unchanged — notification setup, QA, deployment, App Store prep are all still real, necessary work
— but every reference to the old event model has been corrected: **no more anonymous device
tokens** (V1 requires sign-in before the app is usable at all, per `docs/02-system-architecture.md`
§4, so there's no anonymous state left to support), no more event cards/event detail in QA
scenarios or performance targets, and Supabase/API references updated to the schema actually built
in Part 2 (`users`, `daily_data_items`, `daily_data_news`, `user_briefings`, `device_tokens`,
`job_runs`).

By the end of this phase, Walris should have:

- Morning push notifications, tied to signed-in users (not anonymous devices)
- Production backend deployment
- Production database configuration
- App Store / Google Play readiness, including production Google/Apple OAuth credentials
- QA testing against the actual current endpoint/screen set
- Error monitoring
- Performance checks
- Release checklist

---

## Milestone 35 — Expo Notifications Setup

### Objective

Give the mobile app the ability to request notification permission and obtain a real Expo push
token — client-side capability only, no backend call yet (that's M37, once M36's already-built API
is wired up). Unchanged from the original scope; this never depended on the event-vs-personalization
model.

**Scope note found while grounding this milestone:** `docs/03`'s Milestone 36 (Device Token
Registration API) is **already built** — `POST /v1/notifications/register` (`backend/app/routers/
notifications.py`) exists exactly as M36 describes: authenticated via `get_current_user`, storing
`expo_push_token`/`device_id`/`platform`/`timezone` against `device_tokens.user_id` directly. It
was built as part of Milestone 21's backend work and live-verified during M22/M23's integration
pass. So once M35 (this milestone) and M37 (wiring the two together) are done, the full
registration pipeline is complete — there's no new backend work left in this sequence, just two
mobile milestones.

### Deliverables

- Install `expo-notifications` and `expo-device` (`npx expo install`, matching how M27's font
  packages were installed).
- A permission-request flow using `Notifications.requestPermissionsAsync()`, gated on
  `Device.isDevice` — Expo push tokens don't work on simulators, only real devices (this project
  has only ever tested on physical hardware anyway, so this should be a non-issue in practice, but
  the check still needs to exist so the app fails gracefully rather than silently on anyone who
  ever does run it in a simulator).
- Retrieve the actual Expo push token via `Notifications.getExpoPushTokenAsync()`.
- The standard Android notification channel setup (`Notifications.setNotificationChannelAsync`) —
  write this correctly even though Android isn't tested yet (per M34's decision); this is cheap,
  standard Expo boilerplate, not something to skip just because verification is iOS-only for now.

### Acceptance Criteria

- Verified live on the physical iPhone this project has used throughout: permission prompt
  appears, granting it returns a real, non-empty Expo push token (log it to confirm, since there's
  nothing to register it against yet).
- Denying permission doesn't crash the app — it's a real, reachable user choice, not just a happy
  path to test.

### Definition of Done

The app can obtain a real Expo push token on a physical device, ready for M37 to actually send it
to the (already-built) registration endpoint.

### Suggested Commit

`feat: add Expo push notification permission and token retrieval`

### Claude Code Tutor Prompt

> Help me set up Expo push notification permissions in Walris. Explain why Expo push tokens only
> work on physical devices, not simulators, and how to handle a user denying permission gracefully.

## Milestone 36 — Device Token Registration API

**Already complete** — built as part of Milestone 21's backend work, ahead of this roadmap
position, and live-verified during M22/M23's integration pass. See M35's section above for the
full note. Original scope, for reference: replaces "Notification Token API." Since V1 requires
authentication before the app is usable at all, there's no anonymous-token flow to build anymore —
`POST /v1/notifications/register` is an authenticated endpoint (same `get_current_user` pattern as
the preferences endpoint), storing the token against `device_tokens.user_id` directly at
registration time rather than registering anonymously and linking later.

## Milestone 37 — Notification Registration Flow

Unchanged in concept: request permission at an appropriate moment (now naturally after onboarding,
since the user is already signed in by then), get the Expo push token, `POST` it to the backend,
store registration status locally to avoid re-prompting.

## Milestone 38 — Personalized Notification Sender

Replaces "Morning Notification Sender." The old hardcoded copy ("View this morning's top 5
economic events.") doesn't fit — every user's briefing content differs now, so the notification
service sends to each user with a completed `user_briefings` row for that day, with generic
copy that doesn't presume specific content (e.g. "Your personalized economic briefing is ready").
Still: fetch active tokens, send via Expo, handle/deactivate invalid tokens, log results.

## Milestone 39 — Notification Schedule

Replaces "Notification Schedule." The send condition changes from a single global check ("today's
briefing exists and is complete") to a per-user check — only send to a given user once their
`user_briefings` row for today exists, matching Milestone 19's per-user generation job. Job
execution still logged in `job_runs`; manual trigger still available for testing.

## Milestone 40 — Backend QA & Error Handling

Same objective as the original Milestone 46 (harden external-API/OpenAI/database failure handling,
job failure logging, admin endpoint protection), but the test list is updated to the endpoints that
actually exist now: `GET /health`, `GET`/`PUT /v1/users/me/preferences`, the personalized briefing
endpoint from Milestone 20, and `POST /v1/notifications/register` — not the old
`/briefings/today`/`/events/{event_id}` pair.

## Milestone 41 — Mobile QA & Device Testing

Same device/screen-size matrix as the original Milestone 47, but scenarios updated: drop "Event
detail open" (no longer exists) and reframe "No news articles"/"No FRED data" as "no supporting
news" / "no supporting chart data" (Milestones 30/31's optional Home Screen sections, not a
required detail page). Add the sign-up/sign-in and onboarding (category/topics) flow as an
explicit first-open scenario, since that's now part of every new user's path through the app.

## Milestone 42 — Production Backend Deployment

Unchanged from the original scope: deploy FastAPI (Render/Railway/Fly.io), configure environment
variables, verify the database connection and health endpoint, confirm the scheduled daily
personalization job (Milestone 23) can run in production.

## Milestone 43 — Production Supabase Configuration

Same objective as the original Milestone 49 (production schema, indexes, secure service-role
usage, backups, migration workflow), but the table list is corrected to what Part 2 actually built:
`users`, `daily_data_items`, `daily_data_news`, `user_briefings`, `device_tokens`, `job_runs` — not
the old `briefings`/`economic_events`/`enriched_events`/`fred_series`/`news_articles` set.

## Milestone 44 — Mobile Production Configuration

Unchanged core scope (`app.json`/`eas.json`, production API URL, app icon, splash screen, bundle
identifiers), plus one addition specific to this pivot's auth work: Clerk's free shared OAuth
credentials for Google/Apple only work on **development** instances (verified this session) — a
production Clerk instance needs real Google Cloud Console and Apple Developer credentials
configured before Google/Apple sign-in works for real users. This is also the point where the
Apple Developer Program's $99/year membership becomes a real cost, not a deferred one, since it's
required for App Store distribution regardless of auth method.

## Milestone 45 — Analytics & Basic Monitoring

Same objective as the original Milestone 51, but the tracked mobile events are updated for the new
screen set: drop `event_card_tapped`/`event_detail_viewed`, add `chart_viewed`/`news_link_opened`
(Milestones 30/31's Home Screen sections) and `category_selected`/`topics_selected` (onboarding
funnel visibility, Milestone 14). Keep `app_opened`, `briefing_viewed`, and the notification
permission/opened events. Backend monitoring events (`briefing_job_success/failure`,
`notification_job_success/failure`, `external_api_failure`, `openai_validation_failure`) are
unchanged — the job-level shape didn't change, just who it runs for (every user, not once
globally).

## Milestone 46 — Performance Pass

Same target list as the original Milestone 52, minus "Event detail load" (no longer exists) —
home-briefing load, cold app open, backend health check, and briefing-generation targets all still
apply unchanged. "Backend uses cached/pre-generated briefing data" still holds exactly as before,
matching the daily per-user pre-generation job.

## Milestone 47 — App Store Assets

Unchanged core scope (icon, splash screen, screenshots, description, keywords, support/privacy
URLs, tagline), except the privacy policy needs to describe what's actually collected now — email,
category/topic preferences, and notification tokens tied to a real account — not "anonymous
notification token storage," which no longer describes this app.

## Milestone 48 — Beta Distribution

Unchanged from the original scope: TestFlight / Google Play Internal Testing, recruit testers,
collect structured feedback on clarity, usefulness, trust, and notification timing.

## Milestone 49 — Launch Readiness Checklist

Same structure as the original Milestone 55, with two Product-checklist corrections: drop "Event
detail works" (no longer exists), and replace "No-auth experience works" with "Sign-up/sign-in +
onboarding flow works" — V1 requires authentication, so there's no no-auth path left to verify.
Backend/Database/Mobile/Legal checklist items are otherwise unchanged.

## Milestone 50 — Public Launch

Unchanged from the original scope: submit to the App Store and Google Play, monitor crashes,
backend errors, daily job success, notification delivery, and user feedback post-launch.

## Part 4 Complete

After Milestone 50, Walris will have:

- Push notification registration and delivery, tied to signed-in users
- Backend QA against the actual current endpoint set
- Mobile QA against the actual current screen set
- Production backend and Supabase configuration matching the real schema
- Production Google/Apple OAuth credentials
- Production Expo builds
- Basic analytics and performance validation
- App Store assets with an accurate privacy policy
- Beta testing
- Launch checklist
- Public release process

At this point, Walris is no longer just a working MVP.

It is a real mobile application with a production backend, production database, launch process,
and early feedback loop.

---

## Roadmap Complete

The complete Walris roadmap now covers:

- Part 1 — Foundation
- Part 2 — Core Backend
- Part 3 — Mobile App
- Part 4 — Notifications, QA, Deployment & Launch

The recommended implementation order remains:

```text
Foundation
  ↓
Backend Intelligence Engine
  ↓
Mobile Experience
  ↓
Notifications + Launch Polish
```

The most important rule:

> Do not skip directly to UI polish before the backend briefing pipeline works.

Walris becomes valuable only when it reliably generates clear, trustworthy economic briefings.
