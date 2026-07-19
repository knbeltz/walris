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
mapping: `docs/09-personalization-pivot-plan.md`. Summary of each milestone below; expand each
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
`docs/09-personalization-pivot-plan.md` §5.

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

After Milestone 23 (of the personalization pivot — see `docs/09-personalization-pivot-plan.md`),
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
**note: the milestone numbers below (formerly 27+) have not been renumbered to close the gap left
by replacing the old 12-milestone event pipeline with this pivot's 11 milestones (13-23). More
importantly, Milestones 27-45 as written still assume no authentication and one shared global
briefing throughout — they need their own re-scoping pass against this pivot (sign-up/onboarding
screens, per-user data fetching, personalized notification copy) before being started as-is. Don't
treat the content below as current without that review.**

---

# Walris Development Roadmap

**Document:** docs/03-development-roadmap.md
**Version:** 1.0
**Phase:** Part 3 – Mobile App

---

## Part 3 Overview

Part 3 builds the mobile experience that users will actually interact with.

By the end of this phase, the React Native app should be able to:

- Fetch today's briefing from the FastAPI backend
- Display the top 5 economic events
- Show event detail pages
- Render loading, empty, and error states
- Apply the Walris design system
- Validate backend API responses with Zod
- Feel polished enough for early beta testing

---

## Milestone 27 — Mobile API Client

### Objective

Create the frontend API layer that communicates with the FastAPI backend.

### Deliverables

Create:

```text
mobile/lib/api.ts
mobile/lib/apiClient.ts
mobile/lib/env.ts
```

Implement:

- Base API client
- Environment-based API URL
- Request helper
- Error handling
- Timeout handling

### Acceptance Criteria

- Mobile app can call the backend reliably.
- API base URL comes from environment config.
- Failed requests return controlled errors.
- No external API keys exist in the mobile app.

### Definition of Done

The mobile app has a clean API layer and does not call backend endpoints directly from UI
components.

### Suggested Commit

`feat: add mobile API client`

### Claude Code Tutor Prompt

> Help me build a clean API client for the Walris React Native app. Explain how to separate API
> logic from UI components and how to safely handle request failures.

---

## Milestone 28 — Frontend Response Schemas

### Objective

Add runtime validation for backend responses.

### Deliverables

Create:

```text
mobile/lib/schemas/briefing.ts
mobile/lib/schemas/event.ts
mobile/lib/schemas/news.ts
```

Use Zod to validate:

- Today briefing response
- Event detail response
- News article objects
- Error responses

### Acceptance Criteria

- API responses are validated before entering UI.
- Invalid backend responses produce controlled app errors.
- TypeScript types are inferred from Zod schemas.

### Definition of Done

The mobile app has runtime type safety for all backend API responses.

### Suggested Commit

`feat: add frontend API response validation`

### Claude Code Tutor Prompt

> Help me define Zod schemas for Walris API responses. Explain the difference between TypeScript
> compile-time safety and runtime validation.

---

## Milestone 29 — TanStack Query Hooks

### Objective

Create reusable data-fetching hooks.

### Deliverables

Create:

```text
mobile/hooks/useTodayBriefing.ts
mobile/hooks/useEventDetail.ts
```

Implement:

- `useTodayBriefing`
- `useEventDetail`
- Loading state support
- Error state support
- Refetch behavior

### Acceptance Criteria

- Screens consume data through hooks, not raw API calls.
- Loading and error states are exposed clearly.
- Query keys are stable and predictable.

### Definition of Done

Frontend data fetching is centralized and reusable.

### Suggested Commit

`feat: add briefing query hooks`

### Claude Code Tutor Prompt

> Help me build TanStack Query hooks for today's briefing and event detail data. Explain query
> keys, caching, loading states, and error states.

---

## Milestone 30 — Walris Theme Tokens

### Objective

Implement the Walris design system in the mobile app.

### Deliverables

Create:

