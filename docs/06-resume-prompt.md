# Walris Resume Prompt

**Document:** docs/06-resume-prompt.md
**Last Updated:** 2026-07-08 (Milestone 3 complete)
**Status:** Living Document — update at the end of every milestone

This document is the current state of the Walris project. Read it before making assumptions in a
new session.

---

## Current Project Status

Walris exists as a GitHub repository with a scaffolded folder layout, complete project
documentation, and a minimal but working FastAPI backend (`uvicorn app.main:app --reload` starts
successfully; `GET /health` returns HTTP 200). No mobile app code has been written yet — that's
Milestone 4.

- GitHub repo: https://github.com/knbeltz/walris (private)
- Local path: `/Users/kaibeltz/Desktop/Coding Projects/walris`

## Completed Milestones

- [x] **Milestone 1 — Repository & Project Setup**
- [x] **Milestone 2 — Documentation Foundation**
- [x] **Milestone 3 — Backend Foundation**
- [ ] Milestone 4 — React Native Foundation
- [ ] Milestone 5 — Development Environment
- [ ] Milestone 6 — Supabase Setup
- [ ] Milestone 7 — Configuration System
- [ ] Milestone 8 — Continuous Integration
- [ ] Milestone 9 — API Foundation
- [ ] Milestone 10 — First End-to-End Connection
- [ ] Milestones 11–26 — Core Backend (Part 2)
- [ ] Milestones 27–40 — Mobile App (Part 3)
- [ ] Milestones 41–56 — Notifications, QA, Deployment & Launch (Part 4)

## Current Milestone

**Milestone 4 — React Native Foundation** (not started)

- Goal: Initialize the Expo project (TypeScript) inside `mobile/`, install Expo Router,
  NativeWind, React Native Reusables, and TanStack Query, and implement a basic home screen,
  navigation foundation, and theme configuration.
- Progress: Not started. `mobile/` currently only contains the placeholder `README.md`.
- **Resume here:** Phase 1 (Understand the Milestone) for Milestone 4, following the same
  workflow used for Milestone 3 (understand → edge cases → pseudocode → implementation → review →
  refactor → sign off). Note from `docs/06-resume-prompt.md`'s Milestone 1 note: `mobile/` was
  deliberately left empty specifically so `create-expo-app` has a clean target — don't
  pre-create a `package.json` by hand.

### Milestone 3 — Backend Foundation (complete)

Full mentor workflow (Phases 1–7) was followed end to end. Summary for future reference:

- **Phase 2 design decisions** (still governing backend architecture going forward):
  - **Fail-fast config:** a `Settings` object (Pydantic `BaseSettings`) is instantiated once at
    module import time in `app/core/config.py`. Invalid/missing required fields raise
    immediately at startup rather than failing later inside a request handler.
  - **`core/` vs `utils/`:** `core/` holds app-specific foundational pieces that know about
    Walris (settings/config loader, logging setup). `utils/` holds generic, stateless helpers
    with zero app-specific knowledge — the test is "would this still make sense copy-pasted into
    an unrelated Python project?"
  - **`main.py` scope:** thin entrypoint only — wires settings/logging/app/routers together. No
    route handlers, business logic, or config parsing living directly in it.
- **What got built:** `backend/app/core/config.py` (Settings with a `Literal["development",
  "production"]` environment field, defaulting to `"development"`), `backend/app/core/logging.py`
  (`configure_logging`, DEBUG in dev / INFO otherwise), `backend/app/routers/health.py` (`GET
  /health` → `{"status": "ok"}`), `backend/app/main.py` (wires the above together in order:
  settings → logging → app → routers). Empty `services/`, `schemas/`, `models/` packages exist
  as placeholders for Milestones 11–24.
- **Verified working:** `uvicorn app.main:app --reload` starts with no env vars set (defaults to
  `"development"`); `GET /health` returns `200 {"status": "ok"}`; `ENVIRONMENT=production` loads
  correctly; `ENVIRONMENT=staging` (invalid) correctly fails fast with a Pydantic
  `ValidationError` before the server starts.
- **Python 3.14 resolved:** all Milestone 3 dependencies (fastapi, uvicorn, pydantic-settings,
  and their compiled sub-dependencies like pydantic-core, httptools, uvloop, watchfiles) installed
  cleanly with prebuilt 3.14 wheels — no need to switch Python versions.

## Important Decisions

- Monorepo: `mobile/` and `backend/` live in one repository (see Engineering Journal Decision Log
  for full rationale).
- Backend: FastAPI + Pydantic + SQLAlchemy + Alembic.
- Frontend: React Native + Expo + TypeScript + NativeWind + React Native Reusables + Expo Router
  + TanStack Query + Zod.
- Database: Supabase PostgreSQL.
- No authentication in V1 (deferred to V2 with Clerk).
- V1 briefing is generated once per day on a scheduled job, not on-demand per user.
- Mobile package manager: **npm**.
- Backend environment tooling: **venv + pip** (system Python; see Known Issues re: version).
- GitHub repo is **private**.
- Commit messages must **not** include a "Co-Authored-By: Claude" trailer (user preference).
- `mobile/` and `backend/` were intentionally left as placeholders in Milestone 1 — full scaffolds
  happen in Milestone 4 (Expo) and Milestone 3 (FastAPI) respectively, per the roadmap.

