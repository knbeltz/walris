# Walris Resume Prompt

**Document:** docs/06-resume-prompt.md
**Last Updated:** 2026-08-03 (Milestone 17 — Daily Data Pipeline & Storage — complete and verified
end-to-end against the live FMP/FRED/Marketaux APIs and the live Supabase database. Milestone 12
formal sign-off still pending.)
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
apps) on every push to `main` and every pull request, verified passing on a real run. The mobile
app now makes its first real network call: a TanStack Query hook (`useHealthCheck.ts`) calls the
backend's `GET /health` over the LAN and the home screen renders loading/error/success states,
verified end-to-end on a physical iPhone against a real running backend (including deliberately
triggering the error state by stopping the backend). This was also the first milestone where the
project's author wrote the actual pseudocode and implementation themselves, per the working
agreement change described below — Claude's role narrowed to configuration/tooling and review.
The backend now has its first real automated tests: `pytest` is installed and configured, and
three tests in `backend/tests/test_models.py` prove the SQLAlchemy model layer actually creates,
queries, and cascade-deletes real rows against the live Supabase database — not just that a raw
`SELECT 1` succeeds, which is all `GET /health` ever proved. No real screens/data fetching beyond
the Milestone 10 health check exist yet — that's later milestones. Milestone 12 is **implemented
and verified** (the roadmap's original "Finnhub Service" scope turned out to be unbuildable on a
free/personal-use basis — see the Milestone 12 section below for the full story — and was
redesigned around Financial Modeling Prep's (FMP) free-tier market-data endpoints instead), though
formal sign-off (updating the checklist below, writing its own "(complete)" section) is still
pending. **Since then, the project has undergone a much bigger pivot**: instead of one identical
briefing for everyone, Walris now plans a personalized daily briefing — users sign up (Clerk),
pick one of 7 categories, optionally add extra topics, and get an individually-generated briefing
built from FRED + FMP + Marketaux + OpenAI. This is fully planned in
**`docs/09-personalization-pivot-plan.md`** (verified FRED series IDs, database schema, service
architecture, mobile changes, and a full milestone breakdown) and reflected in `docs/01`, `docs/02`,
and `docs/03`. **Implementation of this pivot is well underway**: Milestones 13 through 17 are
complete — user accounts and Clerk auth, category/topic selection, the FRED and Marketaux fetch
services, and (as of this update) a full fetch-filter-persist-cleanup pipeline that turns those
services' output into real rows in `daily_data_items`/`daily_data_news`, verified end-to-end
against live APIs and the live database. The next actual coding work is Milestone 18 (Per-User
OpenAI Briefing Generation) per that plan.

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
- [x] **Milestone 10 — First End-to-End Connection**
- [x] **Milestone 11 — Database Models & Migrations**
- [ ] Milestones 12–26 — Core Backend (Part 2)
- [ ] Milestones 27–40 — Mobile App (Part 3)
- [ ] Milestones 41–56 — Notifications, QA, Deployment & Launch (Part 4)

## Current Milestone

**Milestone 18 — Per-User OpenAI Briefing Generation** (not yet started). Milestones 12–17 are all
complete. **Milestone 14's core flow is verified end-to-end on a real device** — sign-up →
`/category` → `/topics` → `/` all confirmed working against the live database. Two smaller pieces
of M14 are still outstanding (name field, settings screen — see M14 notes below), but the flow
itself is no longer blocked. The personalization pivot is fully planned in
`docs/09-personalization-pivot-plan.md`.

### Milestone 17 — Daily Data Pipeline & Storage (complete, 2026-08-03)

All three pieces from `docs/09` §8 are done, and the full chain has been verified end-to-end
against the live FMP/FRED/Marketaux APIs and the live Supabase database — not just type-checked.

**1. Models + migration.** `backend/app/models/daily_data_items.py` (`DailyDataItem`) and
`daily_data_news.py` (`DailyDataNews`) — first real DB storage for FRED/FMP/Marketaux data (M15/M16
only ever fetched and normalized, never persisted). `DailyDataItem` has a `(item_key, date)` unique
constraint (natural key: a FRED series ID or an FMP field like a symbol/sector); `DailyDataNews` has
a real `item_id` foreign key to `DailyDataItem.id` with `ondelete="CASCADE"` (a deliberate choice
over a natural-key match, matching this codebase's existing convention of flat `ForeignKey()`
columns) plus a `(item_id, url)` unique constraint. Migration `7df1ab8dcf84` applied and verified
via direct `inspect(engine)` column/constraint/FK checks against the live database, not just "the
command didn't error." Several real bugs caught in review before this ever ran: a stray-indentation
syntax error, a missing `Base`/`TimestampMixin` import, `uuid.uuid64` (doesn't exist — `uuid.uuid4`)
and `mapped.column` (should be `mapped_column`) typos, `item_id` typed as the SQLAlchemy dialect
`UUID` class instead of Python's `uuid.UUID`, and `sentiment` typed `Mapped[str]` against an actual
`Float` column — none of these were caught by `mypy` (no SQLAlchemy mypy plugin installed), only by
review and, in one case, by direct reproduction of the resulting Pydantic `ValidationError`.

**2. The fetch-filter-persist pipeline**, all in new `backend/app/services/daily_data_service.py`
(and a new `backend/app/schemas/daily_data.py` for the intermediate shapes):
- `fetch_and_shape_fmp_candidates` / `fetch_and_shape_fred_candidates` /
  `fetch_and_shape_marketaux_candidates` — fetch and normalize each provider's data into
  `DailyDataItemCandidate`/`FmpFetchResults` schemas (both new). Required converting
  `fmp_service.py`'s `fetch_market_snapshot`, `fetch_top_gainer_spotlight`, and
  `fetch_top_loser_spotlight` to `async def` (concurrent profile lookups, same pattern as the
  already-async gainer function), and switching `fred_service.py`/`marketaux_service.py` to read
  their API keys from `settings` directly instead of taking them as parameters.
- `filter_candidates_by_news_coverage` — combines FMP + FRED candidates, drops any with zero
  matching Marketaux articles, pairs survivors with their articles (`CoveredDailyDataCandidate`,
  a named schema chosen deliberately over a bare tuple, since two of the bundled fields —
  `gainer`/`loser` on `FmpFetchResults` — share the same type and a positional swap would be a
  silent, `mypy`-invisible bug).
- `fetch_covered_daily_data_candidates` — the orchestrator tying the above together.
- `saved_covered_daily_data_candidates` — persists survivors into `DailyDataItem`/`DailyDataNews`,
  **skip-if-exists** on the `(item_key, date)`/`(item_id, url)` natural keys (chosen over upsert or
  let-it-fail: a retry always completes and leaves a correct, complete row set, rather than
  potentially dying partway through or silently overwriting).
- **A real bug found in `marketaux_service.py`'s `build_news_search_items`, not part of this
  milestone's own new code**: sector/company search items used the bare `sector.sector`/
  `gainer.symbol` as their Marketaux item_key, which would never have matched the
  `"sector: {name}"`/`"company: {symbol}"` prefixed item_keys the new candidates use — every
  sector and company candidate would have silently failed the coverage filter. Found and fixed
  during this milestone.
- **A real bug in the persistence function found in review**: `resolved_item_ids.append(...)` and
  the entire per-article `DailyDataNews` loop were indented one level too shallow — valid Python,
  so nothing errored, but they silently ran only once (using whatever candidate was left over from
  the last loop iteration) instead of once per candidate. Every `DailyDataItem` was still being
  created/resolved correctly, but only the *last* candidate's articles were ever being persisted.
  Caught by review, not by any tool.
- **Design decision, deliberately accepted as a known risk**: `marketaux_service.py` still searches
  news for all 11 sectors even though only the best/worst two are ever persisted as items (kept
  because Marketaux's 100/day cap has comfortable headroom either way — 46 vs. 55 of 100 — so
  narrowing wasn't worth the added complexity). Separately: a full-pipeline retry-from-scratch on a
  day that already used most of the daily Marketaux quota could theoretically push past 100/day —
  explicitly accepted as an unlikely edge case to revisit later rather than solve now.

**3. The 48-hour cleanup**, `delete_stale_daily_data()` in the same file — a single bulk `DELETE`
against `DailyDataItem` where `fetched_at` is older than `STALE_DATA_HOURS` (48); `DailyDataNews`
cleanup needs no separate query at all, since it happens automatically via the `ON DELETE CASCADE`
FK. One typing-only issue fixed: `Session.execute()`'s declared return type (`Result[Any]`) doesn't
include `.rowcount`, even though the `CursorResult` it actually returns for a DML statement does —
resolved with `typing.cast("CursorResult[Any]", ...)` rather than any change in actual behavior.

**End-to-end verification, run live against real APIs and the real database:** 40 of 46 possible
candidates (39 FRED + 3 index quotes + 2 picked sectors + gainer + loser) survived the coverage
filter; 40 `DailyDataItem` and 113 `DailyDataNews` rows landed in Supabase, confirmed by direct
query. Skip-if-exists proven by running the exact same persist call twice — identical IDs both
times, row counts unchanged. Cascade delete proven by backdating one real persisted row to 49 hours
old, running `delete_stale_daily_data()`, and confirming: exactly 1 row reported deleted, that row
gone, its 3 linked `DailyDataNews` rows also gone with no orphans, and the remaining item count
correctly dropped by exactly one.

### Milestone 16 — Marketaux Service (complete, 2026-07-29)

`backend/app/schemas/marketaux_data.py` (`MarketauxArticle`) and
`backend/app/services/marketaux_service.py` — `fetch_marketaux_articles` (single search),
`build_news_search_items` (combines 39 FRED indicators + 3 index quotes + 11 sectors + gainer +
loser = 55 items), `fetch_all_articles` (concurrent batch fetch, semaphore-bounded, skip-and-continue
per item). Verified end-to-end against the live API: 129 articles across 46 of 55 items, 9 with no
fresh coverage (expected). Found and fixed a real bug during verification: Marketaux's
`published_after` rejects microseconds and any timezone offset/`Z` suffix — needs a bare
`YYYY-MM-DDTHH:MM:SS` (fixed via `.strftime(...)` instead of `.isoformat()`).

### Milestone 15 — FRED Service (complete, 2026-07-26)

`backend/app/schemas/fred_data.py` (`FredObservation`) and `backend/app/services/fred_service.py`
— `FRED_INDICATORS` (all 39 verified series), `fetch_fred_observation` (single indicator),
`fetch_all` (concurrent batch fetch, same semaphore/skip-and-continue pattern as Marketaux).
Verified end-to-end against the live API: all 39 of 39 indicators fetched successfully.

### Milestone 14 — Category & Topic Selection (core flow complete and device-verified, 2026-07-30)

**Done:**
- `users.category`/`users.additional_topics` columns + migration.
- `GET`/`PUT /v1/users/me/preferences` backend endpoint, wired into `v1_router`.
- `SelectCard` (single-select) and `TopicChips` (multi-select) UI primitives, both new — first
  custom interactive components in the app beyond button/card/badge/separator/text.
- `app/(onboarding)/category.tsx` and `topics.tsx` — full onboarding flow: category screen submits
  immediately, topics screen fetches existing preferences first (so it doesn't clobber the saved
  category), then submits both together. Both screens wrapped in `ScrollView` (were plain `View`,
  clipping the Continue button off-screen).
- `mobile/lib/redirectAfterAuth.ts` — checks the signed-in user's saved preferences after any
  auth success and routes to `/category` if `category` is still `null`, or `/` otherwise; falls
  back to `/category` on any fetch failure. Wired into all six sign-in/sign-up success paths
  (email/password, Google, Apple, across both screens).
- `sign-in.tsx`/`sign-up.tsx` now guard against an already-signed-in user re-attempting sign-in
  (was throwing "You're already signed in" SSO errors) — redirects via `redirectAfterAuth` instead.
- **Verified end-to-end on a real device**: sign-up → `/category` (pick one) → `/topics` (pick
  several) → `/`, confirmed against the live database with real `category`/`additional_topics`
  values persisted.

**Bugs found and fixed during this device-testing pass:**
- `CLERK_JWKS_URL` in `backend/.env` was pointed at the bare Clerk domain instead of
  `/.well-known/jwks.json` — meant `ClerkHTTPBearer` had no signing keys to verify against, so
  *every* authenticated request 403'd regardless of token validity. Fixed.
- `TopicChips`' original implementation (`Badge` wrapped in an extra `View`, inside `Pressable`)
  silently never registered taps at all — no visual selection, no console output, nothing.
  Rebuilt without the `Badge`/nested-`View` layers (styling the `Pressable` directly instead);
  confirmed working. Root cause was never conclusively isolated (tried: explicit sizing on
  `Pressable`, removing `flex-wrap`, `role="radio"` vs `"checkbox"`, full Metro cache clear — none
  of those alone fixed it) — worth keeping in mind if a similar "Pressable wrapping a styled View
  wrapping Text, inside flex-wrap" pattern silently fails to register touches elsewhere later.

**Still to do for Milestone 14 (not blocking M15-17, but not forgotten):**
- Name field collection (decided earlier to live in this onboarding flow, not via Clerk sign-up
  fields) — not yet added to either screen.
- Settings screen for changing category/topics later (scoped as part of M14, not built yet).

### Milestone 13 progress so far (2026-07-20)

**Clerk project set up, all config wired and verified:**
- `CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`, `CLERK_JWKS_URL` all in `backend/.env` +
  `.env.example` (the "read by Settings today" section) and `Settings` — confirmed loading
  correctly. `EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY` in `mobile/.env.local` + `.env.local.example`.
- Custom session token claims added in the Clerk Dashboard (Sessions → Customize session token):
  `phone_number` (`{{user.primary_phone_number}}`), `email` (`{{user.primary_email_address}}` —
  redundant since Clerk's JWT v2 already includes `email` by default, but harmless), `full_name`
  (`{{user.full_name}}`). Verified shortcode names against Clerk's own docs before using them.

**Backend, done and verified:**
- `backend/app/models/user.py` — `User` model: `id` (UUID PK), `clerk_user_id` (unique + indexed
  str), `email`/`phone_number`/`name` (all nullable — a user can sign up phone-only with no email,
  or vice versa). Registered in `app/models/__init__.py`. Passes `ruff`/`mypy --strict` clean.
- Two Alembic migrations generated, reviewed, and applied against live Supabase (after resuming
  the project from an auto-pause — a free-tier Supabase project pauses after inactivity, has an
  in-dashboard Resume button, takes a few minutes to come back): `58f1707ee1f7` (create `users`
  table) and `a4154f5fc063` (add `name` column, added after the fact). Both verified via direct
  `inspect(engine)` column checks, not just "the command didn't error."
- `backend/app/core/auth.py` — `get_current_user` dependency, using `fastapi-clerk-auth`'s
  `ClerkHTTPBearer` to verify the token, then look-up-or-create the local `User` row by
  `clerk_user_id`. Two real bugs caught in review and fixed: `return user` was originally nested
  inside the `if user is None:` block, meaning every *returning* user (not first-time sign-ups)
  got `None` back from the dependency — would have broken auth entirely for anyone after their
  first request. Also a missing type annotation on the `credentials` parameter (`mypy --strict`
  requirement) — resolved with an explicit `credentials: Any`, since `fastapi-clerk-auth` ships no
  type stubs at all (a `[[tool.mypy.overrides]]` entry for `fastapi_clerk_auth.*` was added to
  `pyproject.toml` to silence the resulting "missing stubs" noise without weakening strict mode
  for the rest of the codebase). Passes `ruff`/`mypy --strict` clean now.
- `fastapi-clerk-auth` added to `requirements.txt` and installed.

**Mobile, packages installed but no screens/provider wired up yet:**
- `@clerk/expo` (correct current package name — renamed from `@clerk/clerk-expo`, v3.x current as
  of March 2026) and `expo-secure-store` installed. One real mistake caught by `expo-doctor`:
  `expo-secure-store` was first installed via plain `npm install`, landing on `57.0.1` instead of
  the SDK-54-compatible `~15.0.8` — Expo-managed native modules need `npx expo install <name>`,
  not plain `npm install`, to resolve the right version. Fixed; `expo-doctor` clean except one
  unrelated pre-existing `expo` patch-version lag, not touched.

**Mobile progress update (2026-07-20):**
- `<ClerkProvider>` is done, verified, and committed — wrapped as the outermost provider in
  `mobile/app/_layout.tsx`, `publishableKey` read via a fail-fast local variable (not inline
  `process.env` access — TypeScript can't narrow a raw property access, only a checked local
  variable), `tokenCache` from `@clerk/expo/token-cache` wired in. Passes `tsc`/`eslint`/`prettier`.
- `mobile/app/(auth)/sign-in.tsx` exists (route group, not `app/auth/` — route groups don't add a
  URL segment). **Phone-only now** (Google/Apple were built partway then deliberately dropped —
  see the decision note below). Both `handlePhoneSignIn` (send code) and `handleVerifyingPhoneCode`
  (verify code + `finalize()`) are written, buttons are wired to `onPress`, `getErrorMessage`
  (`mobile/lib/utils.ts`, added alongside `cn()`) is used for safely extracting a message from a
  caught `unknown` error. **One known bug, not yet fixed**: `handleVerifyingPhoneCode`'s closing
  brace for its `finally` block and the closing brace for the function itself got collapsed into
  one — so `clerkIsFetching`/`authenticationIsLoading` (declared right after) end up scoped
  *inside* `handleVerifyingPhoneCode` instead of at the component's top level, making them
  inaccessible from the `return (...)` JSX below ("cannot find name"). Fix: add the missing closing
  brace right after the `finally` block, matching `handlePhoneSignIn`'s correct pattern just above
  it in the same file.

**A genuinely important discovery, worth reading before touching any more Clerk code:** this
project's exact installed `@clerk/expo` version (Core 3, `^3.7.8`) uses a fundamentally different
API shape than what's described in Clerk's own docs/most tutorials indexed by search engines
(which describe an older/legacy pattern). Confirmed by reading the actual shipped `.d.ts` files
directly (`node_modules/@clerk/expo/node_modules/@clerk/shared/dist/types/state.d.ts` and
`signInFuture.d.ts`), not from any web source:

- `useSignIn()` returns `{ signIn, errors, fetchStatus }` — **not** `{ signIn, setActive,
  isLoaded }` as most docs/tutorials describe. `setActive`/`isLoaded` don't exist in this version.
- All the actual sign-in methods live *on* the `signIn` object itself (a rich `SignInFutureResource`,
  not a plain trigger function): `signIn.password()`, `signIn.phoneCode.sendCode()`/`.verifyCode()`,
  `signIn.emailCode.sendCode()`/`.verifyCode()`, `signIn.sso()` (unified OAuth/enterprise, takes a
  `strategy` like `'oauth_google'`), `signIn.finalize()` (replaces `setActive()`), `signIn.mfa.*`,
  `signIn.status` (readonly, tracks flow progress: `'needs_identifier'`, `'needs_first_factor'`,
  `'complete'`, etc.) — every method returns `Promise<{ error: ClerkError | null }>`.
- The dedicated per-provider hooks (`useSignInWithGoogle`, `useSignInWithApple`) exist too, but
  their real returned property names are `startGoogleAuthenticationFlow`/
  `startAppleAuthenticationFlow` (with the `Flow` suffix) — not the shorter names that seemed
  intuitive and that most docs imply.
- **When in doubt about this SDK's actual API surface, read the real `.d.ts` files in
  `node_modules/@clerk/expo` directly rather than trusting search/docs** — this is genuinely
  newer (Core 3, March 2026) than most indexed content, and got real method/property names wrong
  twice this session before checking the source directly settled it.
- **Decision reversed: Google and Apple sign-in are dropped, phone number is now the only sign-in
  method.** Reasoning chain worth knowing: while wiring up `useSignInWithGoogle`, its own `.d.ts`
  doc comment revealed it's a *stub* requiring a separate uninstalled package
  (`@clerk/expo-google-signin`) for real native sign-in, and recommends `useSSO()` instead — which
  is browser-based (via `expo-web-browser`), a better fit for this project's Expo-Go-only workflow
  (no dev client set up) than native Google/Apple SDKs would be. Rather than switch to `useSSO()`,
  the user decided to just drop Google/Apple entirely and keep phone-only, favoring the design
  system's own "Simplicity Wins" principle. Google/Apple imports/hooks/handler/buttons have since
  been fully removed from `sign-in.tsx` — phone is the only method now.

### Milestone 13 progress update (2026-07-21)

- **`sign-in.tsx` and `sign-up.tsx` are both done, correct, and verified** (`tsc`/`eslint`/
  `prettier` all clean) — phone-only, full send-code → verify-code → `finalize()` flow on both.
  Real bugs caught and fixed along the way: a brace-matching bug in `handleVerifyingPhoneCode`
  that trapped `authenticationIsLoading` inside the function instead of the component's top level
  (fixed); a mislabeled button on `sign-up.tsx` showing "Verify code" on the phone-number step
  instead of "Continue with phone" (fixed). Confirmed from the real `SignUpFutureResource`/
  `SignInFutureResource` types (not assumed): sign-up's phone methods live under
  `signUp.verifications.sendPhoneCode()`/`verifyPhoneCode()`, a different nesting than sign-in's
  `signIn.phoneCode.sendCode()`/`verifyCode()`; sign-up's `create()` takes `phoneNumber` where
  sign-in's takes a generic `identifier`; and `errors.fields.identifier` (sign-in) becomes
  `errors.fields.phoneNumber` (sign-up) — `SignUpFields` has no `identifier` key at all.
- **`email` removed entirely from `User`** (model + `get_current_user`) — no longer needed now
  that Google/Apple (the main source of an email claim) are gone, phone-only doesn't need it.
  Migration `859c74aa86e1_drop_email_from_users.py` generated, reviewed, and applied against
  Supabase — model and live database confirmed back in sync (`id`, `clerk_user_id`, `phone_number`,
  `name`, `created_at`, `updated_at`).
- **First real end-to-end device test attempted, and a real gap found**: started the backend
  (`--host 0.0.0.0`, LAN IP in `mobile/.env.local` needed updating — it had gone stale since a
  previous session, same known gotcha as before) and the Expo dev server, opened the app in Expo
  Go — but `app/index.tsx` is still the old Milestone 10 health-check screen, and **nothing in the
  app navigates to `/sign-in` or `/sign-up` yet**. The routes exist (Expo Router route groups don't
  add a URL segment) but nothing links to them. Planned fix, not yet done: add a temporary
  `<Link href="/sign-in">` on the home screen to actually test the flow, then build real
  auth-gating (redirect unauthenticated users automatically) as its own deliberate step afterward
  — don't conflate the temporary test link with the real solution.

### The Milestone 12 pivot story (historical — read if you need the full FMP background)

Milestone 12 started, per the roadmap, as "Finnhub Service" — fetch today's economic calendar
events from Finnhub. Config/tooling was wired up (`FINNHUB_API_KEY` in `Settings`, `httpx` added
as the HTTP client), and a full `finnhub_service.py` + `schemas/economic_event.py` implementation
was written, reviewed, and got to a clean state (`ruff check`/`ruff format --check`/`mypy --strict`
all passing). But the actual end-to-end verification call against the real Finnhub API returned
**`403: You don't have access to this resource`** — Finnhub's economic calendar endpoint turned out
to require a paid plan (confirmed via the account's own pricing page: a dedicated
"Economic Data" pricing table shows Economic Calendar gated behind a $50/month plan, not included
in either the free or the general $3,500/month "All-In-One" tier).

Pivoted to trying **Financial Modeling Prep (FMP)** instead, since it looked like a plausible free
alternative with a similar `from`/`to` + API-key-as-query-param shape. Same result, twice over:
FMP's newer `/stable/economic-calendar` endpoint returned `402 Payment Required`, and the older
legacy `/api/v3/economic_calendar` endpoint (what most third-party blog posts/docs referenced)
returned a `403` explaining it's a fully retired endpoint ("only available for legacy users who
have valid subscriptions prior to August 31, 2025"). **Conclusion, confirmed empirically across
two providers: there is no viable free/personal-use source for a scheduled economic-events
calendar with actual-vs-forecast data.** Don't re-attempt this without a real budget decision —
Finnhub's $50/month plan is the cheapest confirmed-working option found so far.

**Scope was renegotiated as a result**, not just "swap the provider." Rather than a calendar of
discrete scheduled events, the daily briefing's data layer is being rebuilt around FMP's free-tier
market-data endpoints (all confirmed working empirically with a real key):

- **Market Snapshot** — index quote(s) (e.g. S&P 500) via `/stable/quote`.
- **Sector Movers** — best/worst performing sector via `/stable/sector-performance-snapshot`.
- **Company Spotlight** — pull `/stable/biggest-gainers` and `/stable/biggest-losers` (50 each,
  confirmed free), look up each symbol's `marketCap` via `/stable/profile` (also confirmed free —
  and conveniently returns company name/sector/market-cap in one call), filter out anything under
  **$10B** market cap (to avoid obscure micro-caps dominating the raw gainers/losers lists — the
  unfiltered lists were dominated by penny stocks like "Twin Vee Powercats Co." +45%, not
  meaningful to a general reader), and take the top qualifying gainer/loser.
- Explicitly rejected: Yahoo Finance / `yfinance` — no official API exists (Yahoo shut it down in
  2017); `yfinance`-style access reverse-engineers Yahoo's internal endpoints, which can break
  without notice and isn't a stable foundation for a scheduled production job, even though it's
  broader/free. Also technically "personal use only" per Yahoo's own terms.
- FMP's own server-side "screener" filtering (e.g. `marketCapMoreThan` as a query param on
  `biggest-gainers`) was tested and confirmed **not supported on the free tier** — the parameter
  is silently ignored. Filtering has to happen client-side, after fetching.

**This is a real, unresolved open question, not yet decided:** Milestones 13 (Store Finnhub
Events), 16 (FRED Service), 18 (Marketaux), and 20 (OpenAI) — everything downstream of Milestone
12 — were designed around **discrete "events"** flowing through the pipeline (fetch events → match
each event to a FRED series → search news per event → rank events with OpenAI). That design
assumption no longer holds now that Milestone 12's output is a market snapshot + sector movers +
one spotlight company, not a list of events. **This needs a real design conversation before
starting Milestone 13** — don't assume the old pipeline shape still applies. `docs/01-product-
requirements.md` §10 (MVP Definition) also still describes the product around "five most important
economic events" and needs a matching reframe — deliberately deferred as its own separate
conversation, not done as part of this docs cleanup pass.

### Current implementation state — Milestone 12 is functionally DONE, not yet formally signed off

- **`backend/app/services/fmp_service.py` is complete and verified working end-to-end against the
  real, live FMP API** (2026-07-17): `fetch_market_snapshot`, `fetch_sector_performance`,
  `pick_best_and_worst`, `fetch_top_gainer_spotlight`, `fetch_top_loser_spotlight`. Passes
  `ruff check`, `ruff format --check`, and `mypy --strict` clean. A real test run returned real
  data (S&P 500/Dow/Nasdaq quotes, all 11 sectors with Technology best/Consumer Defensive worst,
  and a genuine real-world validation of the "don't show if nothing clears $10B" design: the top
  gainer came back `None` that day, while the top loser correctly surfaced Intuitive Surgical
  (ISRG), a real $124B company down 13% — not an obscure penny stock, which was the whole point of
  the market-cap filter). Committed as `271b612`.
- `backend/app/schemas/fmp_data.py` — `IndexQuote`, `SectorPerformance`, `CompanySpotlight`, all
  matching the implementation exactly. Replaced (and the file itself renamed from) the abandoned
  `economic_event.py`/`EconomicEvent` — that dead weight is gone, not just unused.
- `backend/app/core/config.py` / `backend/.env.example` — `fmp_api_key` wired and confirmed
  working. Real `backend/.env` has a real, working `FMP_API_KEY` (gitignored, not committed).
- **Still open, not yet done:**
  - **Key rotation** — the FMP key was briefly printed into a terminal error message during
    ad-hoc testing early in this milestone (same category as the Milestone 6 Supabase key
    exposure). Worth rotating from the FMP dashboard; not yet confirmed done.
  - **Formal sign-off** — `docs/03-development-roadmap.md`'s Milestone 12 section was updated
    *during* the pivot (objective/deliverables/acceptance criteria), but this resume-prompt doc's
    "Completed Milestones" checklist still doesn't list Milestone 12, and there's no
    "Milestone 12 (complete)" write-up yet in the style of Milestones 3-11 below. Do this once the
    downstream-pipeline question (next bullet) is at least scoped, so the sign-off reflects the
    final shape of things.
  - **The big one: Milestones 13/16/18/20 need a full re-scoping conversation, not just a
    rename.** These were designed around discrete "events" flowing through the pipeline (fetch
    events → match to FRED series → search news per event → rank with OpenAI) — Milestone 13
    specifically ("Store Finnhub Events") is entirely about persisting/deduplicating/filtering
    events, none of which fits Milestone 12's actual output anymore (a market snapshot + sector
    movers + a company spotlight, no discrete events at all). **This is explicitly the next thing
    to tackle when picking this back up** — work out what the app's remaining milestones should
    actually be, given the FMP pivot, before writing any more code. Likely touches: what
    persistence looks like (probably `index_quotes`/`sector_performance`/`company_spotlights`
    tables instead of `economic_events`, using natural `(symbol/sector, date)` keys instead of a
    synthetic event ID — no hashing needed this time, see Important Decisions), what Milestone 16
    (FRED)/18 (Marketaux)/20 (OpenAI) even mean without discrete events to enrich, and whether
    `docs/02-system-architecture.md` §5's data-flow diagram and the `economic_events` table under
    §12 (both deliberately left un-updated during the mechanical docs pass) still make sense at
    all.
  - `docs/01-product-requirements.md` §10 (MVP Definition) still describes "five most important
    economic events" — also deferred, likely resolved together with the milestone re-scoping
    above rather than as a separate pass.

Working agreement from Milestone 10 (user writes pseudocode/implementation, Claude handles
configuration/tooling + technical edge cases + Phases 1/5/6/7) held throughout this pivot and the
full implementation — review caught several real bugs along the way (wrong `Settings` field names
repeating a pattern from the Finnhub version, a copy-pasted Finnhub URL left in a new constant, an
`httpx.Client()` connection-reuse optimization that initially didn't reach the code it was meant
to help, a `client.HTTPError`/`httpx.HTTPError` typo) — all found and fixed through review, then
verified against the real API, not just type-checked.

### Milestone 11 — Database Models & Migrations (complete)

Per the roadmap, this milestone is literally "create SQLAlchemy models and Alembic migrations for
the 7 core tables" — but that work already happened in Milestone 6, out of necessity (Alembic's
`--autogenerate` needed the models to exist to diff against). This overlap was flagged and
predicted back in Milestone 6's own notes. Reading the actual acceptance criteria against what
already existed: "tables exist in Supabase" and "migration runs from a clean database" were both
already true. The one real gap was "backend can create and query records" — nothing had ever
actually exercised the ORM layer; `GET /health` only ever ran a raw `SELECT 1`, which proves
connectivity, not that the model classes correctly map to real rows. This milestone's real,
non-overlapping work became: prove the ORM layer actually works, via real automated tests.

- **Decisions made (with reasoning):**
  - **A real `pytest` test suite, not a throwaway script.** "No automated tests exist yet" had
    been sitting in Known Issues since Milestone 8. A script proves something worked once, on the
    date it was run; a test is a permanent, machine-checked claim that gets re-run automatically
    by the existing CI (Milestone 8) on every future push — catching regressions in code this
    milestone touches, not just proving today's state.
  - **Explicit `db_session.delete()` + `commit()` cleanup in each test, not a transaction-rollback
    fixture.** A SQLAlchemy pattern exists where a fixture opens a savepoint-nested transaction
    and rolls it back after every test, so nothing a test does is ever actually permanent,
    regardless of cleanup code. That's the standard answer for larger, longer-lived test suites,
    but it's meaningfully more machinery (a manually-managed transaction, an event listener
    intercepting `commit()`) sitting invisibly in `conftest.py`, asking the user to trust it
    without being able to read and understand it line by line. Given this project's own repeated
    standing principle — don't build more infrastructure than what's needed right now — explicit,
    visible cleanup in each test was judged the more consistent choice for where the project
    actually is today. Worth revisiting toward the fixture pattern if the test suite grows enough
    that this repeatedly bites.
- **What got built:**
  - `pytest` added to `requirements-dev.txt` and installed; `[tool.pytest.ini_options]` in
    `pyproject.toml` (`testpaths = ["tests"]`, `pythonpath = ["."]` — the latter needed because,
    unlike `uvicorn` run from `backend/`, pytest doesn't automatically know to look there for the
    `app` package).
  - `backend/tests/conftest.py` — a `db_session` fixture: the test-context equivalent of
    `get_db()`, opening a `SessionLocal()` and closing it in `finally`, since tests run outside a
    FastAPI request and can't use the real dependency directly.
  - `backend/tests/test_models.py` — three tests, all passing and verified re-runnable:
    - `test_create_and_query_briefing` — creates, queries, and cleans up a `Briefing`; asserts the
      `id` UUID default and all field values round-trip correctly.
    - `test_create_and_query_economic_event` — creates a `Briefing` then a linked `EconomicEvent`
      (proving the foreign key relationship works), queries it back, cleans up both.
    - `test_create_and_query_delete` — proves the `ondelete="CASCADE"` constraint from Milestone 6
      actually fires: deletes only the parent `Briefing`, then confirms the linked `EconomicEvent`
      is gone too, with no separate cleanup needed since cascade handled it.
- **Real bugs found and fixed, several through the mentor review cycle rather than being caught
  by tooling:**
  - A missing required `source` field on `EconomicEvent` caused a real `NotNullViolation` the
    first two times it was attempted — confirmed by actually running the test, not just reading
    the code.
  - Two separate leftover-row incidents: because cleanup code sits at the end of a test, a test
    that fails partway through (on an assertion or a missing-field error) never reaches its own
    cleanup, leaving a real permanent row in the live Supabase database that then collided with a
    later run's insert on the same `briefing_date` (a unique column). Manually cleaned up outside
    the test both times this happened during development.
  - **A genuinely subtle, non-obvious bug**, caught by actually running the test rather than
    reading the code: cleanup explicitly called `db_session.delete(queried_event)` before
    `db_session.delete(briefing)`, intending to control deletion order and avoid relying on
    cascade — but SQLAlchemy's flush ordering isn't guaranteed by the order `.delete()` is called
    in Python; it's driven by ORM-level `relationship()` configuration, which none of the 7
    models use (they only have raw `ForeignKey` columns). The actual SQL ended up deleting the
    `Briefing` first, and Postgres's own cascade constraint silently removed the `EconomicEvent`
    as a side effect — surfaced only as a `SAWarning` ("expected to delete 1 row(s); 0 were
    matched"), not a failure. Fixed by adding `db_session.flush()` between the two deletes, which
    forces the child's DELETE to actually execute before the parent delete is even staged.
  - **A conceptual bug in the cascade test itself**, caught in review before it was ever run: the
    first version of `test_create_and_query_delete` deleted the `EconomicEvent` directly in the
    `Act` step instead of the `Briefing`. It would have passed — trivially, and for the wrong
    reason — proving nothing about whether cascade delete actually works, since directly deleting
    a row obviously removes it regardless of any FK constraint. A test that passes without
    exercising the behavior it claims to verify is worse than not having the test at all, since it
    creates false confidence.
- **Verified working:** `ruff check`, `ruff format --check`, and `mypy --strict` all pass clean;
  all three tests pass individually and as a suite, confirmed re-runnable by running the full
  suite twice in direct succession with no leftover-data collisions; manually queried Supabase
  directly after the cascade test to confirm both rows were actually gone, not just that the
  test's own assertion (which queries the same database) reported so.

### Milestone 10 — First End-to-End Connection (complete)

First milestone under the new working agreement (see Important Decisions): the user wrote the
pseudocode and implementation; Claude handled configuration/tooling and reviewed. Full mentor
workflow (Phases 1–7) was followed, with Phase 3 (pseudocode) and Phase 4 (implementation) now
done by the user instead of Claude.

- **Decisions made (with reasoning):**
  - **Fetch/API logic stays inline in the hook** (`useHealthCheck.ts`), not split into a separate
    `lib/api.ts` — for exactly one endpoint, a shared API wrapper would be solving a duplication
    problem that doesn't exist yet. Revisit once Milestone 11+ adds more hooks and the
    duplication becomes real.
  - **The home screen's placeholder content was replaced outright**, not kept alongside the
    health check — the "Walris" heading/"Get started" button was itself throwaway Milestone-4
    scaffolding, and since the health check display was explicitly framed as temporary
    proof-of-connection (not a permanent fixture), showing only that gives the cleanest signal
    the milestone is done. It'll get replaced again once real screens land.
  - **No CORS middleware added — a correction, not a decision.** Claude initially told the user
    CORS would be needed on the backend for the mobile app's requests to succeed, which was
    wrong: CORS is a browser-enforced restriction, and React Native's `fetch` (backed by native
    networking, not a browser engine) isn't subject to it. This only becomes relevant if
    `expo start --web` is ever tested in an actual browser. Worth remembering so this doesn't get
    re-litigated incorrectly in a future milestone.
- **What got built:**
  - `mobile/hooks/useHealthCheck.ts` — `HealthResponse` interface, `getHealth()` (fetches
    `${EXPO_PUBLIC_API_BASE_URL}/health` via `process.env`, throws on `!response.ok`), and
    `useHealth()` (a TanStack Query hook: `queryKey: ["health"]`, `queryFn: getHealth`, no
    `enabled` guard needed since there's no conditional input to wait on).
  - `mobile/app/index.tsx` — `HealthProfile` component branching on `isPending`/`isError`/success,
    using `Text`/`View` (React Native's real primitives); `Home` now renders `HealthProfile`
    directly in place of the old placeholder.
  - `mobile/.env.local` (gitignored, not committed) — `EXPO_PUBLIC_API_BASE_URL` pointing at the
    dev machine's LAN IP, required because the phone is a separate device from the Mac running
    the backend.
  - `mobile/package.json` — `@types/node` added as an explicit devDependency (previously only
    present transitively).
  - `.vscode/settings.json` (gitignored, local-only, not committed) — `typescript.tsdk` pointing
    at the workspace's TypeScript install, fixing VS Code's language server defaulting to its own
    bundled TypeScript version instead of the project's.
  - Documented run command: `uvicorn app.main:app --reload --host 0.0.0.0` — the default bind
    (`127.0.0.1`) only accepts same-machine connections, which would never let the phone reach it.
- **Real bugs found during review** (all caught before ever running the app, across several
  passes of the user's pseudocode and then real implementation):
  - A self-recursive hook (`useHealth` calling itself instead of `useQuery`).
  - `queryKey` referencing an undefined `status` variable — leftover copy-paste from a reference
    example whose dynamic `userId` parameter doesn't apply to a parameterless health check.
  - `enabled: Boolean()` called with zero arguments always evaluates `false`, which would have
    meant the query never ran — a subtle miss of the reference example's actual intent
    (`enabled: Boolean(userId)` guards a real condition; there's no equivalent condition here).
  - A destructuring rename (`data: status`) that would have rendered the entire response object
    instead of just the status string.
  - A typo (`fron` instead of `from`) and an import path pointing at a nonexistent relative file,
    later corrected to the project's `@/*` alias once the destination file was clarified.
  - **The most significant one:** JSX (`HealthProfile`) was written inside a `.ts` file, which
    doesn't compile — TypeScript requires `.tsx` for JSX. Underneath that, a second, subtler bug:
    the component used raw HTML tags (`<p>`, `<section>`, `<h2>`), which don't exist in React
    Native (no browser, no DOM) and would have crashed at runtime with an "Invariant Violation"
    even after fixing the file extension — TypeScript's JSX types didn't catch this because
    `@types/react`'s default HTML intrinsic elements silently type-check in this setup, so it's
    invisible to `tsc`/ESLint and only shows up by actually running the app. Fixed by moving the
    component into `app/index.tsx` (already a `.tsx` file) and swapping the HTML tags for
    `Text`/`View`.
- **A real editor-only issue, not a project bug:** VS Code's TypeScript language server was
  running its own bundled version (`6.0.3`) instead of the project's actual installed version
  (`5.9.3`), so it couldn't see `@types/node` and falsely flagged `process.env.EXPO_PUBLIC_API_
  BASE_URL` as an error — while the real project compiler (the one CI runs) stayed clean the
  entire time. This is a useful pattern to remember: when an error only shows up in the editor
  but never in `tsc`/CI output, suspect an editor-vs-project TypeScript version mismatch before
  assuming the code is actually broken.
- **Verified working:** the full loading/error/success cycle was tested end-to-end on a physical
  iPhone via Expo Go against the real running backend — success confirmed ("Backend Connected"
  rendered after a real network round-trip over the LAN), error state confirmed by deliberately
  stopping the backend and observing the error branch render `"Network request failed"` instead
  of crashing or hanging, then the backend was restarted and reconfirmed healthy.

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

- **Personalization pivot (2026-07-19):** Walris moved from "one identical briefing for everyone"
  to a per-user personalized briefing — users sign up (Clerk, pulled into V1 from its originally
  planned V2 slot), pick one of 7 categories, optionally add extra topics, and get an
  individually-generated OpenAI briefing built from 39 verified FRED indicators + Milestone 12's
  FMP data + Marketaux news (55 calls/day, one per data field, same-day-recency-filtered). Data is
  temporary (48-hour deletion), not a permanent historical archive. Full plan, reasoning, and
  milestone breakdown: `docs/09-personalization-pivot-plan.md`. This is reflected in `docs/01`
  §1/§10/§11, `docs/02` (auth, data flow, database tables, caching, security — extensively
  rewritten), and `docs/03` (Milestones 13-23 fully replaced; Milestones 27+ flagged as needing
  their own re-scoping pass before being started).
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
  without them. Milestone 11 confirmed this prediction: it was a light touch-up (adding the first
  real tests), not new model design.
- **Automated testing uses `pytest`, with explicit per-test cleanup, not a transaction-rollback
  fixture** (Milestone 11) — see Milestone 11 notes for the full reasoning. Revisit toward the
  fixture pattern if the test suite grows large enough that leftover-data-on-failure repeatedly
  becomes a real problem.
- **SQLAlchemy flush ordering across different mapped classes is not guaranteed by the order
  `.delete()`/`.add()` is called in Python** unless an ORM-level `relationship()` connects them
  (established Milestone 11) — none of the 7 models currently use `relationship()`, only raw
  `ForeignKey` columns. When a single `commit()` needs to affect rows in a specific cross-table
  order (e.g. deleting a child before its parent), call `db_session.flush()` between the
  operations to force the order explicitly, rather than assuming Python call order controls it.
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
- **Working agreement, confirmed working in practice (Milestone 10, 2026-07-11; again in
  Milestone 11, 2026-07-12):** the split held up well across both milestones. The user wrote
  pseudocode/implementation through several review passes each time, catching and fixing issues
  themselves each round; Claude's review caught real bugs — including a test that would have
  passed while proving nothing (Milestone 11's cascade test deleting the wrong object) — rather
  than writing the fixes directly. Worth continuing as-is into Milestone 12.
- **CORS is not needed for native mobile requests** (established Milestone 10) — it's a
  browser-enforced restriction; React Native's `fetch` (native networking, not a browser engine)
  isn't subject to it. Only relevant if `expo start --web` is tested in an actual browser.
- **When an error shows up only in the editor but never in `tsc`/CI output** (established
  Milestone 10), suspect an editor-vs-project TypeScript version mismatch before assuming the
  code is broken — check the TypeScript version VS Code's status bar reports against the
  project's actual installed version.
- **Explain-in-detail trigger:** whenever a concept referenced in
  `docs/08-code-reference-milestones-3-6-9.md` comes up again during later work (SQLAlchemy
  models/sessions, Alembic migrations, exception handlers, middleware, response models, UUIDs,
  JSONB, cascade deletes, connection pooling, etc.), explain it in enough detail that the user has
  what they need to actually write the next step themselves — don't assume it's already
  internalized just because it was explained once when it was originally built.
- **No free/personal-use economic calendar data source exists, confirmed empirically across two
  providers (Milestone 12, 2026-07-16):** Finnhub's calendar requires a $50/month plan; FMP's
  equivalent endpoints are either paid (`402`) or fully retired (`403`, legacy endpoint sunset
  August 2025). Don't re-attempt building around a free scheduled-events calendar without a real
  budget decision first — see the Milestone 12 section above for the full story.
- **Company Spotlight uses a $10B market-cap floor, filtered client-side** (Milestone 12) — FMP's
  free `biggest-gainers`/`biggest-losers` endpoints return real data but are dominated by obscure
  micro-caps; a server-side `marketCapMoreThan` filter was tested and confirmed **not supported**
  on the free tier (silently ignored). Client-side filtering via a `/stable/profile` lookup per
  symbol is the only option, and is affordable (100 extra calls max, well under the 250/day free
  limit for a once-a-day job).
- **Yahoo Finance / `yfinance` rejected as a data source** (Milestone 12) — no official API has
  existed since 2017; unofficial access reverse-engineers Yahoo's internal endpoints and can break
  without notice, an unacceptable risk for a scheduled production job, despite offering broader
  free data than FMP.
- **The daily job's "today" should use this machine's/the target user's local timezone, not UTC**
  (Milestone 12) — the product intent is the briefing arriving on the same local morning, which
  breaks if a future deployment's server defaults to UTC. Not yet fixed in code (`fetch_todays_
  economic_events`/whatever the FMP equivalent becomes still uses bare `date.today()`) — the
  eventual fix is explicit `zoneinfo`-based timezone handling, not relying on server config,
  deferred until the actual deployment milestone. Separately, `docs/02-system-architecture.md`
  §23 already recommends "6:00 AM ET" as the V1 schedule, which is a useful existing hint toward
  which timezone to hardcode when that milestone arrives.
- **Downstream pipeline design (Milestones 13/16/18/20) is an open question, not yet decided**
  (Milestone 12, 2026-07-16) — those milestones were designed around discrete "events" flowing
  through FRED matching/news search/OpenAI ranking; that assumption breaks now that Milestone 12
  produces a market snapshot + sector movers + one spotlight company instead. Needs a real design
  conversation before Milestone 13 starts, not an assumption that the old pipeline shape still
  applies.

## Current Architecture

**Frontend** — Expo SDK 54 + TypeScript scaffold complete. `app/_layout.tsx` wires
`SafeAreaProvider` → `QueryClientProvider` → React Navigation `ThemeProvider` → `Stack` →
`PortalHost`. `app/index.tsx` no longer holds a static placeholder — `Home` renders
`HealthProfile`, a component that calls `useHealth()` and branches on loading/error/success,
using `Text`/`View`. `hooks/useHealthCheck.ts` (new as of Milestone 10, first entry in
`hooks/`, matching `docs/02-system-architecture.md` §13's suggested structure) holds
`HealthResponse`, `getHealth()` (fetches `GET /health` via `EXPO_PUBLIC_API_BASE_URL`), and
`useHealth()` (the TanStack Query hook). `components/ui/` holds React Native Reusables
primitives (`button`, `card`, `badge`, `separator`, `text`) — `button` is currently unused since
the placeholder was replaced. `lib/` holds `utils.ts` (cn helper), `theme.ts` (Walris colors as
React Navigation theme), `queryClient.ts`. Styling is NativeWind (Tailwind-style `className`)
with Walris's actual design-system colors wired through `global.css` → `tailwind.config.js`. No
custom fonts loaded yet (deferred), no real screens/data fetching beyond the health check yet
(later milestones) — `theme/typography.ts` from `docs/02-system-architecture.md` §13 doesn't
exist yet. ESLint (flat config + `eslint-config-expo`) and Prettier (+
`prettier-plugin-tailwindcss`) are configured and passing clean. `mobile/.env.local` (gitignored)
now exists with a real `EXPO_PUBLIC_API_BASE_URL` value.

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
historical files). `tests/` (new as of Milestone 11) holds `conftest.py` (`db_session` fixture)
and `test_models.py` (three tests proving the ORM layer creates/queries/cascade-deletes real
rows) — the project's first automated test suite, run via `pytest` and configured in
`pyproject.toml` (`testpaths`, `pythonpath`).

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
  .vscode/
    settings.json              (gitignored, local-only; typescript.tsdk override — Milestone 10)
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
    .env.local                 (gitignored; EXPO_PUBLIC_API_BASE_URL filled in with LAN IP)
    app/
      _layout.tsx              (SafeAreaProvider > QueryClientProvider > ThemeProvider > Stack > PortalHost)
      index.tsx                 (Home renders HealthProfile: loading/error/success from useHealth())
    hooks/
      useHealthCheck.ts         (HealthResponse, getHealth(), useHealth() — Milestone 10)
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
    requirements-dev.txt       (-r requirements.txt, ruff, mypy, pytest)
    pyproject.toml             (Ruff lint+format config incl. alembic/versions exclude
                                 and Depends()/Query() bugbear allowlist; mypy strict config;
                                 [tool.pytest.ini_options]: testpaths, pythonpath)
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
        economic_event.py         (EconomicEvent — unused dead weight, abandoned Finnhub scope,
                                    not yet deleted; see Milestone 12)
      services/
        __init__.py
        fmp_service.py             (non-working/transitional — needs full rewrite; see Milestone 12)
      utils/__init__.py        (empty — nothing needed yet)
    tests/
      conftest.py               (db_session fixture — Milestone 11)
      test_models.py             (create/query/cascade-delete tests for Briefing, EconomicEvent)
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
- `mobile/hooks/useHealthCheck.ts` — first user-written implementation on the project:
  `HealthResponse`, `getHealth()`, `useHealth()` (TanStack Query hook wrapping `GET /health`)
- `mobile/app/index.tsx` — `Home` now renders `HealthProfile`, which calls `useHealth()` and
  branches on loading/error/success, replacing the Milestone 4 placeholder content
- `mobile/.env.local` — gitignored, holds the real `EXPO_PUBLIC_API_BASE_URL` (dev machine's LAN
  IP) needed for the phone to reach the backend over the network
- `.vscode/settings.json` — gitignored, local-only; `typescript.tsdk` pointing at the workspace's
  TypeScript install, fixing a VS Code editor-only false error (see Milestone 10 notes)
- `backend/tests/conftest.py` — the project's first test fixture (`db_session`)
- `backend/tests/test_models.py` — the project's first automated tests: create/query for
  `Briefing` and `EconomicEvent`, plus a cascade-delete test proving the Milestone 6
  `ondelete="CASCADE"` constraint actually works, not just that the migration declares it

## Known Issues

- **Resolved (2026-07-16):** global git identity (`user.name`/`user.email`) is now configured
  (`Kai Beltz` / `kainbeltz@gmail.com`), fixing the inconsistent auto-derived hostname-based
  identity from earlier commits (`kaibeltz@Kais-MacBook-Pro.local`,
  `kaibeltz@macbook-pro.mynetworksettings.com`, `kaibeltz@kais-mbp.mynetworksettings.com` — three
  distinct values across earlier commits). Not retroactively rewritten on old commits (not worth
  it for a cosmetic issue on a private repo) — only future commits are affected.
- System Python is 3.14.6. **Resolved as a non-issue**: every dependency added so far, including
  `pytest` in Milestone 11, has installed cleanly with prebuilt 3.14 wheels. No action needed.
- **CI does not run `pytest` yet, despite the backend now having a real test suite (Milestone
  11).** `.github/workflows/ci.yml`'s backend job still only runs Ruff/mypy. This isn't a simple
  oversight to fix by adding one line: the tests in `backend/tests/test_models.py` hit the real,
  live Supabase database directly, and CI currently has no `DATABASE_URL` (or any backend secret)
  configured at all — `Settings`' fail-fast validation would immediately reject a bare `pytest`
  step in CI with a missing-config error. Wiring this up for real requires a deliberate decision
  first: whether CI should run tests against the actual dev Supabase database (meaning a GitHub
  Actions secret holding real database credentials, and every push/PR inserting and deleting real
  rows in it) or a separate dedicated test database. Worth resolving explicitly, not by default,
  before adding the CI step — this is exactly the kind of gap that undercuts the reasoning used to
  justify choosing `pytest` over a throwaway script in the first place (that CI would re-run it
  automatically forever), since right now CI isn't actually doing that yet.
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
- **`backend/app/services/fmp_service.py` is in a non-working, transitional state** (Milestone
  12) — contains the entire old Finnhub implementation dead inside a `'''...'''` string (including
  a reference to the now-nonexistent `settings.finnhub_api_key`), followed by a rough diagnostic
  test snippet. Needs a full rewrite around the new market-snapshot/sector-movers/company-spotlight
  design — see the Milestone 12 section above.
- **The FMP API key was briefly exposed in a terminal error message** during ad-hoc testing
  (Milestone 12) — `httpx` exceptions include the full request URL, which contains `apikey=...` as
  a query param. Worth rotating from the FMP dashboard; not yet confirmed done.
- **Downstream pipeline design (Milestones 13/16/18/20) is unresolved** (Milestone 12) — those
  milestones assumed discrete "events" flowing through FRED matching/news search/OpenAI ranking;
  Milestone 12's new output (market snapshot + sector movers + one spotlight company) doesn't fit
  that shape. Needs an explicit design conversation before Milestone 13 starts.
- **`docs/01-product-requirements.md` §10 (MVP Definition) still describes the product around
  "five most important economic events"** — needs reframing to match the market-data pivot,
  deliberately deferred as its own separate conversation (not done as part of the Milestone 12
  docs cleanup).
- **`backend/app/schemas/economic_event.py` (`EconomicEvent`) is unused dead weight** from the
  abandoned Finnhub/calendar scope — not yet deleted; decide when the `fmp_service.py` rewrite
  happens.

## Commands

Backend (working now):

```bash
source backend/.venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0
```

`--host 0.0.0.0` is required (not just `--reload` alone) for the mobile app on a physical phone
to reach it — the default bind (`127.0.0.1`) only accepts connections from this same machine.

Health check: `curl http://127.0.0.1:8000/health` → `{"status":"ok"}`

Frontend (working now):

```bash
cd mobile
npx expo start
```

Scan the QR code with the Expo Go app (verified on a physical iPhone; no Xcode/Android Studio on
this machine, so no simulator available — see Known Issues). Requires `mobile/.env.local` to
exist with `EXPO_PUBLIC_API_BASE_URL` set to this Mac's current LAN IP, matching whatever the
backend is bound to — if the Mac's IP changes (different network, router reassigns it), update
`.env.local` and restart Metro (env vars are inlined at bundle time, not read at runtime).

Database (working now, from `backend/` with the venv active):

```bash
alembic upgrade head              # apply migrations
alembic revision --autogenerate -m "description"   # generate a new migration from model changes
```

Always read an autogenerated migration before applying it — don't trust it blindly, especially
the first one on a new table.

Tests (working now, from `backend/` with the venv active):

```bash
pytest tests/ -v
```

Runs against the real, live Supabase database (no separate test database exists yet — see Known
Issues) — each test in `test_models.py` creates and explicitly cleans up its own rows. Not yet
wired into CI (see Known Issues).

## Environment Variables

`backend/.env.example` and `mobile/.env.local.example` exist (Milestone 5); copy them to `.env` /
`.env.local` and fill in real values as each variable's owning milestone lands. `backend/.env`
now exists and is filled in for `ENVIRONMENT`, `DATABASE_URL` (Session pooler connection string),
`SUPABASE_URL`, and `SUPABASE_SERVICE_ROLE_KEY` (Milestone 6), and `FMP_API_KEY` (Milestone 12,
replacing the short-lived `FINNHUB_API_KEY` — Finnhub's calendar access turned out to require a
paid plan, see the Milestone 12 section above) — `ENVIRONMENT`, `DATABASE_URL`, and `FMP_API_KEY`
are actually read by `Settings` today; the Supabase URL/key are filled in for later use but not
consumed by any code yet. The rest remain reserved. The FMP key was briefly exposed in a terminal
error message during testing — worth rotating from the FMP dashboard as a precaution (see
Milestone 12 / Known Issues). `mobile/.env.local` now exists too (Milestone 10), with
`EXPO_PUBLIC_API_BASE_URL` set to the dev machine's LAN IP — read by `useHealthCheck.ts` via
`process.env`. Per `docs/02-system-architecture.md` §25, the full eventual set is:

Backend (`backend/.env`):

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

Mobile (`mobile/.env.local`):

```text
EXPO_PUBLIC_API_BASE_URL
```

## Next Steps

1. **PRIORITY when resuming: finish Milestone 13's mobile side.** The backend half is done and
   verified (see the Milestone 13 progress notes above) — `User` model, migrations,
   `get_current_user`. What's left: `<ClerkProvider>` in `mobile/app/_layout.tsx` (using the
   `tokenCache` from `@clerk/expo/token-cache`, already installed), then sign-up/sign-in screens
   (likely a new `app/(auth)/` route group — no route groups exist yet in this app). Once that's
   done, Milestone 13 is complete and Milestone 14 (Category & Topic Selection, per `docs/09`) is
   next. Note: `docs/03-development-roadmap.md`'s Milestones 27+ (mobile UI, notifications) have
   an explicit flag noting they still assume no-auth/single-global-briefing and need their own
   re-scoping pass before being started as-is — not urgent until Milestone 22ish is reached, but
   don't skip it when the time comes.
2. **Formally sign off Milestone 12** — add it to the "Completed Milestones" checklist above and
   write its own "(complete)" section in the style of Milestones 3-11 below, summarizing the
   pivot/decisions/bugs-caught the same way those do. Reasonable to do alongside #1 or separately.
3. Rotate the FMP API key (briefly exposed in a terminal error message during testing) as a
   precaution — still not confirmed done.
4. Decide whether/how to wire `pytest` into CI (see Known Issues) — needs a decision on test
   database strategy before it's a simple config change.
5. Continue the personalization pivot Milestones 13-23 per `docs/09`.
6. Once the personalization pivot's backend is complete, revisit and re-scope Milestones 27+
   (Mobile App, Notifications) against it before starting them.