```text
mobile/theme/colors.ts
mobile/theme/typography.ts
mobile/theme/spacing.ts
mobile/theme/radius.ts
```

Implement design tokens from the Walris design file:

- Background colors
- Surface colors
- Text colors
- Primary colors
- Data green
- Alert red
- Border colors
- Spacing scale
- Radius scale
- Typography references

### Acceptance Criteria

- Design tokens are centralized.
- Components do not hardcode colors or spacing.
- Theme values match the approved Walris design direction.

### Definition of Done

The app has a reusable visual foundation.

### Suggested Commit

`feat: implement Walris theme tokens`

### Claude Code Tutor Prompt

> Help me translate the Walris design system into reusable React Native theme tokens. Explain how
> design tokens prevent inconsistent UI.

---

## Milestone 31 — App Layout Shell

### Objective

Create the base mobile application layout.

### Deliverables

Implement:

- Safe area handling
- App background
- Page container
- Scroll layout
- Standard horizontal margins
- Header spacing

Create:

```text
mobile/components/layout/AppScreen.tsx
mobile/components/layout/PageHeader.tsx
```

### Acceptance Criteria

- Screens respect safe areas.
- Layout works on small and large phones.
- Content spacing follows the 8px design scale.
- No screen content touches device edges.

### Definition of Done

All future screens can reuse a shared layout system.

### Suggested Commit

`feat: add mobile layout shell`

### Claude Code Tutor Prompt

> Help me create a reusable mobile layout shell for Walris. Explain safe areas, spacing, and why
> layout components should be reusable.

---

## Milestone 32 — Daily Briefing Header

### Objective

Build the top section of the home screen.

### Deliverables

Create: `mobile/components/briefing/DailyBriefingHeader.tsx`

Displays:

- Walris name
- Current date
- Briefing title
- Daily summary
- Last generated timestamp if available

### Acceptance Criteria

- Header renders real API data.
- Typography follows design system.
- Layout is readable on small phones.
- Missing summary values are handled gracefully.

### Definition of Done

The home screen has a polished editorial-style briefing header.

### Suggested Commit

`feat: add daily briefing header`

### Claude Code Tutor Prompt

> Help me build the DailyBriefingHeader component for Walris. Focus on clean component props,
> typography hierarchy, and mobile readability.

---

## Milestone 33 — Event Card Component

### Objective

Build the reusable card for economic events.

### Deliverables

Create: `mobile/components/events/EventCard.tsx`

Event card displays:

- Event name
- Country
- Release time
- Importance score
- Actual value
- Forecast value
- Previous value
- Plain-English summary
- Affected group chips

### Acceptance Criteria

- Card renders real event data.
- Missing actual/forecast/previous values are handled.
- Importance score is visually clear.
- Card is touchable and navigates to event detail.

### Definition of Done

The primary content unit of the app is complete.

### Suggested Commit

`feat: add economic event card component`

### Claude Code Tutor Prompt

> Help me build the EventCard component for Walris. Explain how to design a reusable, data-rich
> card without making the UI feel crowded.

---

## Milestone 34 — Home Screen

### Objective

Assemble the main app experience.

### Deliverables

Implement: `mobile/app/index.tsx`

Home screen includes:

- Daily briefing header
- Top 5 event list
- Loading state
- Error state
- Empty state
- Pull-to-refresh

### Acceptance Criteria

- Home screen fetches `/briefings/today`.
- Top 5 events render correctly.
- User can refresh manually.
- User can tap an event card.
- Screen handles no briefing available.

### Definition of Done

Users can open Walris and view today's briefing.

### Suggested Commit

`feat: build today briefing home screen`

### Claude Code Tutor Prompt

> Help me build the Walris home screen using the data-fetching hooks and reusable components.
> Explain how to structure loading, error, empty, and success states.

---

## Milestone 35 — Event Detail Screen Structure

### Objective

Create the detail route and screen shell for individual economic events.

### Deliverables

Create: `mobile/app/event/[id].tsx`

Implement:

