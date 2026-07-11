# Walris Resume Prompt

**Document:** docs/06-resume-prompt.md
**Last Updated:** 2026-07-10 (Milestone 9 complete)
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
required configuration. The backend now has a real Supabase Postgres database behind it — all
seven core tables exist, migrations run through Alembic, and `GET /health` proves connectivity
with a real query. GitHub Actions CI now runs all of the above (lint/format/type-check, both
apps) on every push to `main` and every pull request, verified passing on a real run. No real
screens/data fetching exist yet — that's later milestones.

- GitHub repo: https://github.com/knbeltz/walris (private)
- Local path: `/Users/kaibeltz/Desktop/Coding Projects/walris`

## Completed Milestones

- [x] **Milestone 1 — Repository & Project Setup**
- [x] **Milestone 2 — Documentation Foundation**
- [x] **Milestone 3 — Backend Foundation**
- [x] **Milestone 4 — React Native Foundation**
- [x] **Milestone 5 — Development Environment**
- [x] **Milestone 6 — Supabase Setup**
- [x] **Milestone 7 — Configuration System**
- [x] **Milestone 8 — Continuous Integration**
- [x] **Milestone 9 — API Foundation**
- [ ] Milestone 10 — First End-to-End Connection
- [ ] Milestones 11–26 — Core Backend (Part 2)
- [ ] Milestones 27–40 — Mobile App (Part 3)
- [ ] Milestones 41–56 — Notifications, QA, Deployment & Launch (Part 4)

## Current Milestone

**Milestone 10 — First End-to-End Connection** (not started)

- Goal per the roadmap: verify the mobile app talks to the backend for the first time. Backend:
  `GET /health` (already exists). Frontend: call it via TanStack Query, display "Backend
  Connected / Status: Healthy," handle loading/error/success states.
