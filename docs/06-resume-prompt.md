# Walris Resume Prompt

**Document:** docs/06-resume-prompt.md
**Last Updated:** 2026-07-09 (Milestone 5 complete)
**Status:** Living Document — update at the end of every milestone

This document is the current state of the Walris project. Read it before making assumptions in a
new session.

---

## Current Project Status

Walris exists as a GitHub repository with a scaffolded folder layout, complete project
documentation, a minimal but working FastAPI backend (`uvicorn app.main:app --reload` starts
successfully; `GET /health` returns HTTP 200), and a minimal but working Expo mobile app (Expo
Router + NativeWind + React Native Reusables + TanStack Query, verified launching via Expo Go on
a physical iPhone). Both apps now have linting/formatting/type-checking tooling standardized
(Ruff + strict mypy on backend; ESLint + Prettier on mobile) and `.env.example` files documenting
required configuration. No real screens/data fetching exist yet — that's later milestones.

- GitHub repo: https://github.com/knbeltz/walris (private)
- Local path: `/Users/kaibeltz/Desktop/Coding Projects/walris`

## Completed Milestones

- [x] **Milestone 1 — Repository & Project Setup**
- [x] **Milestone 2 — Documentation Foundation**
- [x] **Milestone 3 — Backend Foundation**
- [x] **Milestone 4 — React Native Foundation**
- [x] **Milestone 5 — Development Environment**
- [ ] Milestone 6 — Supabase Setup
- [ ] Milestone 7 — Configuration System
- [ ] Milestone 8 — Continuous Integration
- [ ] Milestone 9 — API Foundation
- [ ] Milestone 10 — First End-to-End Connection
- [ ] Milestones 11–26 — Core Backend (Part 2)
- [ ] Milestones 27–40 — Mobile App (Part 3)
- [ ] Milestones 41–56 — Notifications, QA, Deployment & Launch (Part 4)

## Current Milestone

**Milestone 6 — Supabase Setup** (not started)

- Goal: Create the Supabase project, configure the local connection, create a migration system,
  and create the initial tables (`briefings`, `economic_events`, `enriched_events`, `fred_series`,
  `news_articles`, `device_tokens`, `job_runs`).
- Progress: Not started.
- **Resume here:** Phase 1 (Understand the Milestone) for Milestone 6, following the same
  mentor workflow used for Milestones 3–5 (understand → edge cases → pseudocode → implementation →
  review → refactor → sign off).

### Milestone 5 — Development Environment (complete)

Full mentor workflow (Phases 1–7) was followed end to end, same as Milestones 3–4.

- **Decisions made (with reasoning, in case they need revisiting):**
  - **Ruff alone, not Ruff + Black**, for backend linting *and* formatting. The roadmap listed
    both, but Ruff's built-in formatter (`ruff format`) is Black-compatible, so running both is
    two tools doing overlapping jobs with no real functional gain on a fresh project. One tool,
    one config, one command for each job.
  - **mypy `--strict` starting now**, not ratcheted up later. This wasn't really optional scope —
    `docs/02-system-architecture.md` §16 already mandates full backend typing as an architecture
    requirement, so strict mode just enforces a decision already made. Cheapest time to adopt it
    is while the codebase is four small files, not after it's grown.
  - **Wired up real `.env` file loading** in `Settings` (`SettingsConfigDict(env_file=".env")`)
    rather than just creating `.env.example` per the roadmap's literal wording — an example file
    with nothing that reads it felt hollow, so this closes that gap now instead of leaving it for
    later.
  - **`prettier-plugin-tailwindcss`** added per your go-ahead, since the mobile app leans heavily
    on NativeWind `className` strings.
- **What got built:**
  - Backend: `backend/pyproject.toml` (Ruff broad rule set — pyflakes, pycodestyle, isort,
    pyupgrade, bugbear, comprehensions, simplify; mypy strict + `pydantic.mypy` plugin, scoped to
    `app/`), `backend/requirements-dev.txt` (split from runtime `requirements.txt`),
    `backend/.env.example` (documents the full eventual variable set from
    `docs/02-system-architecture.md` §25, noting which are actually read by `Settings` today vs.
    reserved for later milestones).
  - Mobile: ESLint (flat config + `eslint-config-expo`, scaffolded via `npx expo lint`), Prettier +
    `prettier-plugin-tailwindcss` + `eslint-config-prettier` (prevents ESLint and Prettier fighting
    over formatting rules), `lint`/`format`/`format:check` npm scripts, `mobile/.env.local.example`.
  - Cleanup: while touching backend files for the `.env` wiring, removed stale Milestone-3
    pseudocode/TODO comments that had been left describing already-finished work as still-to-do
    (in `config.py`, `logging.py`, `main.py`, `health.py`); also added a missing return type
    annotation on the health route and simplified an `if`/`else` to a ternary per Ruff's own
    suggestion.