- Route parameter handling
- Event detail query
- Loading state
- Error state
- Back navigation
- Scroll layout

### Acceptance Criteria

- Event detail screen opens from event card.
- Correct event ID is passed through navigation.
- Screen fetches `/events/{event_id}`.
- Loading and error states render correctly.

### Definition of Done

Navigation from home to event detail works end to end.

### Suggested Commit

`feat: add event detail route`

### Claude Code Tutor Prompt

> Help me build the event detail route using Expo Router. Explain dynamic routing, route params,
> and how to fetch data for detail screens.

---

## Milestone 36 — Event Detail Content Components

### Objective

Build the content sections used on the event detail page.

### Deliverables

Create:

```text
mobile/components/events/EventDataPanel.tsx
mobile/components/events/ImportanceSection.tsx
mobile/components/events/HistoricalContextSection.tsx
mobile/components/events/NewsContextSection.tsx
mobile/components/events/AffectedGroupsSection.tsx
```

Sections display:

- Actual vs forecast vs previous
- Importance explanation
- Plain-English summary
- Historical context
- News context
- Affected groups

### Acceptance Criteria

- Each section is reusable and independently testable.
- Missing optional data does not break rendering.
- Data values use JetBrains Mono styling where appropriate.
- Section hierarchy is easy to scan.

### Definition of Done

Event detail screen has all core explanatory content.

### Suggested Commit

`feat: build event detail content sections`

### Claude Code Tutor Prompt

> Help me build modular event detail components for Walris. Explain how to break a complex detail
> page into maintainable sections.

---

## Milestone 37 — News Article Cards

### Objective

Display related Marketaux articles on the event detail page.

### Deliverables

Create:

```text
mobile/components/news/NewsArticleCard.tsx
mobile/components/news/RelatedArticlesList.tsx
```

Article card displays:

- Headline
- Source
- Published time
- Summary
- Sentiment or topic chips if available
- External link behavior

### Acceptance Criteria

- Related articles render correctly.
- Tapping an article opens the URL in browser.
- Missing article metadata is handled.
- Article cards match Walris editorial style.

### Definition of Done

Users can view and open supporting news coverage.

### Suggested Commit

`feat: add related news article cards`

### Claude Code Tutor Prompt

> Help me build related news article components for Walris. Explain best practices for linking
> out to external articles from a mobile app.

---

## Milestone 38 — Basic Historical Chart

### Objective

Add a simple chart for FRED historical context.

### Deliverables

Choose a lightweight charting library compatible with Expo.

Create: `mobile/components/charts/HistoricalLineChart.tsx`

Chart should show:

- Historical FRED values
- Latest value
- Simple trend visualization

### Acceptance Criteria

- Chart renders on iOS and Android.
- Chart handles empty data.
- Chart does not slow down the detail screen.
- Data labels remain readable on phones.

### Definition of Done

Event detail pages can show historical context visually.

### Suggested Commit

`feat: add historical line chart`

### Claude Code Tutor Prompt

> Help me add a simple historical line chart to Walris. Explain how to choose a React Native
> charting library and keep the chart performant.

---

## Milestone 39 — Empty, Error, and Loading States

### Objective

Make the app resilient and user-friendly when data is missing or delayed.

### Deliverables

Create:

```text
mobile/components/states/LoadingState.tsx
mobile/components/states/ErrorState.tsx
mobile/components/states/EmptyState.tsx
```

Implement states for:

- Home screen loading
- Home screen no briefing
- Backend unavailable
- Event detail loading
- Event not found
- No related news
- No FRED historical data

### Acceptance Criteria

- No blank screens exist.
- All known failure states show helpful UI.
- User can retry failed requests.
- States use consistent design language.

### Definition of Done

The app behaves gracefully when things go wrong.

### Suggested Commit

`feat: add mobile loading and error states`

### Claude Code Tutor Prompt

> Help me design loading, empty, and error states for Walris. Explain how resilient UI improves
> perceived product quality.

---

