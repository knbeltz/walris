# Walris

Walris is a mobile-first economic intelligence app. Every morning it generates a briefing of the
top five macroeconomic events, explaining what happened, why it matters, how unusual it is
historically, how financial media is interpreting it, and who is most affected.

Walris is not a trading app or a news firehose. It's an interpretation layer: a curated, calm,
editorial-style briefing designed to be read in under five minutes.

## Tech Stack

**Frontend** — React Native, Expo, TypeScript, NativeWind, React Native Reusables, Expo Router,
TanStack Query, Zod

**Backend** — FastAPI, Python, Pydantic, SQLAlchemy, Alembic

**Database** — Supabase PostgreSQL

**External APIs** — Finnhub (economic calendar), FRED (historical data), Marketaux (news),
OpenAI (ranking/summaries), Expo Notifications (push)

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
- [`05-engineering-journal.md`](docs/05-engineering-journal.md) — running engineering journal (living document)
- [`06-resume-prompt.md`](docs/06-resume-prompt.md) — current project status, for resuming work
- [`07-learning-notes.md`](docs/07-learning-notes.md) — concepts and debugging lessons worth remembering (living document)
- [`08-code-reference-milestones-3-6-9.md`](docs/08-code-reference-milestones-3-6-9.md) — snapshot of the code Claude wrote for Milestones 3/6/9, for study (not a template to copy forward — see the working agreement in `06-resume-prompt.md`)

## Status

In active development, following the roadmap in `docs/03-development-roadmap.md`. See
`docs/06-resume-prompt.md` for the current milestone and next steps.
