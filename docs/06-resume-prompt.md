# Walris Resume Prompt

**Document:** docs/06-resume-prompt.md
**Last Updated:** 2026-07-08 (paused mid-Milestone 3)
**Status:** Living Document — update at the end of every milestone

This document is the current state of the Walris project. Read it before making assumptions in a
new session.

---

## Current Project Status

Walris exists as a GitHub repository with a scaffolded folder layout and complete project
documentation. No application code has been written yet (no FastAPI app, no Expo app). This is
expected — Milestones 1 and 2 are pure setup/documentation by design.

- GitHub repo: https://github.com/knbeltz/walris (private)
- Local path: `/Users/kaibeltz/Desktop/Coding Projects/walris`

## Completed Milestones

- [x] **Milestone 1 — Repository & Project Setup**
- [x] **Milestone 2 — Documentation Foundation**
- [ ] Milestone 3 — Backend Foundation
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

**Milestone 3 — Backend Foundation** (in progress — paused between Phase 1 and Phase 2)

- Goal: Scaffold the FastAPI application (`backend/app/main.py`, `core/`, `routers/`, `services/`,
  `schemas/`, `models/`, `utils/`), implement a health endpoint, environment configuration,
  logging, and dependency management.
- Progress: **Phase 1 (Understand the Milestone) is complete** — goal, why-it-matters, files
  involved, acceptance criteria, and DoD have been summarized and agreed on (see below). We paused
  right before **Phase 2 (Define Edge Cases)** — specifically, discussing what happens if the app
  starts without required env vars, what `core/` vs `utils/` should each hold, and whether
  `main.py` should do anything beyond wiring things together. No code or files for Milestone 3
  have been created yet. `backend/` still only contains the placeholder `README.md` and the
  `.venv` virtual environment shell (no packages installed).
- Phase 1 summary (for quick recall next session):
  - **Acceptance Criteria:** `uvicorn app.main:app --reload` starts successfully; health endpoint
    returns HTTP 200.
  - **Definition of Done:** Backend can start locally.
- Also open/undecided from the prior session: whether to switch `backend/.venv` from system
  Python 3.14.6 to an older version (e.g. 3.12 via pyenv/homebrew) now, or wait and only switch if
  a real dependency install failure occurs in Milestone 3. Current lean: wait and see — FastAPI/
  SQLAlchemy/Alembic/Pydantic are mature enough to likely already support 3.14.
- **Resume here:** pick up the Phase 2 edge-case discussion for Milestone 3 (env vars missing,
  `core/` vs `utils/` responsibilities, `main.py` scope) before writing any backend code.

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

**Backend** — Not yet scaffolded. Will be FastAPI organized around `app/main.py`, `core/`,
`routers/`, `services/`, `schemas/`, `models/`, `utils/` per `docs/03-development-roadmap.md`
Milestone 3.

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
    .venv/            (gitignored, empty of packages)
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

## Known Issues

- Global git identity (`user.name`/`user.email`) is not configured on this machine; the first
  commit used git's auto-derived identity (`Kai Beltz <kaibeltz@Kais-MacBook-Pro.local>`). Worth
  setting `git config --global user.name/user.email` explicitly at some point (not done
  automatically — see git safety rules).
- System Python is 3.14.6, which is very new. Some backend dependencies in Milestone 3 (FastAPI,
  SQLAlchemy, Alembic, etc.) may not yet publish wheels for 3.14. If `pip install` fails on
  compiled dependencies, consider installing a more broadly-supported Python (e.g. 3.12) via
  pyenv/brew and recreating `backend/.venv`.
- No `.env.example` / `.env.local.example` yet — those are Milestone 5 deliverables.
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

1. Begin Milestone 3 — Backend Foundation: scaffold `backend/app/` structure, install FastAPI +
   Uvicorn in `backend/.venv`, implement `GET /health`, and verify `uvicorn app.main:app --reload`
   starts successfully.
2. Begin Milestone 4 — React Native Foundation: run `create-expo-app` inside `mobile/` (TypeScript
   template), install Expo Router, NativeWind, React Native Reusables, and TanStack Query.
3. Begin Milestone 5 — Development Environment: add Ruff/Black/mypy for backend and
   ESLint/Prettier/TS-strict for mobile, plus `.env.example` files for both.