## Milestone 40 — Mobile Integration Test Pass

### Objective

Verify the mobile app works end to end with the backend.

### Deliverables

Test:

- Home screen fetch
- Event card rendering
- Event detail navigation
- Event detail fetch
- News links
- Loading state
- Error state
- Empty state
- Pull-to-refresh

### Acceptance Criteria

- App works on iOS simulator.
- App works on Android emulator.
- App handles backend down state.
- App renders real backend data correctly.

### Definition of Done

Walris mobile app is ready for notification implementation and visual polish.

### Suggested Commit

`test: validate mobile app integration`

### Claude Code Tutor Prompt

> Help me test the Walris mobile app end to end. I want to verify real backend integration,
> navigation, loading states, and error states before adding notifications.

---

## Mobile App Phase Complete

After Milestone 40, Walris will have:

- React Native frontend API layer
- Runtime response validation with Zod
- TanStack Query data fetching
- Walris theme tokens
- Home screen
- Daily briefing header
- Event cards
- Event detail screen
- Historical chart
- Related news cards
- Loading, empty, and error states
- End-to-end mobile/backend integration

At this point, Walris should feel like a real mobile product.

The next phase should focus on:

- Push notifications
- QA
- Performance
- Polish
- Deployment
- App Store / Google Play preparation

---

# Walris Development Roadmap

**Document:** docs/03-development-roadmap.md
**Version:** 1.0
**Phase:** Part 4 – Notifications, QA, Deployment & Launch

---

## Part 4 Overview

Part 4 turns Walris from a working prototype into a launch-ready mobile application.

By the end of this phase, Walris should have:

- Morning push notifications
- Anonymous device token storage
- Production backend deployment
- Production database configuration
- App Store / Google Play readiness
- QA testing
- Error monitoring
- Performance checks
- Release checklist

---

## Milestone 41 — Expo Notifications Setup

### Objective

Configure push notifications in the React Native app.

### Deliverables

Install and configure: `expo-notifications`, `expo-device`

Implement:

```text
mobile/lib/notifications.ts
mobile/hooks/usePushNotifications.ts
```

Capabilities:

- Request notification permission
- Get Expo push token
- Detect platform
- Handle permission denied state
- Handle physical device requirement

### Acceptance Criteria

- App can request notification permission.
- App can retrieve Expo push token on a physical device.
- App handles denied permissions gracefully.
- No notification logic is hardcoded inside UI screens.

### Definition of Done

The mobile app can register for push notifications.

### Suggested Commit

`feat: configure Expo push notifications`

### Claude Code Tutor Prompt

> Help me configure Expo push notifications for Walris. Explain how push tokens work, why
> physical devices are required, and how to keep notification logic separate from UI components.

---

## Milestone 42 — Notification Token API

### Objective

Create backend support for storing anonymous device push tokens.

### Deliverables

Create endpoint: `POST /notifications/register`

Request body:

```text
expo_push_token
device_id
platform
timezone
```

Backend should:

- Validate token payload with Pydantic
- Store token in Supabase
- Avoid duplicate active tokens
- Update existing token records when needed

### Acceptance Criteria

- Push token can be stored from mobile app.
- Duplicate tokens are not repeatedly inserted.
- Invalid token requests return controlled errors.
- No user authentication is required.

### Definition of Done

Walris can persist anonymous device notification tokens.

### Suggested Commit

`feat: add notification token registration endpoint`

### Claude Code Tutor Prompt

> Help me build the notification token registration endpoint for Walris. Explain how to store
> anonymous device tokens safely without user authentication.

---

## Milestone 43 — Notification Registration Flow

### Objective

Connect mobile notification registration to the backend.

### Deliverables

Implement mobile flow:

```text
App opens
  ↓
Ask permission at appropriate moment
  ↓
Get Expo push token
  ↓
POST token to FastAPI
  ↓
Store registration status locally
```

Use local storage to avoid asking repeatedly.

Recommended library: `@react-native-async-storage/async-storage`