- **Real problems hit and fixed along the way:**
  - `npx expo lint`'s first run installed ESLint + `eslint-config-expo`, then immediately tried to
    `require('eslint')` in the same process and failed with "Cannot find module 'eslint'" — a
    timing quirk (Node's resolution hadn't caught up with the just-finished install), not a real
    config problem. Re-running the exact same command once the install had finished worked fine.
  - All ten mobile files written before Prettier existed needed reformatting once Prettier was
    added — expected, not a bug; `prettier --write .` fixed it in one pass.
- **Verified working:** `ruff check`, `ruff format --check`, and `mypy` all pass clean on backend;
  `uvicorn app.main:app --reload` + `GET /health` still work after the config/logging/health.py
  edits. `npm run lint`, `npm run format:check`, `npx tsc --noEmit`, and `npx expo-doctor`
  (18/18) all pass clean on mobile.

### Milestone 4 — React Native Foundation (complete)

Full mentor workflow (Phases 1–7) was followed end to end, same as Milestone 3.

- **Real problems hit and fixed along the way** (worth knowing before touching `mobile/` again):
  - Scaffolding on the newest Expo SDK (57) hit an internal Expo inconsistency — expo-router's
    bundled web/DOM-components support (Radix UI + `vaul`) pulled a newer `react-dom` than the
    base template's pinned `react`, causing an npm ERESOLVE conflict. **This was not fixed by
    downgrading to SDK 54** — the same conflict recurred, because the root cause (an unbounded
    peer dep on `react-dom`) exists independent of SDK version. The actual fix: a `"react-dom"`
    entry in `package.json`'s `overrides`, pinned to match `react`'s version. Safe because the app
    never uses expo-router's DOM-components feature.
  - We deliberately settled on **Expo SDK 54** anyway (not 57) because it's the pairing NativeWind
    itself documents as tested (`Expo SDK 54 + NativeWind v4.1`), and it's more likely to have
    broad ecosystem compatibility than the newest SDK.
  - NativeWind's actual engine (`react-native-css-interop`) requires **Tailwind CSS ~3.x**, not
    the current Tailwind v4 — pin `tailwindcss@^3.4.17` explicitly, don't take whatever's latest.
  - The `@react-native-reusables/cli doctor` command's interactive prompts don't all understand
    `--yes`/piped `yes` cleanly — two free-text prompts (CSS/Tailwind file paths) got the literal
    text `"y"` written into `components.json` instead of accepting their defaults. Always spot-check
    `components.json` after running `doctor` non-interactively.
  - `expo-router/react-navigation` (a convenience re-export) doesn't exist in expo-router's SDK-54
    version — use `@react-navigation/native` directly for `ThemeProvider`/`DarkTheme`/`DefaultTheme`/
    `Theme`.
  - `expo-doctor` (Expo's own project health checker, separate from RNR's `doctor`) caught a missing
    `react-native-worklets` peer dependency required by `react-native-reanimated` that doesn't hard-fail
    until runtime — worth running `npx expo-doctor` after any native-module install.
- **What got built:** Expo SDK 54 TypeScript project in `mobile/`; Expo Router (`app/_layout.tsx`
  Stack navigator, `app/index.tsx` home route); NativeWind fully configured (`tailwind.config.js`,
  `babel.config.js`, `metro.config.js`, `global.css`); `@/*` path alias; React Native Reusables
  (`components/ui/`: `button`, `card`, `badge`, `separator`, `text`) plus its prerequisites
  (`lib/utils.ts` cn helper, `PortalHost` in root layout, `inlineRem: 16` in Metro config);
  TanStack Query (`lib/queryClient.ts`, `QueryClientProvider` in root layout); Walris's actual
  design-system colors converted to HSL and wired through `global.css` → `tailwind.config.js` →
  `lib/theme.ts` (React Navigation chrome theme).