## Current Architecture

**Frontend** — Not yet scaffolded. Will be Expo + TypeScript, organized around `app/` (Expo
Router screens), `components/`, `hooks/`, `lib/`, `theme/` per `docs/02-system-architecture.md`
§13.

**Backend** — FastAPI scaffold complete. `app/main.py` wires settings → logging → app → routers.
`core/` holds `config.py` (Pydantic Settings, fail-fast) and `logging.py`. `routers/` holds
`health.py` (`GET /health`). `services/`, `schemas/`, `models/`, `utils/` exist as empty packages
awaiting later milestones. No database, no external API integrations yet.

**Database** — Supabase PostgreSQL. No project created yet (Milestone 6). Planned tables:
`briefings`, `economic_events`, `enriched_events`, `fred_series`, `news_articles`,
`device_tokens`, `job_runs`.

**External APIs** — Finnhub, FRED, Marketaux, OpenAI, Expo Notifications. None integrated yet
(Milestones 12, 16, 18, 20, 41–45).

## Current File Structure

```text
walris/
  .git/
  .gitignore
  README.md
  mobile/
    README.md
  backend/
    README.md
    requirements.txt
    .venv/                     (gitignored; fastapi, uvicorn, pydantic-settings installed)
    app/
      __init__.py
      main.py
      core/
        __init__.py
        config.py
        logging.py
      routers/
        __init__.py
        health.py
      services/__init__.py     (empty — Milestone 12+)
      schemas/__init__.py      (empty — Milestone 14+)
      models/__init__.py       (empty — Milestone 11)
      utils/__init__.py        (empty — nothing needed yet)
  docs/
    01-product-requirements.md
    02-system-architecture.md
    03-development-roadmap.md
    04-design-system.md
    05-engineering-journal.md
    06-resume-prompt.md
```

## Key Files Created

- `README.md` — project overview and doc index
- `.gitignore` — Python/Node/OS/editor ignores
- `mobile/README.md`, `backend/README.md` — placeholder explainers
- `docs/01-product-requirements.md` through `docs/06-resume-prompt.md` — full project docs
- `backend/requirements.txt` — fastapi, uvicorn[standard], pydantic-settings
- `backend/app/core/config.py` — `Settings` (Pydantic `BaseSettings`, fail-fast, `Literal`-typed
  `environment` field defaulting to `"development"`)
- `backend/app/core/logging.py` — `configure_logging(environment)`
- `backend/app/routers/health.py` — `GET /health` → `{"status": "ok"}`
- `backend/app/main.py` — app entrypoint, wires the above together

## Known Issues

- Global git identity (`user.name`/`user.email`) is not configured on this machine; the first
  commit used git's auto-derived identity (`Kai Beltz <kaibeltz@Kais-MacBook-Pro.local>`). Worth
  setting `git config --global user.name/user.email` explicitly at some point (not done
  automatically — see git safety rules).
- System Python is 3.14.6. **Resolved as a non-issue**: Milestone 3's dependencies (fastapi,
  uvicorn, pydantic-settings, and compiled sub-deps like pydantic-core, httptools, uvloop,
  watchfiles) all installed cleanly with prebuilt 3.14 wheels. Worth re-checking if a future
  milestone (e.g. SQLAlchemy/Alembic in Milestone 11, or a DB driver) hits a wheel gap, but no
  action needed for now.
- No `.env.example` / `.env.local.example` yet — those are Milestone 5 deliverables. Backend
  `Settings` currently has no `.env` file support wired up (no `SettingsConfigDict(env_file=...)`)
  since there's no `.env` file yet to read from.
- No tests, CI, or linting configured yet — Milestones 5 and 8.

## Commands

Backend (once scaffolded in Milestone 3):

```bash
source backend/.venv/bin/activate
uvicorn app.main:app --reload
```

Frontend (once scaffolded in Milestone 4):

```bash
npx expo start
```

Database (once Alembic is set up in Milestone 11):

```bash
alembic upgrade head
```

## Environment Variables

Not yet created. Per `docs/02-system-architecture.md` §25, will eventually need:

Backend (`backend/.env`):

```text
DATABASE_URL
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
FINNHUB_API_KEY
FRED_API_KEY
MARKETAUX_API_KEY
OPENAI_API_KEY
ADMIN_SECRET
EXPO_ACCESS_TOKEN
ENVIRONMENT
```

Mobile (`mobile/.env.local`):

```text
EXPO_PUBLIC_API_BASE_URL
```

## Next Steps

1. Begin Milestone 4 — React Native Foundation: run `create-expo-app` inside `mobile/`
   (TypeScript template), install Expo Router, NativeWind, React Native Reusables, and TanStack
   Query, and implement a basic home screen, navigation foundation, and theme configuration.
2. Begin Milestone 5 — Development Environment: add Ruff/Black/mypy for backend and
   ESLint/Prettier/TS-strict for mobile, plus `.env.example` files for both.
3. Begin Milestone 6 — Supabase Setup: create the Supabase project, configure the connection, and
   create the initial tables (`briefings`, `economic_events`, `enriched_events`, `fred_series`,
   `news_articles`, `device_tokens`, `job_runs`).