- **Working agreement change starting this milestone:** the user writes pseudocode and the actual
  implementation (the TanStack Query hook, the screen's loading/error/success UI); Claude handles
  configuration/tooling and reviews. See Important Decisions below for the full agreement,
  including the split on edge cases (Claude surfaces technical/infra ones; logical/behavioral
  ones are worked out together). This is a deliberate, good first milestone to start on — small,
  contained, no architectural decisions riding on it.
- **Resume here:** Phase 1 (Understand the Milestone) for Milestone 10, following the same
  mentor workflow used for Milestones 3–9 (understand → edge cases → pseudocode → implementation →
  review → refactor → sign off), under the new working agreement.
- Reference: `docs/08-code-reference-milestones-3-6-9.md` has a full snapshot of the Milestone
  3/6/9 code (the milestones with real logic, as opposed to pure config) for study — not a
  template to copy forward.

### Milestone 9 — API Foundation (complete)

Full mentor workflow (Phases 1–7), still Claude-implemented (the working-agreement change to
user-written code starts at Milestone 10, not this one).

- **Decisions made (with reasoning):**
  - **URL-prefix versioning** (`/v1/...`), not header-based — simpler to understand, test, and
    debug (curl/browser-visible) than an `Accept` header scheme, and it's what most real-world
    APIs (Stripe, GitHub) actually do regardless of REST purism.
  - **Raw resource + standardized errors only**, not a full success/error envelope — matches
    FastAPI's own idiom; a successful `GET /briefings/today` returns the briefing object directly,
    only *failure* responses get a predictable `{"error": {...}, "request_id": ...}` shape. Keeps
    the mobile app's happy-path code simple.
  - **`/health` stays unversioned** (not `/v1/health`) — health checks are an operational concern
    (uptime monitors, load balancers) that should stay decoupled from the versioned business API
    contract, which will evolve independently over time.
  - **`request_id` added** (not explicitly asked for by the roadmap) — ties the logging middleware
    and error responses together so a specific failure can always be matched to its exact server
    log line.
  - **Error codes as a small fixed set mapped from HTTP status** (`404→NOT_FOUND`,
    `422→VALIDATION_ERROR`, etc.), not bespoke per-endpoint codes — generic infrastructure
    shouldn't guess at business-specific error cases that don't exist yet.
  - **Dev vs. prod behavior for unhandled exceptions** — full exception always logged server-side;
    the real message is only included in the API response when `environment == "development"`,
    otherwise a generic safe message — reusing the same `Settings.environment` pattern from
    Milestone 3's logging.
- **What got built:** `app/schemas/errors.py` (`ErrorDetail`, `ErrorResponse`), `app/schemas/
  health.py` (`HealthResponse`, replacing `/health`'s old raw `dict[str, str]` return), `app/core/
  middleware.py` (`RequestLoggingMiddleware` — assigns a `request_id`, times the request, logs
  method/path/status/duration, echoes the ID back as an `X-Request-ID` header), `app/core/
  exceptions.py` (three handlers: validation/422, HTTP/varies, unhandled/500), an empty
  `v1_router` in `app/routers/__init__.py` (no routes yet — ready for Milestone 10+), all wired
  together in `main.py`.
- **A real bug found during verification, not just written and assumed correct:** the 404 handler
  initially didn't fire for "no matching route" errors. Cause: those are raised internally as
  Starlette's *base* `HTTPException`, while the handler was registered against `fastapi.
  HTTPException` (a subclass) — a handler on the narrower subclass doesn't catch instances of the
  broader base class. Fixed by registering against Starlette's base `HTTPException` instead,
  which (via the exception's MRO) catches both the base-class routing errors and any
  `fastapi.HTTPException` raised in application code.
- **A second, smaller fix:** mypy strict initially rejected `app.add_exception_handler(...)`
  calls (the handler functions' specific exception-subclass parameter types didn't match the
  method's declared generic `Exception` signature) — switched to the `app.exception_handler(...)`
  decorator form (applied directly to the imported functions, not as an inline decorator) instead,
  which mypy accepts cleanly.
- **Honest limitation:** the validation-error (422) handler is wired and type-checks, but couldn't
  be exercised end-to-end yet — no current endpoint takes any parameters to invalidate. Its first
  real test will be whichever endpoint Milestone 10 adds.
- **Verified working:** `ruff check`, `ruff format --check`, and `mypy --strict` all pass clean.
  Manually verified end-to-end against a running server: `GET /health` still works (now backed by
  `HealthResponse`); a nonexistent path returns the standardized error shape with a `request_id`;
  temporarily forcing `/health` to raise confirmed the 500 path also returns the standardized
  shape, includes the real exception message in development mode, and logs the full traceback
  server-side — then the temporary change was reverted and re-verified clean.

### Milestone 8 — Continuous Integration (complete)

- **Decisions made (with reasoning):**
  - **Trigger on both `push` to `main` and `pull_request`**, not pull-request-only as the roadmap
    literally says. Every commit across this entire project so far has gone straight to `main` —
    no feature branches or PRs used at all. A pull-request-only trigger would have meant the CI
    workflow essentially never ran, given actual observed workflow. Running on both means it's
    useful today (direct pushes) and still works if a PR-based workflow gets adopted later.
  - **Fuller check scope than the roadmap's literal list** — added mypy `--strict`, `tsc --noEmit`,
    and Prettier's format check on top of the roadmap's named Ruff/ESLint/TypeScript, matching
    everything actually run locally. Reasoning: CI that's narrower than local checks creates a real
    gap — e.g. unformatted code could merge/land on `main` with CI staying green the whole time.
  - **Ruff alone, no Black** — same reasoning as Milestone 5; the roadmap repeats "Black" here too,
    but it'd be inconsistent to reintroduce a tool we deliberately dropped two milestones ago.
- **What got built:** `.github/workflows/ci.yml` — one workflow, two parallel jobs. `backend` job:
  Python 3.14 → `pip install -r requirements-dev.txt` → `ruff check` → `ruff format --check` →
  `mypy`. `mobile` job: Node 26 → `npm ci` → `npm run lint` → `npx tsc --noEmit` →
  `npm run format:check`.
- **Verified empirically, not just by reading docs:** neither Python 3.14 nor Node 26 are
  confirmed-supported in GitHub Actions' hosted runners by documentation alone (both are quite
  new), so rather than keep researching, the workflow was pushed for real and watched end to end —
  both jobs passed on the first run. One harmless notice appeared: GitHub flagged that
  `actions/checkout@v4`/`actions/setup-python@v5`'s own internal Node.js runtime (unrelated to our
  specified Python/Node versions) targets a deprecated Node 20 and is being auto-forced to Node 24
  — this is GitHub handling its own action infrastructure transparently, not something requiring
  any fix here.

### Milestone 7 — Configuration System (complete)

Much lighter than Milestones 3–6 — this was a **verification milestone, not a build one**.

- **What happened:** reading the roadmap's Acceptance Criteria ("fails gracefully when required
  variables are missing") and Definition of Done ("no secrets are hardcoded") literally, both were
  already true from Milestones 3 and 6 — `Settings` is a Pydantic `BaseSettings` that fails fast
  on missing `database_url`, and nothing sensitive has ever been hardcoded (everything lives in
  gitignored `.env`). Flagged this overlap explicitly and discussed two options: (A) verify the
  existing behavior and sign off, or (B) pre-declare `Settings` fields now for every future API
  key (Finnhub, FRED, Marketaux, OpenAI, admin secret, Expo push), even though nothing reads them
  yet.
- **Decision: Option A**, deliberately. Option B's only apparent benefit (less work later) turned
  out to be illusory — to add those fields today they'd have to be `Optional[str] = None` (since
  nothing sets them yet), which would quietly defeat the fail-fast guarantee this milestone is
  about: an optional field can't distinguish "genuinely missing, something will break" from
  "intentionally unused right now," it just silently returns `None` either way. When each key's
  owning milestone actually arrives and needs it to be a *required* field, we'd have to change it
  from optional to required anyway — so pre-declaring wouldn't have saved real work, just added a
  placeholder that gets redone later while weakening `Settings` as an accurate, honest reflection
  of what the app currently uses.
- **Verification performed:** confirmed no hardcoded secrets anywhere in tracked backend files
  (`git grep` for key/secret/password/token literal assignments — none found). Directly tested
  the fail-fast behavior by temporarily removing `backend/.env` and confirming `Settings()` raises
  a clear `pydantic.ValidationError` pointing at the missing `database_url` field, then restored
  `.env` and confirmed normal startup still works.
- **No code changes this milestone** — purely a scope read + verification pass.

### Milestone 6 — Supabase Setup (complete)

Full mentor workflow (Phases 1–7) was followed end to end, same as Milestones 3–5. This was the
first milestone involving an external service (an actual account/project on Supabase's website,
under the user's own credentials) rather than pure local scaffolding — a real workflow shift worth
remembering for Milestone 12+ (Finnhub/FRED/Marketaux/OpenAI all involve the same pattern).

- **Decisions made (with reasoning):**
  - **Sync SQLAlchemy**, not async — the backend is mostly a once-a-day scheduled job plus light
    read traffic, not a high-concurrency service, so async's benefit (juggling many concurrent
    waits) doesn't apply yet, while its complexity cost (`async`/`await` threaded through every
    DB call) would apply immediately.
  - **UUID primary keys**, not auto-incrementing integers — matches Supabase convention, avoids
    leaking row counts, and allows generating IDs before insert (useful for related rows created
    together).
  - **`psycopg` (v3)**, not `psycopg2-binary` — more actively maintained, and confirmed to have
    prebuilt Python 3.14 wheels (checked before committing to it, same caution as Milestone 3's
    Python-version check).
  - **Direct connection was the original plan, but doesn't work from this network** — Supabase's
    direct-connection hostname is IPv6-only, and this machine only has a link-local (non-routable)
    IPv6 address. Switched to the **Session pooler** instead (not Transaction pooler — Session
    preserves per-connection state, which Transaction pooling breaks for some migration
    operations). If this machine ever gets real IPv6 connectivity or moves networks, direct
    connection could be reconsidered, but Session pooler has no real downside for this app's shape.
  - **`--radius` and column types**: see "What got built" below.
  - Decided to build the actual SQLAlchemy model classes now rather than deferring to Milestone 11
    (see Important Decisions) — Alembic's autogenerate requires the models to exist to diff
    against, so there was no way to satisfy Milestone 6's "create migration system" deliverable
    without them.
- **What got built:** `backend/app/core/database.py` (`engine`, `SessionLocal`, `Base`,
  `TimestampMixin`, `get_db` FastAPI dependency); seven SQLAlchemy model classes in
  `backend/app/models/` (`Briefing`, `EconomicEvent`, `EnrichedEvent`, `FredSeries`,
  `NewsArticle`, `DeviceToken`, `JobRun`) matching `docs/02-system-architecture.md` §12's column
  lists, with `timestamptz` timestamps, JSONB for free-form fields (`affected_groups`, `entities`,
  `topics`, `data_points`, `job_metadata`), cascade-delete on the `briefing → economic_events →
  enriched_events/fred_series/news_articles` relationships, and a unique constraint on
  `briefing_date` (V1 generates one briefing per day). Alembic initialized in `backend/alembic/`,
  configured to reuse the app's own `engine` (see the debugging note below for why this matters).
  One reviewed migration (`b9a040b66e1e_create_initial_tables.py`) applied to the real Supabase
  database. `GET /health` extended to run a real `SELECT 1` through a DB session.
- **Judgment calls made where the design doc doesn't specify a value:** `status` fields
  (`briefings`, `job_runs`) are plain `String`, not a Postgres `ENUM` — enums are painful to alter
  later, and a plain string is more forgiving while the schema is still young. Numeric values
  (`actual_value`, `latest_value`, etc.) are `Float`, not `Numeric`/decimal — these are display
  values, not currency needing exact decimal arithmetic. The `--radius` base was derived directly
  from the design doc's own Button/Input (8px) and Card/Modal (12px) values, not guessed.
- **The authentication debugging saga** — by far the bulk of this milestone's time. Full
  play-by-play is worth reading once if `alembic/env.py` or `app/core/database.py` ever need
  touching again; short version:
  1. Direct connection failed three different ways in sequence (a special character in the
     password broke URL parsing; SQLAlchemy defaulted to the wrong driver for Supabase's bare
     `postgresql://` scheme; the direct-connection hostname turned out to be IPv6-only and
     unreachable from this network). Each was a distinct, real bug, not the same thing recurring.
  2. Switched to the Session pooler, then hit a long run of `password authentication failed`
     errors. Several password resets in a row didn't fix it — because **the password was never
     the problem**. That only became clear by testing raw `psycopg` connections directly
     (bypassing SQLAlchemy entirely), which succeeded consistently, proving the credentials were
     fine and the bug was specifically in how the SQLAlchemy/Alembic path connected.
  3. **Root cause:** `alembic/env.py`'s default template builds its own separate database engine
     by converting the connection URL to a *string* and having a second function
     (`engine_from_config`) re-parse that string from scratch — and something in that
     object-to-string-and-back round-trip silently broke. Fixed by having `env.py` import and
     reuse the exact same `engine` object `app/core/database.py` already builds, eliminating the
     round-trip entirely (one engine, defined once, used everywhere — cleaner design regardless of
     the bug).
  4. Smaller fixes along the way: `Settings` needed `extra="ignore"` added (reserved-but-unused
     `.env` vars were crashing startup — same pattern as `.env.example` documenting vars before
     `Settings` reads them, first hit in Milestone 5, now actually triggered); Ruff needed
     `alembic/versions/` excluded from linting (autogenerated migrations will never match hand-
     written style, and re-fighting that on every future migration isn't worth it) and
     `Depends()`/`Query()` allow-listed for the bugbear B008 rule (FastAPI's DI pattern requires
     calling them in argument defaults — that's the API, not the mutable-default-argument footgun
     the rule normally guards against).
- **Known exposure (low-risk, already handled):** early in this milestone, a Pydantic validation
  error printed the real `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` values into terminal
  output. Never committed, never sent anywhere external. The database password was independently
  reset multiple times afterward for unrelated debugging reasons, so it's a different password now
  regardless. Nothing further needed unless the Supabase service-role key itself is a concern, in
  which case it can be regenerated from the API Keys page.
- **Verified working:** `ruff check`, `ruff format --check`, and `mypy --strict` all pass clean;
  `alembic upgrade head` applied without error; all 7 tables confirmed present in Supabase via
  direct inspection; `uvicorn app.main:app` boots and `GET /health` returns
  `200 {"status":"ok"}` after a real round-trip through FastAPI → SQLAlchemy → Supabase Postgres.

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
- Backend database access is **sync SQLAlchemy**, not async — the app's workload (a daily
  scheduled job plus light reads) doesn't need async's concurrency benefits yet, and sync is
  simpler to reason about while learning.
- All tables use **UUID primary keys** (Supabase/Postgres convention), not auto-incrementing
  integers.
- Database connection uses Supabase's **Session pooler**, not a direct connection — this
  machine's network can't reach Supabase's IPv6-only direct-connection hostname (see Milestone 6
  notes). Revisit only if the network situation changes.