### Acceptance Criteria

- Users are not spammed with permission prompts.
- Granted tokens are sent to backend.
- Denied permissions do not break the app.
- Registration status persists across app restarts.

### Definition of Done

Push notification registration works end to end.

### Suggested Commit

`feat: connect push token registration flow`

### Claude Code Tutor Prompt

> Help me implement the full push notification registration flow in the mobile app. Explain when
> to ask for permission and how to avoid annoying users.

---

## Milestone 44 — Morning Notification Sender

### Objective

Send the daily morning push notification.

### Deliverables

Create backend service: `services/notification_service.py`

Service should:

- Fetch active device tokens
- Send Expo push notifications
- Handle failed tokens
- Mark invalid tokens inactive
- Log notification results

Notification copy:

> View this morning's top 5 economic events.

### Acceptance Criteria

- Notification can be sent to registered devices.
- Failed sends are logged.
- Invalid tokens are handled.
- Notification opens app to home screen.

### Definition of Done

Walris can send the morning briefing notification.

### Suggested Commit

`feat: add morning notification sender`

### Claude Code Tutor Prompt

> Help me build the notification sending service for Walris. Explain Expo push notification
> delivery, invalid tokens, retries, and logging.

---

## Milestone 45 — Notification Schedule

### Objective

Automate the morning notification job.

### Deliverables

Schedule notification job for: 7:00 AM ET daily

Notification should only send if:

- Today's briefing exists
- Briefing status is complete
- At least one event exists
- Active device tokens exist

### Acceptance Criteria

- Notification job runs automatically.
- Job does not send when briefing is missing.
- Job execution is logged in `job_runs`.
- Manual trigger exists for testing.

### Definition of Done

Morning notifications are automated.

### Suggested Commit

`feat: schedule morning briefing notifications`

### Claude Code Tutor Prompt

> Help me schedule the morning notification job. Explain how to ensure notifications only send
> after today's briefing has been generated successfully.

---

## Milestone 46 — Backend QA & Error Handling

### Objective

Harden the backend before production deployment.

### Deliverables

Review and improve:

- External API failure handling
- OpenAI failure handling
- Database error handling
- Job failure logging
- Empty briefing responses
- Invalid event IDs
- Admin endpoint protection

Add tests for:

```text
GET /health
GET /briefings/today
GET /events/{event_id}
POST /notifications/register
```

### Acceptance Criteria

- Backend does not crash from expected external API failures.
- Missing data produces controlled responses.
- Admin endpoints require secret protection.
- Tests pass locally and in CI.

### Definition of Done

Backend is stable enough for staging deployment.

### Suggested Commit

`test: harden backend error handling`

### Claude Code Tutor Prompt

> Help me QA the Walris backend. Walk me through expected failure modes and help me write tests
> for the most important endpoints.

---

## Milestone 47 — Mobile QA & Device Testing

### Objective

Test the mobile application on realistic devices and screen sizes.

### Deliverables

Test on:

- Small iPhone
- Large iPhone
- Common Android phone
- iOS simulator
- Android emulator
- Physical device for notifications

Scenarios:

- First app open
- Briefing loaded
- No briefing available
- Backend unavailable
- Event detail open
- No news articles
- No FRED data
- Notification permission granted
- Notification permission denied

### Acceptance Criteria

- No major UI breakage on supported phones.
- App does not crash during expected failure states.
- Notification registration works on physical device.
- Touch targets are usable.

### Definition of Done

Mobile app is ready for beta distribution.

### Suggested Commit

`test: complete mobile QA pass`

### Claude Code Tutor Prompt

> Help me create and run a mobile QA checklist for Walris. Focus on real-device testing, screen
> sizes, loading states, error states, and notification behavior.

---

## Milestone 48 — Production Backend Deployment

### Objective

Deploy FastAPI backend to production.

### Recommended Options

Use one: Render, Railway, Fly.io

Deliverables:

- Production backend URL
- Environment variables configured
- Database connection verified
- Health endpoint verified
- Admin secret configured
- Scheduled jobs configured

### Acceptance Criteria

- Production `/health` endpoint returns success.
- Backend can connect to Supabase.
- External API keys work in production.
- Scheduled briefing job can run in production.
- Logs are accessible.

### Definition of Done

Walris backend is live.

### Suggested Commit

`chore: deploy backend to production`

### Claude Code Tutor Prompt

> Help me deploy the Walris FastAPI backend to production. Explain environment variables,
> production logging, health checks, and deployment tradeoffs.

---

## Milestone 49 — Production Supabase Configuration

### Objective

Prepare Supabase for production use.

### Deliverables

Configure:

- Production schema
- Database indexes
- Secure service role usage
- Backups
- Connection pooling if needed
- Migration workflow

Confirm tables:

```text
briefings
economic_events
enriched_events
fred_series
news_articles
device_tokens
job_runs
```

### Acceptance Criteria

- Production database schema matches migrations.
- Backend can read/write production data.
- No service role key exists in mobile app.
- Basic indexes exist for date/event queries.

### Definition of Done

Supabase production database is ready.

### Suggested Commit

`chore: configure production Supabase database`

### Claude Code Tutor Prompt

> Help me prepare Supabase for production. Explain database security, indexes, migrations,
> backups, and why service role keys must never be exposed to the mobile app.

---

## Milestone 50 — Mobile Production Configuration

### Objective

Prepare the Expo app for production builds.

### Deliverables

Configure:

- `app.json` / `app.config.ts`
- `eas.json`
- production API base URL
- app icon
- splash screen
- bundle identifiers
- Android package name
- iOS bundle ID

### Acceptance Criteria

- App points to production backend.
- App has production app name: Walris.
- App icon and splash screen are configured.
- EAS build config exists.

### Definition of Done

Mobile app can be built for iOS and Android production.

### Suggested Commit

`chore: configure Expo production builds`

### Claude Code Tutor Prompt

> Help me configure Expo and EAS for production builds. Explain bundle identifiers, app icons,
> splash screens, and environment-specific API URLs.

---

## Milestone 51 — Analytics & Basic Monitoring

### Objective

Add basic visibility into user behavior and system health.

### Recommended MVP Analytics

Use one: PostHog, Expo Analytics-compatible tool, Firebase Analytics

Track:

```text
app_opened
briefing_viewed
event_card_tapped
event_detail_viewed
news_article_opened
notification_permission_granted
notification_permission_denied
notification_opened
```

Backend monitoring should track:

```text
briefing_job_success
briefing_job_failure
notification_job_success
notification_job_failure
external_api_failure
openai_validation_failure
```

### Acceptance Criteria

- Basic product events are tracked.
- Backend job failures are observable.
- Analytics do not store sensitive personal information.

### Definition of Done

Walris has minimal analytics and monitoring for beta testing.

### Suggested Commit

`feat: add basic analytics and monitoring`

### Claude Code Tutor Prompt

> Help me add lightweight analytics and monitoring to Walris. Explain which product events matter
> for an MVP and how to avoid collecting unnecessary personal data.

---

## Milestone 52 — Performance Pass

### Objective

Ensure the app feels fast and reliable.

### Target Performance

```text
Home briefing load: under 2 seconds
Event detail load: under 2 seconds
Cold app open: under 3 seconds
Backend health check: under 300ms
Briefing generation: under 5 minutes
```

Review:

- API response size
- Query performance
- Image usage
- Chart rendering
- Network error handling
- Loading skeletons
- Pull-to-refresh behavior

### Acceptance Criteria

- Home screen loads quickly with production backend.
- Event detail screen loads quickly.
- No unnecessary external API calls happen from mobile.
- Backend uses cached/pre-generated briefing data.

### Definition of Done

Walris meets MVP performance expectations.

### Suggested Commit

`perf: optimize app and backend performance`

### Claude Code Tutor Prompt