- **Judgment calls made where the design doc (`04-design-system.md`) doesn't specify a value** —
  worth revisiting if they look wrong once real screens are built: `border`/`input` = surface-variant
  (#d3e4fe), `ring` = primary (#000000), `destructive`-foreground = white, chart-1–5 = React Native
  Reusables' shadcn defaults (unused until the Historical Chart milestone). The `--radius` base
  (`0.75rem`) was *not* a guess — it was derived directly from the design doc's own shape system so
  that Tailwind's `sm`/`lg` radii land on the doc's Button/Input (8px) and Card/Modal (12px) values.
- **Deferred on purpose:** custom font loading (Libre Caslon Text / Inter / JetBrains Mono) — the
  home screen currently uses the system default font. Dark mode — the design doc never defines a
  dark palette, and `app.json` has `"userInterfaceStyle": "light"` (forces light regardless of
  system setting); `lib/theme.ts`'s `dark` key currently just mirrors `light`.
- **Verified working:** `npx expo start` + Expo Go on a physical iPhone 17 Pro (no Xcode/Android
  Studio on this machine — verification was on a real device, not a simulator); home screen renders
  "Walris" heading, subtitle, and a themed "Get started" button; `npx tsc --noEmit`,
  `npx @react-native-reusables/cli doctor`, and `npx expo-doctor` all pass clean.

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
- Mobile is pinned to **Expo SDK 54**, not the newest SDK (57 at the time of Milestone 4), because
  NativeWind's own docs test against SDK 54 and it avoided an internal Expo dependency conflict
  present on SDK 57 (see Milestone 4 notes above). Re-evaluate the SDK version deliberately before
  ever bumping it — don't just take whatever `npx create-expo-app` defaults to.
- Backend uses **Ruff alone** for both linting and formatting, not Ruff + Black — Ruff's built-in
  formatter is Black-compatible, so running both is redundant (see Milestone 5 notes).
- Backend mypy runs in **`--strict`** mode from the start, not ratcheted up gradually — this
  enforces the full-typing requirement `docs/02-system-architecture.md` §16 already mandates.

## Current Architecture

**Frontend** — Expo SDK 54 + TypeScript scaffold complete. `app/_layout.tsx` wires
`SafeAreaProvider` → `QueryClientProvider` → React Navigation `ThemeProvider` → `Stack` →
`PortalHost`. `app/index.tsx` is a placeholder home screen. `components/ui/` holds React Native
Reusables primitives (`button`, `card`, `badge`, `separator`, `text`). `lib/` holds `utils.ts`
(cn helper), `theme.ts` (Walris colors as React Navigation theme), `queryClient.ts`. Styling is
NativeWind (Tailwind-style `className`) with Walris's actual design-system colors wired through
`global.css` → `tailwind.config.js`. No custom fonts loaded yet (deferred), no real screens/data
fetching yet (later milestones) — `hooks/` and `theme/typography.ts` from
`docs/02-system-architecture.md` §13 don't exist yet. ESLint (flat config + `eslint-config-expo`)
and Prettier (+ `prettier-plugin-tailwindcss`) are configured and passing clean.

**Backend** — FastAPI scaffold complete. `app/main.py` wires settings → logging → app → routers.
`core/` holds `config.py` (Pydantic Settings, fail-fast, now reads `.env`) and `logging.py`.
`routers/` holds `health.py` (`GET /health`). `services/`, `schemas/`, `models/`, `utils/` exist as
empty packages awaiting later milestones. No database, no external API integrations yet. Ruff
(lint + format) and mypy `--strict` are configured via `pyproject.toml` and passing clean.

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
    package.json
    app.json                  (scheme: "walris", userInterfaceStyle: "light")
    tsconfig.json             (strict: true, "@/*" path alias)
    tailwind.config.js
    babel.config.js
    metro.config.js
    global.css                (Walris color tokens as CSS variables)
    components.json           (React Native Reusables config)
    nativewind-env.d.ts
    eslint.config.js           (flat config: eslint-config-expo + eslint-config-prettier)
    .prettierrc                (+ prettier-plugin-tailwindcss)
    .prettierignore
    .env.local.example
    app/
      _layout.tsx              (SafeAreaProvider > QueryClientProvider > ThemeProvider > Stack > PortalHost)
      index.tsx                 (placeholder home screen)
    components/
      ui/
        button.tsx
        card.tsx
        badge.tsx
        separator.tsx
        text.tsx
    lib/
      utils.ts                 (cn helper)
      theme.ts                 (Walris colors as React Navigation theme)
      queryClient.ts
  backend/
    README.md
    requirements.txt
    requirements-dev.txt       (-r requirements.txt, ruff, mypy)
    pyproject.toml             (Ruff lint+format config, mypy strict config)
    .env.example
    .venv/                     (gitignored; fastapi, uvicorn, pydantic-settings, ruff, mypy installed)
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
- `docs/05-engineering-journal.md` now has a real, user-written Entry 1 (Session Goal + Work
  Completed only — the user has deliberately trimmed the journal template down to just those two
  sections; don't suggest re-adding Bugs/Debugging/Learned unless they bring it up)
- `mobile/app/_layout.tsx`, `mobile/app/index.tsx` — Expo Router root layout and home screen
- `mobile/global.css`, `mobile/tailwind.config.js`, `mobile/lib/theme.ts` — Walris design-system
  colors wired through NativeWind and React Navigation (see Milestone 4 notes above for the
  judgment calls made where the design doc didn't specify a value)
- `mobile/components/ui/` — React Native Reusables primitives (button, card, badge, separator, text)
- `mobile/lib/utils.ts`, `mobile/lib/queryClient.ts` — cn helper and TanStack Query client
- `backend/pyproject.toml` — Ruff (broad rule set, lint + format) and mypy (`--strict` +
  `pydantic.mypy` plugin) config
- `backend/requirements-dev.txt`, `backend/.env.example` — dev tooling deps and the documented
  full environment variable shape
- `mobile/eslint.config.js`, `mobile/.prettierrc`, `mobile/.prettierignore`,
  `mobile/.env.local.example` — mobile linting/formatting config and env var template

## Known Issues

- Global git identity (`user.name`/`user.email`) is still not configured on this machine.
  Confirmed this is now causing real inconsistency: early commits used
  `Kai Beltz <kaibeltz@Kais-MacBook-Pro.local>`, but a later commit in this same session used
  `Kai Beltz <kaibeltz@macbook-pro.mynetworksettings.com>` — git's auto-derived identity changed
  based on network/hostname resolution. The repo's commit history now has inconsistent author
  emails for the same person. Worth running
  `git config --global user.name "..."` and `git config --global user.email "..."` yourself soon
  (not done automatically — see git safety rules).
- System Python is 3.14.6. **Resolved as a non-issue**: Milestone 3's dependencies (fastapi,
  uvicorn, pydantic-settings, and compiled sub-deps like pydantic-core, httptools, uvloop,
  watchfiles) all installed cleanly with prebuilt 3.14 wheels. Worth re-checking if a future
  milestone (e.g. SQLAlchemy/Alembic in Milestone 11, or a DB driver) hits a wheel gap, but no
  action needed for now.
- No tests or CI configured yet — Milestone 8. Linting/formatting (Milestone 5) is done.
- No Xcode or Android Studio installed on this machine (only Xcode Command Line Tools) — no iOS
  Simulator or Android emulator available. Mobile verification happens via Expo Go on a physical
  iPhone 17 Pro instead. Fine for now; would need addressing before any native-build-only feature
  (e.g. custom native modules) or CI device testing later.
- `mobile/package.json` has a `"react-dom": "19.1.0"` entry under `overrides` — needed to resolve
  an expo-router internal peer-dependency conflict (see Milestone 4 notes above). Not a real
  runtime dependency; safe to leave as long as expo-router's DOM-components feature stays unused.
- Mobile has no custom fonts loaded yet (Libre Caslon Text / Inter / JetBrains Mono per
  `docs/04-design-system.md` §5) — deliberately deferred until a milestone that builds a real
  screen needing them. Currently renders with the system default font.

## Commands

Backend (working now):

```bash
source backend/.venv/bin/activate
uvicorn app.main:app --reload
```

Health check: `curl http://127.0.0.1:8000/health` → `{"status":"ok"}`

Frontend (working now):

```bash
cd mobile
npx expo start
```

Scan the QR code with the Expo Go app (verified on a physical iPhone; no Xcode/Android Studio on
this machine, so no simulator available — see Known Issues).

Database (once Alembic is set up in Milestone 11):

```bash
alembic upgrade head
```

## Environment Variables

`backend/.env.example` and `mobile/.env.local.example` exist (Milestone 5); copy them to `.env` /
`.env.local` and fill in real values as each variable's owning milestone lands. Only `ENVIRONMENT`
is actually read by code today (`Settings` in `backend/app/core/config.py`) — the rest are
reserved. Per `docs/02-system-architecture.md` §25, the full eventual set is:

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

1. Begin Milestone 6 — Supabase Setup: create the Supabase project, configure the connection,
   create a migration system, and create the initial tables (`briefings`, `economic_events`,
   `enriched_events`, `fred_series`, `news_articles`, `device_tokens`, `job_runs`).
2. Begin Milestone 7 — Configuration System.
3. Begin Milestone 8 — Continuous Integration.
