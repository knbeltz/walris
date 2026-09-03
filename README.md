# Walris

Walris is a mobile-first economic intelligence app. Users sign up, pick one of seven categories
(Investors, Small Business Owners/Entrepreneurs, Consumers, Home Owners/Home Buyers, Students,
Job Seekers, or "I Want Everything") plus any additional topics they want, and get an individually
generated daily briefing explaining what happened in the economy, why it matters, and who's most
affected — built from FRED, Financial Modeling Prep, and Marketaux data, enriched with AI.

Walris is not a trading app or a news firehose. It's an interpretation layer: a curated, calm,
editorial-style briefing designed to be read in under five minutes.

## Tech Stack

**Frontend** — React Native, Expo, TypeScript, NativeWind, React Native Reusables, Expo Router,
TanStack Query, Zod, Clerk (auth)

**Backend** — FastAPI, Python, Pydantic, SQLAlchemy, Alembic, fastapi-clerk-auth

**Database** — Supabase PostgreSQL

**External APIs** — FRED (macroeconomic indicators), Financial Modeling Prep (market data),
Marketaux (news), OpenAI (personalized briefing generation), Clerk (authentication),
Expo Notifications (push)

## Project Structure

```text
walris/
  mobile/    React Native + Expo app (scaffolded in Milestone 4)
  backend/   FastAPI backend (scaffolded in Milestone 3)
  docs/      Full project documentation (see below)
```

## Documentation

Full documentation lives in [`docs/`](docs/):

- [`01-product-requirements.md`](docs/01-product-requirements.md) — product vision, philosophy, and problem statement
- [`02-system-architecture.md`](docs/02-system-architecture.md) — system architecture and data flows
- [`03-development-roadmap.md`](docs/03-development-roadmap.md) — the milestone-by-milestone build plan
- [`04-design-system.md`](docs/04-design-system.md) — visual design system and content style
- [`05-resume-prompt.md`](docs/05-resume-prompt.md) — current project status, for resuming work
- [`06-learning-notes.md`](docs/06-learning-notes.md) — concepts and debugging lessons worth remembering (living document)
- [`07-code-reference-milestones-3-6-9.md`](docs/07-code-reference-milestones-3-6-9.md) — snapshot of the code Claude wrote for Milestones 3/6/9, for study (not a template to copy forward — see the working agreement in `05-resume-prompt.md`)
- [`08-personalization-pivot-plan.md`](docs/08-personalization-pivot-plan.md) — the personalization pivot plan (per-user categories/topics, Clerk auth, the FRED/FMP/Marketaux/OpenAI data pipeline) and the milestone breakdown that replaced the original roadmap's Milestones 13-24

## Status

In active development. **Milestones 1-29 and 31-33 are complete** — the entire backend build for the
personalization pivot: backend foundation, Supabase, CI, user accounts via Clerk, category/topic
selection, the FRED/Marketaux fetch services, a full fetch-filter-persist-cleanup pipeline for
daily market/news data, per-user OpenAI briefing generation, the daily briefing orchestrator tying
it all together with per-run tracking, the personalized briefing API endpoint, personalized push
notifications, a full integration test pass, and an admin-triggered automation surface for the
daily jobs — all verified end-to-end against live APIs, the live OpenAI API, the live Expo push
API, and the live database, including a real weekday run on 2026-08-17 confirming real notification
deactivation. Milestone 21's mobile registration flow is deliberately deferred to the Mobile App
phase. Wiring M23's admin endpoints to an actual hosted cron schedule is deferred to Milestone 42,
once the backend has a real deployment to point one at. **Milestones 24 through 29 and 31-33, the
start of the Mobile App phase, are all complete** — a shared, authenticated fetch wrapper
(`mobile/lib/apiClient.ts`), Zod schemas (`mobile/schemas/`) validating the briefing, preferences,
and news API responses, a `useTodayBriefing` TanStack Query hook, typography/spacing/radius theme
tokens (`mobile/theme/`), a shared `Screen` layout component, the actual Home Screen —
personalized narrative, supporting news cards, sign-in/sign-out, and pull-to-refresh — and real,
designed empty/error/loading states with working retry, all verified end-to-end on a physical
device. **Milestone 30 (Key Indicator Chart Component) is deferred, not part of V1** — the
underlying indicator data is shipped and available, but a chart wasn't judged worth building yet
given how sparse the historical data still is. Next up: Milestone 34 (Mobile Integration Test
Pass). See `docs/05-resume-prompt.md` for the current milestone and next steps.
