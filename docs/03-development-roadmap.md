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

Unchanged from the original scope: safe area handling, page container, scroll layout, standard
spacing and margins, reusable across every future screen.

## Milestone 29 — Daily Briefing Header

App name, current date, and the signed-in user's name/greeting where relevant — replaces the old
generic version, which had no concept of a signed-in user to greet.

## Milestone 30 — Key Indicator Chart Component

Replaces the old "Basic Historical Chart" (previously an event-detail-page feature, Milestone 38).
Now a Home Screen building block: a lightweight chart rendering one or more of the FRED indicators
referenced in that day's personalized narrative, rather than a chart tied to one discrete event.

## Milestone 31 — Supporting News Cards

Replaces "News Article Cards" (previously Milestone 37, tied to an individual event's detail page).
Cards linking out to the source Marketaux articles behind that day's personalized narrative.

## Milestone 32 — Home Screen

Assembles Milestones 29-31 into the actual home screen: header, the AI-generated narrative,
supporting key-indicator chart(s), supporting news cards, loading/empty/error states, and
pull-to-refresh. Replaces the old "top 5 event list" home screen entirely — there's no per-event
navigation, since Milestones 35/36 from the original Part 3 (event detail route + content sections)
no longer apply under this model.

## Milestone 33 — Empty, Error, and Loading States

Unchanged in concept from the original scope: resilient UI for no-briefing-yet, backend-unavailable,
and loading states, with a consistent way to retry failed requests.

## Milestone 34 — Mobile Integration Test Pass

Unchanged in concept from the original scope: end-to-end verification of the full personalized
flow — sign-in → onboarding (category/topics) → home screen fetch → real backend data — on both
iOS and Android, including the backend-down state.

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

Unchanged from the original scope (`expo-notifications`/`expo-device`, permission request, Expo
push token retrieval, physical-device handling) — this is client-side capability work that never
depended on the event-vs-personalization model.

## Milestone 36 — Device Token Registration API

Replaces "Notification Token API." Since V1 requires authentication before the app is usable at
all, there's no anonymous-token flow to build anymore — `POST /v1/notifications/register` is an
authenticated endpoint (same `get_current_user` pattern as the preferences endpoint), storing the
token against `device_tokens.user_id` directly at registration time rather than registering
anonymously and linking later.

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