> Help me run a performance pass on Walris. Explain how to identify slow frontend rendering, slow
> API responses, and unnecessary network requests.

---

## Milestone 53 — App Store Assets

### Objective

Prepare required assets for Apple App Store and Google Play.

### Deliverables

Create:

- App icon
- Splash screen
- App screenshots
- App description
- Short description
- Keywords
- Support URL
- Privacy policy URL
- Marketing tagline

Example tagline:

> Understand today's economy in under five minutes.

### Acceptance Criteria

- Required assets exist for both stores.
- App description clearly communicates value.
- Privacy policy explains anonymous notification token storage.
- Screenshots show real app UI.

### Definition of Done

Walris is ready for store listing creation.

### Suggested Commit

`docs: add app store launch assets`

### Claude Code Tutor Prompt

> Help me prepare App Store and Google Play launch assets for Walris. Explain what assets are
> required and how to write a clear app description.

---

## Milestone 54 — Beta Distribution

### Objective

Distribute Walris to a small group of testers.

### Deliverables

Use: TestFlight for iOS, Google Play Internal Testing for Android

Recruit testers:

- Economics students
- Finance students
- Retail investors
- Curious professionals
- Friends who follow business news

Collect feedback on:

- Clarity
- Usefulness
- Trust
- Visual design
- Notification timing
- Confusing language
- Missing context

### Acceptance Criteria

- At least 10 users test the app.
- Feedback is collected in one document.
- Bugs are triaged.
- Product feedback is separated from technical bugs.

### Definition of Done

Walris has completed first external beta test.

### Suggested Commit

`docs: add beta testing feedback plan`

### Claude Code Tutor Prompt

> Help me plan Walris beta testing. Explain how to recruit testers, collect structured feedback,
> and separate bugs from product insights.

---

## Milestone 55 — Launch Readiness Checklist

### Objective

Confirm Walris is ready for public submission.

### Checklist

**Product:**

- Home screen works
- Event detail works
- Morning notification works
- No-auth experience works
- Loading/error states work

**Backend:**

- Production backend live
- Daily briefing job runs
- Notification job runs
- External APIs work
- Logs available

**Database:**

- Production Supabase ready
- Indexes added
- Backups configured
- No secrets exposed

**Mobile:**

- iOS build passes
- Android build passes
- App icon configured
- Splash screen configured
- Production API URL configured

**Legal / Store:**

- Privacy policy
- Support URL
- Store screenshots
- App description
- Age rating
- Data collection disclosure

### Acceptance Criteria

- No known launch-blocking bugs.
- Beta feedback has been reviewed.
- App can be submitted to Apple and Google.

### Definition of Done

Walris is launch-ready.

### Suggested Commit

`docs: add launch readiness checklist`

### Claude Code Tutor Prompt

> Help me run a final launch readiness review for Walris. Act like a senior engineer and product
> manager reviewing whether the app is ready for App Store submission.

---

## Milestone 56 — Public Launch

### Objective

Submit Walris to the App Store and Google Play.

### Deliverables

Submit:

- Apple App Store build
- Google Play build
- Store listing metadata
- Screenshots
- Privacy disclosures

Post-launch monitor:

- Crashes
- Backend errors
- Daily job success
- Notification delivery
- User feedback
- App reviews

### Acceptance Criteria

- App submitted successfully.
- Review issues are addressed if returned.
- Production monitoring is active.
- Post-launch feedback collection begins.

### Definition of Done

Walris is publicly available or pending approval.

### Suggested Commit

`chore: prepare public launch`

### Claude Code Tutor Prompt

> Help me prepare Walris for public launch. Explain what to monitor immediately after launch and
> how to respond to App Store or Google Play review issues.

---

## Part 4 Complete

After Milestone 56, Walris will have:

- Push notification registration
- Morning notification delivery
- Backend QA
- Mobile QA
- Production backend
- Production Supabase setup
- Production Expo builds
- Basic analytics
- Performance validation
- App Store assets
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