- SQLAlchemy model classes for all 7 core tables were built in **Milestone 6**, not deferred to
  Milestone 11 as the roadmap's wording might suggest — Alembic's autogenerate needs the models to
  exist to diff against, so there was no way to do Milestone 6's migration-system deliverable
  without them. Milestone 11 will likely be a light touch-up, not new model design.
- **Standing principle (confirmed again in Milestone 7):** don't pre-declare config fields, model
  fields, or scaffolding before the code that actually needs them exists — even when a roadmap
  milestone's wording suggests doing so now. Every time this has come up (font loading and dark
  mode in Milestone 4, API keys in Milestone 5, now `Settings` fields in Milestone 7), building
  ahead of need has turned out to cost more than it saves, usually by weakening some other
  guarantee (fail-fast validation, in Milestone 7's case) rather than actually being free.
- CI (`.github/workflows/ci.yml`) runs on **both `push` to `main` and `pull_request`**, not
  PR-only as the roadmap literally says — matches actual observed workflow (no branches/PRs used
  so far), while still working if that changes later. CI checks are **broader than the roadmap's
  literal list**: Ruff, mypy `--strict`, ESLint, `tsc --noEmit`, and Prettier's format check — the
  same set run locally, not a narrower CI-only subset.
- **Working agreement, starting Milestone 10 (2026-07-10):** across Milestones 3–9, Claude wrote
  100% of the actual code every milestone — the user made real decisions and asked deep
  conceptual questions, but never wrote pseudocode or implementation themselves. This was never a
  deliberate plan, just default momentum, and the user caught it and asked to change it. From
  Milestone 10 onward: **the user writes pseudocode (Phase 3) and the actual application/business
  logic implementation (Phase 4)** — routes, models, exception handlers, middleware, components,
  hooks, service functions. Claude's role narrows to configuration/tooling work (dependency
  installs, config files, CI, environment/`Settings` wiring) plus Phases 1, 5, 6, 7 (explaining
  the milestone, reviewing the user's code, suggesting refactors, sign-off/doc updates) and git
  operations when asked. **Refinement on Phase 2 (edge cases):** for *technical/infrastructure*
  edge cases (version compatibility, environment/network issues, driver quirks), Claude still
  surfaces these directly, same as before. For *logical/behavioral* edge cases — what the
  implementation should actually do in a given scenario — the user wants to actively participate
  in identifying them, not just receive a pre-made list to confirm. If it's ambiguous whether
  something is "logic" or "config" (e.g., is a SQLAlchemy model class logic or schema config?),
  ask rather than assume.
- **Explain-in-detail trigger:** whenever a concept referenced in
  `docs/08-code-reference-milestones-3-6-9.md` comes up again during later work (SQLAlchemy
  models/sessions, Alembic migrations, exception handlers, middleware, response models, UUIDs,
  JSONB, cascade deletes, connection pooling, etc.), explain it in enough detail that the user has
  what they need to actually write the next step themselves — don't assume it's already
  internalized just because it was explained once when it was originally built.

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

**Backend** — FastAPI scaffold complete. `app/main.py` wires settings → logging → middleware →
exception handlers → routers. `core/` holds `config.py` (Pydantic Settings, fail-fast, reads
`.env`, `extra="ignore"` for not-yet-wired reserved vars), `database.py` (SQLAlchemy `engine`/
`SessionLocal`/`Base`/`TimestampMixin`/`get_db`), `middleware.py` (`RequestLoggingMiddleware`),
`exceptions.py` (validation/HTTP/unhandled exception handlers), and `logging.py`. `routers/`
holds `health.py` (`GET /health`, unversioned, verifies DB connectivity via a real query) and an
empty `v1_router` (ready for future versioned endpoints, no routes yet). `models/` holds all 7
SQLAlchemy model classes. `schemas/` holds `errors.py` (`ErrorDetail`/`ErrorResponse`) and
`health.py` (`HealthResponse`) — no longer empty as of Milestone 9, ahead of its "Milestone 14+"
placeholder comment, same pattern as the Milestone 6/7 overlaps. `services/`, `utils/` still
empty, awaiting later milestones. Ruff (lint + format) and mypy `--strict` are configured via
`pyproject.toml` and passing clean; `alembic/versions/` excluded from linting (generated,
historical files).

**Database** — Supabase PostgreSQL, project created and live (Milestone 6). All 7 core tables
exist: `briefings`, `economic_events`, `enriched_events`, `fred_series`, `news_articles`,
`device_tokens`, `job_runs`. Connected via the Session pooler (not direct — see Important
Decisions). Migrations run through Alembic (`backend/alembic/`), which reuses the app's own
`engine` object rather than building a separate one.

**External APIs** — Finnhub, FRED, Marketaux, OpenAI, Expo Notifications. None integrated yet
(Milestones 12, 16, 18, 20, 41–45).

## Current File Structure

```text
walris/
  .git/
  .github/
    workflows/
      ci.yml                   (backend + mobile jobs; push to main + pull_request)
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
    requirements.txt           (+ sqlalchemy, alembic, psycopg[binary])
    requirements-dev.txt       (-r requirements.txt, ruff, mypy)
    pyproject.toml             (Ruff lint+format config incl. alembic/versions exclude
                                 and Depends()/Query() bugbear allowlist; mypy strict config)
    .env                       (gitignored; DATABASE_URL, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY filled in)
    .env.example
    .venv/                     (gitignored; fastapi, uvicorn, pydantic-settings, ruff, mypy,
                                 sqlalchemy, alembic, psycopg installed)
    alembic.ini
    alembic/
      env.py                    (reuses app.core.database.engine directly — see M6 notes)
      script.py.mako
      versions/
        b9a040b66e1e_create_initial_tables.py
    app/
      __init__.py
      main.py
      core/
        __init__.py
        config.py                (now reads database_url, extra="ignore")
        database.py               (engine, SessionLocal, Base, TimestampMixin, get_db)
        middleware.py              (RequestLoggingMiddleware — request_id, timing, logging)
        exceptions.py              (validation/HTTP/unhandled exception handlers)
        logging.py
      routers/
        __init__.py                (v1_router — empty, ready for future versioned endpoints)
        health.py                 (unversioned; checks DB connectivity; uses HealthResponse)
      models/
        __init__.py                (imports all 7 models for Base.metadata)
        briefing.py
        economic_event.py
        enriched_event.py
        fred_series.py
        news_article.py
        device_token.py
        job_run.py
      schemas/
        __init__.py              (exports ErrorDetail, ErrorResponse, HealthResponse)
        errors.py                (ErrorDetail, ErrorResponse — the standard error envelope)
        health.py                (HealthResponse)
      services/__init__.py     (empty — Milestone 12+)
      utils/__init__.py        (empty — nothing needed yet)
  docs/
    01-product-requirements.md
    02-system-architecture.md
    03-development-roadmap.md
    04-design-system.md
    05-engineering-journal.md
    06-resume-prompt.md
    07-learning-notes.md
    08-code-reference-milestones-3-6-9.md
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
- `backend/app/core/database.py` — SQLAlchemy `engine`/`SessionLocal`/`Base`/`TimestampMixin`/
  `get_db`; reused directly by `alembic/env.py` (important — see Milestone 6 notes on why a
  second, separately-constructed engine caused a long debugging saga)
- `backend/app/models/` — all 7 SQLAlchemy model classes (`Briefing`, `EconomicEvent`,
  `EnrichedEvent`, `FredSeries`, `NewsArticle`, `DeviceToken`, `JobRun`)
- `backend/alembic/` — migration system; one applied migration creating all 7 tables in Supabase
- `backend/app/routers/health.py` — `GET /health` now runs a real `SELECT 1` through the DB
- `.github/workflows/ci.yml` — GitHub Actions: Ruff/mypy (backend) + ESLint/tsc/Prettier (mobile)
  on push to `main` and on pull requests; verified passing on a real run, not just written
- `backend/app/schemas/errors.py`, `backend/app/schemas/health.py` — the standardized error
  envelope (`ErrorDetail`/`ErrorResponse`) and `/health`'s response model
- `backend/app/core/middleware.py` — `RequestLoggingMiddleware` (per-request `request_id`, timing,
  logging, `X-Request-ID` response header)
- `backend/app/core/exceptions.py` — validation/HTTP/unhandled exception handlers, all producing
  the standardized error shape; registered against Starlette's base `HTTPException`, not
  `fastapi.HTTPException` (see Milestone 9 notes for why that distinction mattered)
- `backend/app/routers/__init__.py` — empty `v1_router`, the real infrastructure for API
  versioning, ready for Milestone 10+'s first real endpoint
- `docs/08-code-reference-milestones-3-6-9.md` — snapshot of the actual code from the three
  milestones that involved real logic (not just config), for study — not a template to copy
  forward now that the user writes implementation starting Milestone 10

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
- No automated tests exist yet (no pytest/jest suite) — CI (Milestone 8) runs linting/type
  checking/formatting on every push/PR, but there's nothing to actually test yet since there's no
  business logic beyond config/models/health checks. Add real tests as they become meaningful.
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

Database (working now, from `backend/` with the venv active):

```bash
alembic upgrade head              # apply migrations
alembic revision --autogenerate -m "description"   # generate a new migration from model changes
```

Always read an autogenerated migration before applying it — don't trust it blindly, especially
the first one on a new table.

## Environment Variables

`backend/.env.example` and `mobile/.env.local.example` exist (Milestone 5); copy them to `.env` /
`.env.local` and fill in real values as each variable's owning milestone lands. `backend/.env`
now exists and is filled in for `ENVIRONMENT`, `DATABASE_URL` (Session pooler connection string),
`SUPABASE_URL`, and `SUPABASE_SERVICE_ROLE_KEY` (Milestone 6) — only `ENVIRONMENT` and
`DATABASE_URL` are actually read by `Settings` today; the Supabase URL/key are filled in for
later use but not consumed by any code yet. The rest remain reserved. Per
`docs/02-system-architecture.md` §25, the full eventual set is:

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

1. Begin Milestone 10 — First End-to-End Connection: mobile calls `GET /health` via TanStack
   Query, displays "Backend Connected / Status: Healthy," handles loading/error/success states.
   **User writes the pseudocode and implementation this time** — see Important Decisions.
2. Begin Milestones 11–26 — Core Backend (Part 2) — where real Walris-specific business logic
   (briefing generation, external API integrations) actually begins.
3. Begin Milestones 27–40 — Mobile App (Part 3).
