# Walris Resume Prompt

**Document:** docs/05-resume-prompt.md
**Last Updated:** 2026-09-02 (Milestone 34 — Mobile Integration Test Pass — is complete. Scoped to
iOS-only (this project has never had Android tooling — no Xcode-adjacent Android Studio, no
emulator, no physical device; tracked explicitly in Known Issues as a real follow-up, not silently
skipped). Rather than re-verifying each piece M24-M33 already tested in isolation, ran the full
flow as one continuous journey on a genuinely new account: sign-up with a new email → correctly
routed to `/category` (a brand-new user has no preferences) → completed category/topic selection →
real Home Screen → confirmed the empty state (a fresh account has no generated briefing) →
sign-out → sign back in → correctly routed straight to `/` this time, not back through onboarding,
confirming the saved preferences correctly gate `redirectAfterAuth`'s routing decision across a
real session boundary, not just in isolated testing. The backend-down/retry path was not
re-verified within this same session — M33's isolated verification of that exact mechanism was
judged sufficient. **Part 3 (Mobile App, Milestones 24-34) is now fully complete.**

Milestone 33 (Empty, Error, and Loading States) closed out earlier the same day — see its
write-up below for the full state-by-state verification.)

Milestone 31 (Supporting News Cards) and Milestone 30's deferral both closed out 2026-08-24; see
their write-ups below.)
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
**`docs/08-personalization-pivot-plan.md`** (verified FRED series IDs, database schema, service
architecture, mobile changes, and a full milestone breakdown) and reflected in `docs/01`, `docs/02`,
and `docs/03`. **Implementation of this pivot is well underway**: Milestones 13 through 18 are
complete — user accounts and Clerk auth, category/topic selection, the FRED and Marketaux fetch
services, a full fetch-filter-persist-cleanup pipeline that turns those services' output into real
rows in `daily_data_items`/`daily_data_news`, and (as of this update) per-user OpenAI briefing
generation — a user's category/topics get resolved into relevant FRED/FMP data, formatted into a
prompt, and sent to `gpt-5-nano` to produce a structured `BriefingContent` (headline + themed
sections), persisted one row per user per day in the new `user_briefings` table. Verified
end-to-end against the live OpenAI API (not just type-checked), including the quiet-day fallback
path (no relevant data → no API call, just a static message) and the per-user loop's
skip-if-exists behavior. **Milestone 19 (Daily Briefing Orchestrator) is complete** —
`briefing_service.py`'s `run_daily_briefing_job` wires M15-18 together (fetch/filter/persist raw
data → per-user generation loop → 48-hour cleanup) and writes one `job_runs` row per run; its live
end-to-end run on 2026-08-11 also finally confirmed M17's gainer/loser coverage, blocked twice
earlier in the week by FMP's rate limit. **Milestone 20 (Personalized Briefing API) is also
complete** — `GET /v1/users/me/briefing` serves a signed-in user's own `user_briefings` row for
today, replacing the old single-briefing `GET /briefings/today` design, with a friendly fallback
message (not an error) when no briefing has been generated yet. Verified live: the route is
correctly registered and Clerk-protected (confirmed `403`, not `404`, when unauthenticated), and
both branches of its actual logic — a real found briefing, and the not-yet-generated fallback —
were tested directly against real data, not just type-checked. **Milestone 21 (Personalized
Notifications) is complete for its backend scope** — `POST /v1/notifications/register` links a
device's Expo push token to the signed-in user, and `notification_service.py`'s
`send_daily_notifications` finds everyone with a real (non-quiet-day) briefing for a given day,
skips weekends entirely, and sends each active device a push notification via Expo's real API
concurrently, deactivating any token Expo reports as no longer registered. Deliberately scoped to
backend only — the mobile side (requesting notification permission, obtaining the Expo push token,
calling the new registration endpoint) is real work but belongs to the Mobile App phase
(Milestones 27-40), not this one, and there's no way to test "does a real device actually receive
this" without it existing yet. **Milestone 22 (Backend Integration Test Pass) is complete** —
`backend/scripts/integration_check.py`, a real reusable script (not a one-off, per the same
reasoning Milestone 11 used for building a permanent `pytest` suite instead of a throwaway check)
that runs the actual daily pipeline (`run_daily_briefing_job`) end to end, reads the result back
through the real API endpoint (`get_todays_briefing`, called directly rather than over HTTP, since
the script has no real Clerk session token), then exercises the notification send
(`send_daily_notifications`) against a throwaway test device token, reporting a clear PASS/FAIL per
stage rather than just "the script didn't crash." A Saturday run confirmed Steps 1-2 cleanly and
confirmed the weekend-skip design was working as intended, not broken. The one remaining
check — real weekday notification deactivation — was finally confirmed live on 2026-08-17, not by
re-running the script itself but through M23's own new admin endpoints (see below), closing M22 out
for real. **Milestone 23 (Scheduled Personalization Job) is complete for its current scope** — per
`docs/03`'s M23 scope, the goal is automating the daily pipeline so it runs without manual
intervention. Deliberately scoped to build-and-verify only, since the backend has no live
deployment yet to point a real cron schedule at: `verify_admin_secret` (constant-time admin-secret
auth) and both `POST /v1/admin/trigger-briefing`/`POST /v1/admin/trigger-notifications` routes are
built, wired, and now verified against a real running server over real HTTP — a real
`X-Admin-Secret` header, a real pipeline run, and a real confirmed device-token deactivation, not
just a local test client. Live hosted-cron scheduling itself is still deferred to Milestone 42 —
see the write-up below, including a real stale-date bug (the trigger date was being computed once
at import time instead of per request) caught and fixed along the way. **Milestone 24 (Mobile API
Client) is complete** — `mobile/lib/apiClient.ts` provides one shared `apiFetch` (optional Clerk
`getToken`, request timeout, normalized `ApiError` on any failure), wired into `useHealthCheck.ts`
and the onboarding screens' preference calls, replacing their ad hoc `fetch` logic. Verified
end-to-end on a physical device: real sign-up, real Clerk-authenticated requests reaching
`/v1/users/me/preferences`, and both onboarding screens saving/loading correctly. That pass also
surfaced a real, unrelated bug in `redirectAfterAuth.ts` — see Known Issues. **Milestone 25
(Frontend Response Schemas) is also complete** — `zod` installed, `UserBriefingResponseSchema` and
`UserPreferencesSchema` added under `mobile/schemas/`, both verified against real backend-serialized
data (not hand-typed fixtures) for every real branch, and malformed-input rejection explicitly
confirmed. The preferences schema is wired into both onboarding screens' real `apiFetch` calls; the
briefing schema is verified but deliberately not wired to a consumer yet, since none exists until
M26's `useTodayBriefing` hook. **Milestone 26 (TanStack Query Hooks) is complete** —
`useTodayBriefing` wraps `apiFetch`/`UserBriefingResponseSchema` in a `useQuery`, gated on Clerk
being ready, giving that schema its first real consumer. Verified live on a physical device via a
temporary debug block on the home screen. **Milestone 27 (Walris Theme Tokens) is complete** —
typography tokens and spacing/radius Tailwind extensions are built, font loading is wired, and both
were confirmed live on a physical device 2026-08-21. **Milestone 28 (App Layout Shell) is also
complete** — a shared `Screen` component now handles safe areas, optional scrolling, and page
margins for every screen, migrated off each screen's own inconsistent ad hoc handling, verified
live via a full fresh onboarding run. **Milestone 29 (Daily Briefing Header) is also complete** —
`DailyBriefingHeader` renders the app name, a time-of-day greeting, and today's date, wired into
`app/index.tsx`, confirmed correct live on a physical device. See the write-ups below for the real
bugs review caught in all of these milestones before they shipped.

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
- [x] **Milestone 12 — FMP Market Data Service** (redesigned from the roadmap's original Finnhub
  scope — see the pivot story below; formal sign-off closed out 2026-08-09, long after the code
  itself was done)
- [x] **Milestone 13 — User Accounts & Clerk Integration**
- [x] **Milestone 14 — Category & Topic Selection** (core flow complete and device-verified; two
  small pieces still outstanding — see notes below)
- [x] **Milestone 15 — FRED Service**
- [x] **Milestone 16 — Marketaux Service**
- [x] **Milestone 17 — Daily Data Pipeline & Storage**
- [x] **Milestone 18 — Per-User OpenAI Briefing Generation**
- [x] **Milestone 19 — Daily Briefing Orchestrator** (live end-to-end verification passed
  2026-08-11 — see notes below)
- [x] **Milestone 20 — Personalized Briefing API** (`GET /v1/users/me/briefing`, verified live
  2026-08-11 — see notes below)
- [x] **Milestone 21 — Personalized Notifications** (backend scope complete and verified live
  2026-08-14 — mobile registration UI deferred to Milestones 27-40 — see notes below)
- [x] **Milestone 22 — Backend Integration Test Pass** (weekend behavior confirmed 2026-08-15;
  real weekday notification deactivation confirmed live 2026-08-17 — see notes below)
- [x] **Milestone 23 — Scheduled Personalization Job** (admin auth and both trigger endpoints
  built and verified live over real HTTP, 2026-08-17; live hosted-cron wiring itself deferred to
  Milestone 42, once there's a real deployment to point one at — see notes below)
- [x] **Milestone 24 — Mobile API Client** (`apiClient.ts` built, wired into `useHealthCheck.ts`
  and onboarding screens, verified end-to-end on a physical device 2026-08-20 — see notes below)
- [x] **Milestone 25 — Frontend Response Schemas** (`zod` added, both schemas verified against real
  backend data and malformed-input rejection, preferences schema wired into both onboarding
  screens; briefing schema deliberately left unwired until M26 — see notes below)
- [x] **Milestone 26 — TanStack Query Hooks** (`useTodayBriefing` built, wired to
  `UserBriefingResponseSchema`, verified live on a physical device — see notes below)
- [x] **Milestone 27 — Walris Theme Tokens** (typography tokens, tailwind spacing/radius
  extension, and font loading all built and verified live on a physical device 2026-08-21 — see
  notes below)
- [x] **Milestone 28 — App Layout Shell** (shared `Screen` component built, migrated onto all
  three existing screens, verified live on a physical device 2026-08-21 — see notes below)
- [x] **Milestone 29 — Daily Briefing Header** (`DailyBriefingHeader` built and wired into
  `app/index.tsx`, verified live on a physical device 2026-08-21 — see notes below)
- [x] *(not a numbered milestone)* **Backend indicator-data extension** — resolved Milestone 30's
  real blocker; `GET /v1/users/me/briefing` now returns structured `indicators` data, verified
  end-to-end 2026-08-24 — see notes below
- [~] **Milestone 30 — Key Indicator Chart Component** (deferred 2026-08-24, not part of V1 —
  see notes below)
- [x] **Milestone 31 — Supporting News Cards** (`NewsCard` built and verified live on a physical
  device, including real tap-to-open — see notes below)
- [x] **Milestone 32 — Home Screen** (real screen assembled, debug scaffolding removed, sign-out
  added, verified live on a physical device across every path — see notes below)
- [x] **Milestone 33 — Empty, Error, and Loading States** (all three components built, wired into
  `TodayBriefing`, verified live on a physical device across all four states — see notes below)
- [x] **Milestone 34 — Mobile Integration Test Pass** (iOS-only, Android tracked as a follow-up —
  full flow confirmed as one continuous journey on a physical device — see notes below)
- [ ] Milestones 35–50 — Notifications, QA, Deployment & Launch (Part 4)

## Current Milestone

**Milestones 12 through 23 are all complete — Part 2 (Core Backend) is fully closed out.** Per
`docs/03`, that's the entire personalization pivot's backend build: accounts and auth, category/
topic selection, the FRED/FMP/Marketaux fetch services, the fetch-filter-persist-cleanup pipeline,
per-user OpenAI generation, the daily orchestrator, the personalized briefing API, personalized
notifications (backend scope), a full integration test pass, and the admin-triggered automation
surface M23 needed. See the M22/M23 write-ups below for exactly how both closed on 2026-08-17, in
one combined live run rather than two separate ones.

**Milestones 24 through 29 — the start of Part 3 (Mobile App, M24–34) — are all complete.** M24
built the shared `apiClient.ts` fetch wrapper (per `docs/02` §13/§14, `docs/08` §3/§10) and verified
it end-to-end on a physical device. M25 added Zod schemas for the briefing and preferences
responses, verified against real backend data. M26 built `useTodayBriefing`, wiring the briefing
schema into a real `useQuery` consumer for the first time and verifying it live on a physical
device. M27 built typography tokens, Tailwind spacing/radius extensions, and font loading. M28
built the shared `Screen` layout component and migrated every screen onto it. M29 built
`DailyBriefingHeader` (app name, time-of-day greeting, date) and wired it into the home screen. All
confirmed live on a physical device 2026-08-21. See the write-ups below for what got built and the
real bugs review caught in each before they shipped. **The backend indicator-data extension
(2026-08-24) resolved M30's real blocker** — `GET /v1/users/me/briefing` now returns structured
`indicators` data, not just prose; see that write-up below. **Milestone 30 (Key Indicator Chart
Component) itself is deferred, not part of V1** — decided after scoping it out: most indicators
only have 1-2 data points right now, so a chart showing the same near-static picture every day a
user opens the app doesn't earn its place yet. Revisit once real history accumulates. `docs/03`'s
M32 (Home Screen) no longer assembles a chart. **Milestone 31 (Supporting News Cards) is
complete** — `NewsCard` renders real, deduplicated, recent articles, confirmed live on a physical
device including real tap-to-open behavior. **Milestone 32 (Home Screen) is also complete** — the
real screen is assembled (`BriefingNarrative`, `NewsCard`s, signed-in/out branching, pull-to-refresh,
sign-out, all debug scaffolding removed) and confirmed live on a physical device across every path.
See its write-up and Known Issues (for `redirectAfterAuth`'s resolved race) below. **Milestone 33
(Empty, Error, and Loading States) is also complete** — `LoadingState`/`ErrorState`/`EmptyState`
built, wired into `TodayBriefing`, and confirmed live on a physical device across all four
reachable states, including retry actually recovering after a real backend outage. **Milestone 34
(Mobile Integration Test Pass) is also complete, iOS-only** (Android tracked as a real follow-up —
see Known Issues) — the full flow confirmed as one continuous journey on a genuinely new account:
sign-up → onboarding → real Home Screen → sign-out → sign back in → correctly routed straight to
`/`, not back through onboarding. **Part 3 (Mobile App, Milestones 24-34) is now fully complete.**

**Milestone 14's core flow is verified end-to-end on a real device** — sign-up → `/category` →
`/topics` → `/` all confirmed working against the live database. Two smaller pieces of M14 are
still outstanding (name field, settings screen — see M14 notes below), but the flow itself is no
longer blocked. The personalization pivot is fully planned in
`docs/08-personalization-pivot-plan.md`.

### Milestone 34 — Mobile Integration Test Pass (complete, 2026-09-02, iOS-only)

Per `docs/03`'s M34 scope: end-to-end verification of the full personalized flow — sign-in →
onboarding → Home Screen → real backend data — run as one continuous journey rather than the
piece-by-piece verification M24-M33 each already did individually.

**Scope decision:** `docs/03`'s original text calls for "both iOS and Android," but this project
has never had Android tooling — no Android Studio, no emulator, no physical Android device.
Scoped M34 to iOS-only rather than block on setting up an entire second platform's tooling;
Android is now a tracked, explicit follow-up in Known Issues, not a silently dropped requirement.

**What this milestone actually added:** every prior mobile milestone verified its own piece in
isolation — auth methods individually (M24, and the `redirectAfterAuth` fixes), the Home Screen's
states individually (M33), sign-out on its own (M32). What hadn't been confirmed was all of it
working *together*, across a real session boundary, on a genuinely fresh account — not the same
reused test user whose preferences had been manually reset via direct database writes several
times throughout this project's testing.

**Test run, on a physical iPhone:**

1. Signed out of the existing account.
2. Signed up with a brand-new email.
3. Confirmed `redirectAfterAuth` correctly routed the new account to `/category` (no preferences
   exist yet for a brand-new user).
4. Completed category and topic selection; landed on the real Home Screen.
5. Confirmed the empty state rendered (a fresh account genuinely has no generated briefing) —
   the same `EmptyState` component M33 built and verified, now proven correct for a real new user
   rather than the manually-reset existing one.
6. Signed out, then signed back in with the same new account.
7. Confirmed `redirectAfterAuth` this time routed straight to `/` — not back through onboarding —
   correctly reading the preferences saved in step 4 back out on a genuinely separate sign-in,
   proving the round trip works across a real session boundary, not just within one continuous
   render.

**Deliberately not re-verified:** the backend-down/retry mechanism, since M33 already proved that
exact mechanism works in isolation, and re-running it within this same session was judged
unnecessary rather than an oversight.

**Part 3 (Mobile App, Milestones 24-34) is now fully complete.**

### Milestone 33 — Empty, Error, and Loading States (complete, 2026-08-25–2026-09-02)

Per `docs/03`'s M33 scope: replace `TodayBriefing`'s placeholder loading/error handling
(`<Text>Loading...</Text>`, a raw `<Text>{error.message}</Text>` dump) with real, designed states
per `docs/04` §10.9 (Empty State) and §10.10 (Error State), plus a consistent, reusable retry
mechanism.

**Real distinction found while scoping:** both of the backend's fallback paths (`briefings.py`'s
"no briefing generated yet," and `prompt_services.py`'s `build_quiet_day_briefing` for a genuinely
quiet day) always produce `content.sections: []`; a real generated briefing never does. That makes
`content.sections.length === 0` a reliable way to detect "empty," instead of rendering the fallback
headline as if it were real narrative content — which is what the app did before this milestone.

**What got built:**

- `mobile/components/ui/loading-state.tsx` — `LoadingState`: an `ActivityIndicator` with an
  optional `message` prop. `docs/04` has no dedicated spec for loading states beyond its QA
  checklist asking that they exist, so this is a reasonable default rather than a strict
  requirement.
- `mobile/components/ui/error-state.tsx` — `ErrorState`: `docs/04` §10.10's exact example copy as
  defaults ("We couldn't load today's briefing." / "Please try again."), both overridable via
  props, with a required `onRetry` prop wired to the existing `Button` component — this is the
  "consistent way to retry" the milestone calls for; any future screen can reuse it instead of
  inventing its own retry UI.
- `mobile/components/ui/empty-state.tsx` — `EmptyState`: `docs/04` §10.9's tone and example copy
  ("Today's briefing is not available yet." / "Check back shortly."), title/description both
  prop-driven.
- `app/index.tsx`'s `TodayBriefing` updated to use all three: `LoadingState` for `isPending`,
  `ErrorState` (`onRetry={refetch}`, pulled from `TodayBriefing`'s own `useTodayBriefing()` call —
  free, since TanStack Query shares the cached call rather than firing a second request) for
  `isError`, and `EmptyState` when `content.sections.length === 0`, falling through to the real
  `BriefingNarrative`/`NewsCard`s otherwise.

**Scope boundary (deliberate, not an oversight):** the onboarding screens
(`category.tsx`/`topics.tsx`) keep their own ad hoc `setErrorMessage` + inline `<Text>` error
handling — different concern (form validation, not network retry) — not retrofitted onto these new
components as part of this milestone.

**Bugs caught and fixed during review, before any of this shipped:**

- `EmptyState`'s title originally used `typography.headlineSm` (Libre Caslon Text, bold) —
  directly contradicting §10.9's "calm, helpful, non-alarming" tone, since that exact weight is
  used everywhere else in the app (`DailyBriefingHeader`, `BriefingNarrative`) specifically to
  signal real, important content. Switched to `bodyLg`/`bodyMd` (Inter) for both title and
  description.
- An unused `StyleSheet` import in `empty-state.tsx` (never used anywhere in the file).
- An unused `error` variable left dangling in `app/index.tsx` after switching from the raw
  `{error.message}` text to `<ErrorState>` (which intentionally shows fixed, calm copy rather than
  the technical error — `docs/04`'s tone calls for "clear, honest, recoverable," not a raw
  exception message surfaced to the user).
- A "Lodaing your briefing..." typo in the `LoadingState` message.

**Verification (2026-09-02):** confirmed live on a physical device across all four reachable
states. Loading: real spinner observed on load. Empty: today (2026-09-02) genuinely has no
generated briefing, so this was the app's actual real-world state — matched `docs/04`'s exact
copy. Real briefing: temporarily pointed the router's `today` at 2026-08-17 (a date with an actual
generated briefing), confirmed `BriefingNarrative`/`NewsCard`s render correctly, then reverted
cleanly (confirmed via `git diff` showing no changes). Error + retry: stopped the backend entirely,
confirmed `ErrorState` rendered with a working "Try Again" button, restarted the backend, and
confirmed tapping retry actually recovered — correctly falling back to the empty state again,
since today still has no real briefing.

### Milestone 32 — Home Screen (complete, 2026-08-24–25)

Per `docs/03`'s M32 scope: replace `app/index.tsx`'s M10-M31 verification scaffolding with the
actual Home Screen.

**What got built:**

- `mobile/components/ui/screen.tsx`: `Screen` extended with an optional `refreshControl` prop
  (`ReactElement<RefreshControlProps>`), forwarded to its internal `ScrollView` — the only way
  React Native supports pull-to-refresh, and `Screen` had no way to pass one through before.
- `mobile/schemas/briefings.ts`: `BriefingSectionSchema`/`BriefingContentSchema` pulled out as
  their own named schemas (mirroring the backend's `BriefingSection`/`BriefingContent` Pydantic
  classes) — the narrative's shape used to be the only one left anonymous/inline, unlike
  `IndicatorSeriesSchema`/`NewsItemSchema`. `export type BriefingContent` added for component props.
- `mobile/components/ui/briefing-narrative.tsx`: `BriefingNarrative` — renders the real headline
  (`headlineMd`) and each section (`headlineSm` + `bodyMd`) for the first time; previously only a
  headline string and a section count were ever shown anywhere.
- `app/index.tsx` fully rewritten: `HealthProfile`/`BriefingDebug`/`TypographyDebug` removed
  entirely (confirmed via grep — no leftover references to `useHealthCheck`, `BriefingDebug`, or
  `TypographyDebug`). Replaced with `SignInPrompt` (renders when `isLoaded && !isSignedIn`) and
  `TodayBriefing` (renders when `isLoaded && isSignedIn`), using `useAuth()` — fixing a real gap
  found while scoping this milestone: previously *every* visitor, signed in or not, saw the same
  block including sign-in/sign-up links, with no auth branching anywhere. Pull-to-refresh wired via
  `RefreshControl`, tied to `useTodayBriefing`'s `refetch`/`isRefetching`.

**Newly discovered gap, not part of M32's original scope, added anyway:** there was no sign-out
mechanism anywhere in the app — confirmed via grep, zero `signOut()` calls existed. A real hole:
once signed in, a user had no way to sign out at all. Added `SignOut` (`mobile/app/index.tsx`),
using Clerk's `useAuth().signOut()` directly — no new dependency needed — rendered alongside
`TodayBriefing` when `isLoaded && isSignedIn`, until a real settings screen exists (still the open
M14 loose end) to move it to. One cleanup caught during review: `Pressable` was imported from
`react-native` on its own separate line instead of being added to the existing `RefreshControl,
View` import — consolidated.

**Verification:** on-device re-verification was initially blocked by `redirectAfterAuth`'s
race condition recurring (see Known Issues for the full story) — once that was actually fixed
2026-08-25, a clean pass confirmed every path: signed-in real briefing content
(`BriefingNarrative` + `NewsCard`s), the signed-out `SignInPrompt`, pull-to-refresh actually
triggering a refetch, and sign-out actually signing the user out.

### Milestone 31 — Supporting News Cards (complete, 2026-08-24)

Per `docs/03`'s M31 scope: expose real Marketaux articles alongside the narrative — same
data-availability gap M25 flagged for news as it did for indicators (`DailyDataNews` existed in
the database, linked to `DailyDataItem` via `item_id`, but was never exposed through any API
endpoint).

**Scope decision:** tested against a real date with actual fetched data (2026-08-17) — one user's
relevant news came back as 125 rows, 96 unique URLs. "Supporting" cards, not a full feed — capped
at 5, deduplicated by `url`, sorted by `published_at` descending (most recent first).

**What got built (backend):**

- `backend/app/schemas/user_briefing.py`: new `NewsItem` schema (`headline`, `source`, `summary`,
  `published_at: datetime`, `url`, `sentiment: float | None`), matching `docs/04` §10.7's required
  fields except "topic" (no such field exists on `DailyDataNews`; `sentiment` is the only tag data
  available). `UserBriefingResponse` extended with `news: list[NewsItem]`.
- `backend/app/routers/briefings.py`: reused the existing `get_user_daily_data_with_news(user,
  as_of)` — the same function that already combines relevant FRED + FMP items with linked news for
  the AI prompt — called read-only, not modified (avoiding M30's mistake of editing a live-pipeline
  function in place). Flattens all items' `.news` tuples into one list, dedupes by `url`, sorts by
  `published_at` descending, takes the first 5, then maps each real `DailyDataNews` row into a
  `NewsItem`.

**Bugs caught and fixed during review, before any of this shipped:**

- The flatten/dedupe/sort/cap logic itself was correct on the first pass (verified: exactly 5
  items from a real 96-unique-URL test case, properly sorted newest-first) — but the raw
  `DailyDataNews` ORM objects were passed directly as `news=` where `list[NewsItem]` was expected.
  Notably, **mypy did not catch this one** (`mypy` passed clean) — its type inference through the
  `{n.url: n for n in all_news}.values()` → `sorted(...)` chain apparently lost precision somewhere
  along the way. A real end-to-end test against live data caught it instead: a genuine
  `pydantic.ValidationError` ("Input should be a valid dictionary or instance of NewsItem",
  ×5). Fixed with an explicit `NewsItem(...)` mapping step per row. Worth remembering: mypy passing
  is not sufficient proof of correctness for Pydantic model construction through several chained
  built-ins — real-data verification still matters even when the type checker is silent.

**What got built (mobile):**

- `mobile/schemas/briefings.ts`: `NewsItemSchema` mirroring the backend field-for-field, plus an
  exported `NewsItem` inferred type (`z.infer<typeof NewsItemSchema>`) — `UserBriefingResponseSchema`
  extended with `news`.
- `mobile/components/ui/news-card.tsx`: `NewsCard`, per `docs/04` §10.7's style — 12px radius
  (`rounded-md`, M27's radius token), subtle border, headline in `headlineSm` (Libre Caslon Text),
  summary in `bodyMd` (Inter), source + a formatted timestamp in `dataLabel` (JetBrains Mono via
  `Intl.DateTimeFormat`, e.g. "Aug 17, 1:11 PM"). Tapping opens the real article via
  `Linking.openURL`.
- **Product decision:** the sentiment tag was dropped from the card entirely, not deferred as a
  bug — Marketaux only provides a raw numeric score (e.g. `0.756567`), not a friendly label, and it
  wasn't judged worth building a score→label mapping for V1. Revisit in a later version if wanted.
  `published_at` fills that slot on the card instead, satisfying `docs/04`'s "published time"
  requirement that the first draft had missed entirely.
- Wired into `app/index.tsx`'s `BriefingDebug` for on-device verification, alongside a fix to give
  the whole debug screen (`Screen scroll`) room to actually scroll through everything now stacked
  on it (typography tokens, indicators, and up to 5 news cards).

**Additional bugs caught and fixed during review (mobile side):**

- The initial `NewsCardProps` type was written as `item: <NewsItemSchema></NewsItemSchema>` —
  JSX tag syntax used where a TypeScript type was needed, not valid syntax at all. Fixed by adding
  the missing `export type NewsItem = z.infer<typeof NewsItemSchema>` to the schema file and using
  it properly (`item: NewsItem`).
- `sentiment: z.string()` in the Zod schema — wrong type entirely (backend is `float | None`);
  failed on both a real numeric value and the common real `null` case, confirmed directly.
- `z.string().url()` — deprecated Zod v4 API; replaced with the top-level `z.url()`.

**Verification:** confirmed live on a physical device against real data — temporarily pointed the
router's `today` at 2026-08-17 (a date with actual fetched articles) to force real cards to render,
confirmed 5 correctly deduplicated cards with readable formatted timestamps, confirmed tapping a
card actually opened its real article URL, then reverted the temporary date override.

### Backend: Briefing Endpoint Indicator Data Extension (complete, 2026-08-24)

Not a numbered milestone — a backend prerequisite discovered while scoping Milestone 30 (Key
Indicator Chart Component). `GET /v1/users/me/briefing` only ever returned `date` + `content`
(headline + prose sections) — no structured indicator values anywhere, even though the real
numbers exist in the database (`DailyDataItem`, populated daily from FRED). A chart needs real
numbers, not prose, so this had to be resolved before M30 could start.

**What got built:**

- `backend/app/services/daily_data_service.py`: `STALE_DATA_HOURS` raised from `48` to `400 * 24`
  (~400 days). `DailyDataItem` rows were being deleted after 48 hours, so no historical trend data
  could ever accumulate — confirmed via the daily pipeline's own cleanup step
  (`delete_stale_daily_data`). Storage cost is trivial: only 39 fixed FRED series exist across
  every category/topic combination, so even a full year of daily snapshots is ~20k rows.
  `DailyDataNews` cascades off `DailyDataItem` via `ON DELETE CASCADE`, so it now retains for the
  same window automatically, no separate change needed. **No backfill possible** — data already
  deleted under the old 48-hour window is gone; real history starts accumulating from 2026-08-24.
- `backend/app/schemas/user_briefing.py`: new `IndicatorPoint` (`date`, `value`) and
  `IndicatorSeries` (`item_key`, `label`, `points`) schemas; `UserBriefingResponse` extended with
  `indicators: list[IndicatorSeries]`.
- `backend/app/routers/briefings.py`: `get_todays_briefing` now queries `DailyDataItem` filtered by
  `get_relevant_fred_item_keys(user)` (the same relevance function that already decides what feeds
  the AI narrative — the chart matches the story instead of drifting from it), groups by
  `item_key`, and looks up each series' human-readable label from `fred_service.py`'s existing
  `FRED_INDICATORS` list (no new label mapping needed — it already had real names for all 39
  series).
- `mobile/schemas/briefings.ts`: `IndicatorPointSchema`/`IndicatorSeriesSchema` added, mirroring
  the backend field-for-field, and `UserBriefingResponseSchema` extended with `indicators`.

**Bugs caught and fixed during review, before any of this shipped** (several rounds, since this
went through more iteration than most changes):

- An edit to `openai_service.py`'s existing `get_relevant_fred_items_for_day` (a *different*,
  pre-existing function used by the live M18/M19 daily-briefing pipeline — scoped to one day, for
  the AI prompt) stacked a new, broken implementation on top instead of writing new code elsewhere.
  The new block had `list(items = session.scalars(...).all())` — invalid keyword argument to
  `list()`, confirmed via a direct `TypeError`. Since this function feeds the live pipeline, this
  would have broken generating *any* user's daily briefing, not just the new chart feature. Also
  silently dropped that function's `source == "fred"` and `date == as_of` filters. Fully reverted
  to the original working version; the new multi-day, no-date-filter query was written fresh
  in `briefings.py` instead, where it belongs.
- `UserBriefingResponse` was defined **twice** in `user_briefing.py` (mypy: `no-redef`) — the
  second silently shadowed the first, which was missing the new `indicators` field. Merged into one
  definition.
- `briefings.py`'s `.all()` was chained onto the `select(...)` statement itself — `Select` objects
  don't have that method (confirmed: `AttributeError: 'Select' object has no attribute 'all'`).
  Needed to be on the result of `db.scalars(...)` instead.
- The raw `DailyDataItem` query result was passed directly as `indicators=items` — wrong shape
  entirely (`DailyDataItem` has no `label`/`points` fields). The actual grouping-into-`IndicatorSeries`
  step had to be written.
- `labels = dict[FRED_INDICATORS]` used type-subscript syntax (square brackets) instead of calling
  the `dict` constructor (`dict(FRED_INDICATORS)`) — produced a `types.GenericAlias`, not a real
  dict; confirmed via `TypeError` on `.get()`.
- `IndicatorSeries(item, label=..., points=...)` passed a positional argument to a Pydantic model
  (which only accepts keyword arguments) — confirmed via `TypeError`. `item` was also a stale
  leftover variable from an earlier, already-finished loop, not the intended `key`.
- The "no briefing yet" fallback branch was initially left without `indicators=` entirely, meaning
  any freshly-onboarded user would still 500 even after the "found" branch was fixed.

**Verification:** confirmed end-to-end against real data — `get_todays_briefing` called directly
against the real database returned 32 real indicators with correct labels/values; the same JSON,
run through the mobile Zod schema, parsed successfully; and on a physical device, `BriefingDebug`
rendered real indicator labels and values pulled all the way through the real stack.

### Milestone 29 — Daily Briefing Header (complete, 2026-08-21)

Per `docs/03`'s M29 scope: an identity header (app name, date, greeting) every future
screen-content milestone sits under — `docs/04` §10.2 describes a richer header including the
briefing title/summary/generated-timestamp, but that content is deliberately deferred to
Milestone 32's Home Screen; this milestone stays scoped to identity only, as the roadmap intended.

**Scope decision:** the greeting is a generic time-of-day greeting, not personalized with the
user's name. `User.name` exists as a DB column, but nothing in the app sets it yet — the
still-open Milestone 14 loose end — and there's no API endpoint exposing it either. Building a
name-based greeting now would mean faking data; deferred until M14's name field actually exists.

**What got built:**

- `mobile/components/ui/daily-briefing-header.tsx` — `DailyBriefingHeader`:
  - App name ("Walris") styled with M27's `headlineMd` token (Libre Caslon Text).
  - A time-of-day greeting computed from the device's local hour (`< 12` morning, `< 18`
    afternoon, else evening).
  - Today's date via the built-in `Intl.DateTimeFormat` — no new date-library dependency needed.
- Wired into `app/index.tsx`, rendered first inside `Screen`, above the temporary debug blocks.

**Bugs caught and fixed during review, before any of this shipped:**

- The component was named `HomeHeader` instead of the spec'd `DailyBriefingHeader` (also the
  filename's own name) — renamed.
- A typo in the afternoon greeting: `'Good Afternon!'` instead of `'Good Afternoon!'`.

**Verification:** confirmed live on a physical device — correct date, and the greeting boundary
checked directly: 17:46 (5:46pm) correctly read "Good Afternoon," confirming the `< 18` cutoff
behaves as intended (evening starts at 6pm, kept as-is per user preference).

### Milestone 28 — App Layout Shell (complete, 2026-08-21)

Per `docs/03`'s M28 scope: give every screen one shared layout wrapper instead of each handling
safe areas, scrolling, and page margins independently. Checked the real code before writing this
milestone's plan: `index.tsx` wrapped in `SafeAreaView` with no margin at all, while
`category.tsx`/`topics.tsx` wrapped in `ScrollView` directly with no `SafeAreaView` and no margin
either — a real, current inconsistency, not a hypothetical future one.

**What got built:**

- `mobile/components/ui/screen.tsx` — a `Screen` component: `SafeAreaView` wrapping an optional
  `ScrollView` (via a `scroll?: boolean` prop, kept per-screen since `index.tsx` doesn't scroll but
  the onboarding screens do) and a `px-md` horizontal margin, using M27's `md` spacing token
  (16px), matching `docs/04` §7.1's mobile margin spec exactly.
- Migrated `index.tsx`, `category.tsx`, and `topics.tsx` onto it, removing their own ad hoc
  `SafeAreaView`/`ScrollView` usage.

**Bugs caught and fixed during review, before any of this shipped:**

- `topics.tsx`'s three early-return states — `isLoading`, `fetchError`, and
  `savedPreferences === null` — were returning bare `<Text>` entirely outside `<Screen>`, bypassing
  safe-area handling and margin for exactly the states a user sees first when opening the screen.
  `category.tsx` didn't have this problem since its error state renders inline inside `<Screen>`.
  Fixed by wrapping all three in `<Screen>`.
- Leftover unused `ScrollView` imports in both `category.tsx` and `topics.tsx`, left over from
  before the migration since `Screen` now owns `ScrollView` internally.

**Verification:** confirmed live on a physical device via a full fresh onboarding run — the test
user's `category`/`additional_topics` were reset to `null`/`[]` directly in the database to force
the entire sign-up → category → topics flow, including `topics.tsx`'s loading state (the one just
fixed to render inside `Screen`). Safe area, scroll behavior, and consistent margins all confirmed
correct across all three screens.

### Milestone 27 — Walris Theme Tokens (complete, 2026-08-20–21)

Per `docs/03`'s M27 scope: make `docs/04-design-system.md`'s approved typography, spacing, and
shape system real, usable tokens — checked first and found colors were already done (verified by
converting `global.css`'s HSL values back to `docs/04`'s hex, e.g. `--background: 231 100%
98.6%` = exactly `#f8f9ff`), seeded correctly back in Milestone 4. User decision 2026-08-20: leave
colors where they are rather than consolidating into a `mobile/theme/` folder, since that would
duplicate what NativeWind's CSS-variable model already provides correctly.

**What got built:**

- `mobile/theme/typography.ts` — 8 type-scale tokens (`displayLg`, `displayLgMobile`, `headlineMd`,
  `headlineSm`, `bodyLg`, `bodyMd`, `caption`, `dataLabel`), each a plain `TextStyle` object
  bundling `fontFamily`/`fontSize`/`fontWeight`/`lineHeight`/`letterSpacing` — plain objects rather
  than Tailwind classes, since NativeWind's `text-*` utilities only cover `fontSize` and Walris's
  tokens are multi-property bundles.
- Real constraint found and resolved: `docs/04` §5.1 specifies `headline-md`/`headline-sm` at
  weight 600, but the actual `@expo-google-fonts/libre-caslon-text` package only ships 400
  (Regular) and 700 (Bold) — no 600/SemiBold file exists to load. User decided: load the 700 Bold
  file (closer to 600 than Regular) while keeping the token's `fontWeight` metadata at 600 to match
  `docs/04`'s declared intent.
- `tailwind.config.js` extended: a fixed `borderRadius` scale (`sm`/`DEFAULT`/`md`/`lg`/`xl`/`full`)
  per `docs/04` §8, replacing the old shadcn boilerplate that derived `lg`/`md`/`sm` from a single
  `--radius` CSS variable via `calc()` (now removed from `global.css` as dead code); and a `spacing`
  scale with named aliases (`xs` through `3xl`) per `docs/04` §6's 8px system, layered on top of
  Tailwind's existing numeric spacing (both resolve to the same pixel values).
- `app/_layout.tsx` — `useFonts()` loading the four actual font weights `typography.ts` references
  (`LibreCaslonText_700Bold`, `Inter_400Regular`, `Inter_500Medium`, `JetBrainsMono_500Medium`),
  gated behind `expo-splash-screen`'s `preventAutoHideAsync`/`hideAsync` so the app doesn't flash
  fallback system fonts before the real ones load.
- Dependencies installed via `npx expo install`: `expo-font`, `expo-splash-screen`,
  `@expo-google-fonts/libre-caslon-text`, `@expo-google-fonts/inter`,
  `@expo-google-fonts/jetbrains-mono`.
- A temporary `TypographyDebug` block added to `app/index.tsx` (alongside M26's `BriefingDebug`),
  rendering one line per token in its actual style, for on-device verification.

**Bugs caught and fixed during review, before any of this shipped:**

- The first draft of `typography.ts` had every token's `fontFamily` set to `'Inter'` regardless of
  which typeface `docs/04` actually specifies for it — the four Libre Caslon Text headline tokens
  were pointing at the wrong font family entirely.
- Several numeric values didn't match `docs/04` §5.1–5.3: `displayLg`/`displayLgMobile`/
  `headlineMd`/`headlineSm` all had wrong `fontSize`/`lineHeight`, `caption`'s `fontWeight` was 400
  instead of the spec's 500, and `dataLabel`'s `fontSize`/`lineHeight` were wrong. Several
  `letterSpacing` values were also off — `docs/04` specifies letter-spacing in `em`, which needed
  converting to px per token (e.g. `displayLg`: `-0.02em × 48px = -0.96`), not copied as a flat
  number across different font sizes.
- All `fontFamily` values were also generic placeholders (`'Inter'`) rather than the actual export
  names the `@expo-google-fonts/*` packages provide (`Inter_400Regular`, etc.) — without the exact
  weight-specific name, `useFonts()` has nothing valid to map the style to.

**On-device verification (2026-08-21):** confirmed on a physical device — all three typefaces
(Libre Caslon Text, Inter, JetBrains Mono) render correctly via the temporary `TypographyDebug`
block, and the new spacing/radius Tailwind classes render correctly too (checked via the sign-in/
sign-up screens' buttons, which use `rounded-lg`/`rounded-md`).

### Milestone 26 — TanStack Query Hooks (complete, 2026-08-20)

Per `docs/03`'s M26 scope: a single reusable hook for the signed-in user's personalized daily
briefing, giving M25's `UserBriefingResponseSchema` its first real consumer instead of leaving it
verified-but-unwired.

**What got built:**

- `mobile/hooks/useTodayBriefing.ts` — `useTodayBriefing()`:
  - Calls `useAuth()` internally for `getToken`/`isLoaded`/`isSignedIn`, so callers don't thread
    Clerk state through themselves.
  - Query function: `apiFetch('/v1/users/me/briefing', getToken)` → `await response.json()` →
    `UserBriefingResponseSchema.parse(...)` — a shape mismatch fails loudly through the query's
    `error` state.
  - `enabled: isLoaded && isSignedIn`, mirroring the guard `topics.tsx` already used, so it doesn't
    fire before Clerk's session is ready.
  - Stable query key `['briefing', 'today']` — no date parameter needed, since the endpoint always
    resolves "today" server-side from the signed-in user's session.
- A temporary debug block (`BriefingDebug`) added to `app/index.tsx`, rendering the hook's
  loading/error/data states directly on the home screen — explicitly marked in a comment for
  removal once Milestone 32 builds the real Home Screen.

**Bugs caught and fixed during review, before any of this shipped:**

- The hook was originally named `useBriefing` and `export default`ed, breaking both the milestone's
  own naming (`useTodayBriefing`) and the codebase's existing convention — every other hook
  (`useHealthCheck.ts`'s `useHealth`) uses a named export, not default. Renamed and switched to a
  named export.
- An unused `UserBriefingResponse` type import (only `UserBriefingResponseSchema` was actually
  used).

**Verification:** confirmed live on a physical device — a real signed-in request reached
`GET /v1/users/me/briefing` and correctly rendered the real no-briefing-yet fallback ("No briefing
available yet for today.", 0 sections), matching what this test user's actual database state
should produce (no `user_briefings` row for today's date, per the earlier M25 verification's real
data check). `isPending`/`isError`/`data` all behaved as expected; no request fired before Clerk
finished loading.

### Milestone 25 — Frontend Response Schemas (complete, 2026-08-20)

Per `docs/03`'s M25 scope: Zod schemas that parse and validate what the backend actually returns
from `GET /v1/users/me/briefing` and `GET`/`PUT /v1/users/me/preferences`, instead of trusting
`response.json()`'s `any` type. The original draft of this milestone described schemas for
structured indicator/news data that doesn't actually exist in the API response yet (see the
scope-correction note in `docs/03`'s M25 section) — that gap is documented there for a later
decision, not solved by this milestone.

**What got built:**

- `zod` added as a mobile dependency (wasn't installed before, despite being listed in the README's
  tech stack).
- `mobile/schemas/briefings.ts` — `UserBriefingResponseSchema`, matching the real
  `UserBriefingResponse` Pydantic schema (`date`, `content.headline`, `content.sections[].{heading,
  body}`).
- `mobile/schemas/preferences.ts` — `UserPreferencesSchema`, matching the real backend
  `UserPreferences` schema (`category: string | null`, `additional_topics: string[]`).
- Both wired into real call sites: `category.tsx` and `topics.tsx` now `.parse()` every
  `apiFetch` response through the schema before using it, instead of just TypeScript-asserting the
  shape.

**Verification — real data, not hand-typed fixtures:** rather than guessing at response shapes,
verification pulled real rows out of the database and serialized them through the backend's actual
Pydantic response classes (same technique `integration_check.py` used in M22 to sidestep needing a
real Clerk token) — a real persisted briefing, the real no-briefing-yet fallback (calling the actual
`get_todays_briefing` function for a date genuinely without a row), a real user's saved preferences,
and a constructed fresh-signup (`category: null`) case. All four parsed successfully. Four
deliberately malformed inputs (missing field, wrong type, bad date format, missing key) were also
confirmed to fail parsing cleanly, closing out that acceptance criterion explicitly.

**Bugs caught and fixed during review, before any of this shipped:**

- A `headling`/`heading` typo in the briefing schema — would have failed every real briefing parse,
  confirmed by testing against a real response before the fix.
- `additional_topics` typed as `z.string()` instead of `z.array(z.string())` — would have failed
  every real preferences parse, same real-response confirmation.
- Both onboarding screens initially passed the raw `Response` object into `.parse()` instead of its
  parsed JSON body (`await response.json()`) — would have failed on every successful request, not
  just malformed ones. Caught in `category.tsx` and `topics.tsx` separately; both fixed and
  reverified against a real `Response`-shaped object.
- Minor: a `no-redeclare` naming collision where the inferred TypeScript type reused the exact same
  name as its own Zod schema const in `preferences.ts`; renamed to `UserPreferences` (and
  `UserBrefingResponse` → `UserBriefingResponse`, fixing a missing-letter typo) for consistency.

**Deliberately not done:** `UserBriefingResponseSchema` isn't wired to any consumer yet — there's no
call site fetching `/v1/users/me/briefing` on the mobile side at all until M26's `useTodayBriefing`
hook exists. Wiring it in now would mean building a throwaway consumer just to prove it works.

### Milestone 24 — Mobile API Client (complete, 2026-08-20)

Per `docs/03`'s M24 scope: one shared, authenticated fetch wrapper for the mobile app instead of
each screen hand-rolling its own `fetch` call, with the one real addition the personalization pivot
requires — attaching the signed-in user's Clerk session token as an `Authorization: Bearer` header
on per-user requests.

**What got built:**

- `mobile/lib/apiClient.ts` — `apiFetch(path, getToken?, options?)`:
  - Reads `EXPO_PUBLIC_API_BASE_URL` once, at module scope, instead of every call site checking
    `process.env` itself.
  - `getToken` is optional, so one function serves both unauthenticated calls (`GET /health`) and
    authenticated per-user calls (`/v1/users/me/*`) — no second client needed. When provided, a
    missing/expired token throws before the request is even made.
  - A 10-second request timeout via `AbortController`.
  - Every failure — a non-OK response, an aborted/timed-out request, or a bare network failure —
    normalizes into one `ApiError` (with `.status`) instead of leaking whatever raw error type the
    failure happened to produce.
- Migrated the existing ad hoc fetch call sites onto it: `useHealthCheck.ts`, and both onboarding
  screens' preference calls (`category.tsx`'s submit, `topics.tsx`'s fetch-on-mount and submit).

**Bugs caught and fixed during review, before any of this shipped:**

- `topics.tsx`'s submit handler was missing the leading slash on `/v1/users/me/preferences` —
  would have produced a broken concatenated URL (`{base}v1/users/me/preferences`) against the real
  backend.
- An early version of `apiClient.ts`'s `catch` block caught everything unconditionally, including
  the `ApiError` thrown for a real failed response — a 404 or 500 would've been swallowed and
  relabeled as a generic timeout message, losing the real status/detail.
- `topics.tsx` had a `response.status === 401` check that could never fire, since `apiFetch` already
  throws before returning on any non-OK response — dead code masking what was actually unreachable.
- Cleanup: an unused `ApiError` import in all three migrated files, an unused `response` variable
  in `category.tsx`, redundant manual `getToken()`/null-checks now handled inside `apiFetch`
  itself, and a `'Put'` method-casing typo.

**End-to-end device verification (2026-08-20):** signed up for real on a physical device — a real
Clerk-authenticated request reached `/v1/users/me/preferences` and was accepted, and both onboarding
screens saved/loaded correctly against the real running backend. The timeout/network-failure paths
were separately confirmed via a script exercising `apiClient.ts` itself against the real local
backend (a genuinely unresponsive server, connection-refused, and a missing/invalid token all
normalized to `ApiError` correctly, including the real 10-second `AbortController` timeout).

That same device pass surfaced a real, unrelated bug: `redirectAfterAuth.ts` — called twice on
sign-up (once explicitly after `signUp.finalize()`, once via a `useEffect` watching `isSignedIn`) —
threw a false "session could not be verified" because `isSignedIn` can flip `true` slightly before
`getToken()` is actually able to return a token. Fixed with a bounded retry (3 attempts, 200ms
between them) rather than removing the `useEffect`, since that effect is also the only thing that
redirects an already-signed-in user who lands back on `/sign-in`/`/sign-up`. Confirmed resolved on
a physical device 2026-08-20 — **later found incomplete: the race recurred 2026-08-24 under worse
network conditions; see the current Known Issues entry for the full history and the actual
root-cause fix deferred to 2026-08-25.**

### Milestone 23 — Scheduled Personalization Job (complete for current scope, 2026-08-16–17)

Per `docs/03`'s M23 scope: automate the daily pipeline (M15–19) so it runs without manual
intervention. Scoped deliberately, before writing any code: the backend has no live deployment
yet, so an actual hosted-cron schedule can't be configured for real until there's a public URL to
point it at (Milestone 42, later in the roadmap). This pass builds and locally verifies the two
admin-triggered endpoints a future cron will call; wiring the real schedule is left for when the
backend is actually deployed.

**What got built:**
- `app/core/config.py` / `.env.example` — `admin_secret: str`, following the existing `Settings`
  pattern exactly. `ADMIN_SECRET` had been reserved in `.env.example` since Milestone 6 but never
  actually read; moved into the "read by Settings today" section now that it is.
- `app/core/auth.py` — `verify_admin_secret`, a new dependency alongside `get_current_user`. Pulls
  `X-Admin-Secret` off the request via FastAPI's `Header`, compares it against
  `settings.admin_secret` with `secrets.compare_digest` (constant-time, avoiding the timing
  side-channel a plain `==` would expose), and raises a uniform `401` whether the header is
  missing, empty, or simply wrong.
- `app/routers/admin.py` (new) — two routes, both guarded by `Depends(verify_admin_secret)`:
  `POST /v1/admin/trigger-briefing` calls `run_daily_briefing_job(date.today())`;
  `POST /v1/admin/trigger-notifications` calls `send_daily_notifications(date.today())`. Wired into
  `v1_router` in `app/routers/__init__.py`, the same way every other router is.

**A real scoping correction made along the way**: `integration_check.py` (M22) was briefly
considered as the thing a cron job could call directly, since it already runs the same two
functions. Rejected on inspection: it's scoped to one hardcoded test user, creates and deletes a
throwaway device token on every run, and — critically — would report `FAIL` every single weekend,
since its Step 3 assertion has no awareness that `send_daily_notifications` is designed to skip
weekends entirely. The admin endpoints call `run_daily_briefing_job`/`send_daily_notifications`
directly, with none of that test scaffolding; `integration_check.py` stays exactly what it already
is — a manual verification tool, not the production trigger.

**Real bugs found and fixed:**
- `secrets.compare_digest(x_admin_secret, settings.admin_secret)` crashed with an unhandled
  `TypeError` — surfacing as a real `500`, not a controlled `401` — whenever the `X-Admin-Secret`
  header was missing entirely. An intermediate draft typed the parameter `str | None` (to route a
  missing header through the dependency's own logic instead of FastAPI's default `422`) but never
  actually guarded against `None` before comparing. `mypy --strict` caught it statically
  (`Value of type variable "AnyStr" ... cannot be "str | None"`); a live `TestClient` request
  confirmed the crash before the fix and a clean, uniform `401` after adding an explicit
  `is None` check ahead of the comparison.
- **The more consequential one**: both admin routes originally computed `today = date.today()` once
  at module import time, not per request. Since a deployed backend stays running across many days
  rather than restarting at midnight, every trigger after the server's first day up would have
  silently run the pipeline against a stale, frozen date. Confirmed live by simulating a server
  that "started yesterday" and calling the route today — it generated a briefing tagged with
  yesterday's date, not today's. Fixed by moving `date.today()` inside each route function so it's
  computed fresh on every call; re-verified the same simulation now returns the correct date across
  a simulated day boundary.

**Verified locally first, then for real over real HTTP:**
- All four `verify_admin_secret` cases tested directly against a throwaway FastAPI route: missing
  header, empty header, and wrong secret all return `401`; the correct secret returns `200`.
- Both routes confirmed registered at their expected paths (`/v1/admin/trigger-briefing`,
  `/v1/admin/trigger-notifications`) via the running app's own OpenAPI schema.
- The stale-date bug reproduced live, then disproven live after the fix, as described above.

**Closed 2026-08-17, combined with M22's own remaining check into a single real run** (deliberately,
to avoid triggering the real pipeline twice in one day): with the backend running locally and a
throwaway device token attached to a real user, sent a real `POST /v1/admin/trigger-briefing` with
the correct `X-Admin-Secret` header — `200`, and a real `JobRun` (`status="success"`) plus a real
5-section `UserBriefing` for 2026-08-17 landed in the database, confirmed by direct query, not just
the HTTP response. Then, since it was a genuine weekday, sent a real
`POST /v1/admin/trigger-notifications` the same way — `200`, and the throwaway token's `is_active`
flipped from `True` to `False`, confirmed by direct query. Cleaned up the throwaway token
afterward. This proves both admin endpoints work end to end over real HTTP with real auth, not just
against a local test client — and doubles as M22's final missing piece (see below).

**Still deliberately not done, and not a gap**: no hosted cron actually points at these endpoints —
there's nowhere public to point one at until Milestone 42 (Production Backend Deployment). The
automation *surface* is done and proven; the actual schedule is real future work tied to
deployment, not an oversight.

### Milestone 22 — Backend Integration Test Pass (complete, 2026-08-15–17)

Per `docs/08` §12: end-to-end verification of the full new pipeline. Unlike every prior
verification this week (all one-off `python -c` scripts, run once and discarded), this one is
being built as a **permanent, reusable artifact** — `backend/scripts/integration_check.py` —
following the same reasoning Milestone 11 used to justify a real `pytest` suite over a throwaway
script: a script proves something worked once, on the date it ran; something you can re-run is a
standing, repeatable check. Deliberately kept as a standalone script rather than added to the real
`pytest` suite, though — `test_models.py` only exercises the database layer with no real cost or
rate-limit exposure; this script calls the *real* FMP, FRED, Marketaux, and OpenAI APIs and writes
to the *real* database, which is exactly the kind of thing that shouldn't run automatically on
every CI push (a lesson already learned the hard way this week from hitting FMP's daily quota
twice just from manual testing).

**What it does**: runs `run_daily_briefing_job(as_of)` for real (Step 1), reads the result back
through `get_todays_briefing` — called directly rather than over HTTP, since the script has no
real Clerk session token to authenticate with (Step 2) — then creates a throwaway test
`DeviceToken` and runs `send_daily_notifications(as_of)` against it (Step 3), cleaning the test row
up afterward regardless of outcome. Every stage appends a `(name, passed, detail)` result rather
than just trusting "it didn't crash," and prints one clear PASS/FAIL report at the end covering the
whole run.

**Real bugs found and fixed while writing it, several recurring from earlier this week**: a
missing `await` on `run_daily_briefing_job` (the exact same class of bug caught multiple times in
`briefing_service.py`/`openai_service.py` earlier this week — silently creates a coroutine that
never runs); `JobRun.job` instead of the model's actual `job_name` field; and a genuine
logic-ordering bug invisible to any tool — the final PASS/FAIL report was originally being printed
*before* Step 3 had even run, meaning Step 3's result silently never made it into the summary at
all, and "All checks passed" could print as true even if Step 3 later failed. Also recurring: the
same session-lifecycle bug from `briefing_service.py`'s first draft — cleanup code sitting outside
the `with SessionLocal()` block that owned the session it was trying to use.

**A genuinely valuable finding from actually running it, not a bug in the pipeline being
tested**: the first live run happened to land on a Saturday. Steps 1-2 passed cleanly (real
`JobRun` success, real `UserBriefing` created, correct date, a real generated headline). Step 3
reported `FAIL` — the test token was never deactivated — but tracing it back, that's because
`send_daily_notifications` correctly skipped the entire send step, exactly per its weekend-skip
design; the token was never touched because nothing ever tried to reach it. The real gap is in the
*script*, not the system: Step 3's check unconditionally expects deactivation, with no awareness
that weekends are supposed to behave differently. Rather than fix the check or burn another round
of real FMP/OpenAI cost re-running the whole thing same-day just to watch a weekday behavior that's
already been independently confirmed twice this week (once in `send_push_notifications`'s own
standalone test, once during M21's full live verification), the decision was to defer a full clean
pass to an actual weekday — scheduled 2026-08-17 — rather than spend more to re-prove something
already known.

**Closed 2026-08-17, but not by re-running `integration_check.py` itself.** By the time the
scheduled weekday arrived, M23's admin endpoints existed and could exercise the exact same
pipeline for real over real HTTP — so rather than run the script a second time and spend another
round of real FMP/OpenAI cost, the weekday check was done through `POST /v1/admin/trigger-briefing`
then `POST /v1/admin/trigger-notifications` (see M23's write-up above for the full detail). Same
throwaway-device-token technique the script itself uses; same real result the script was built to
confirm: the token's `is_active` flipped from `True` to `False`, a real Expo send attempt against a
real weekday, exactly the one thing a Saturday run couldn't exercise. `integration_check.py` itself
remains available as a standing, reusable check for future regressions — it just wasn't the tool
that closed this particular milestone.

### Milestone 21 — Personalized Notifications (backend scope complete, 2026-08-14)

Per `docs/08` §12 and `docs/02` §8/§22/§23: `device_tokens.user_id` migration, plus the actual
notification-sending pipeline. **Deliberately scoped to backend only** — decided explicitly before
starting, for two reasons: the milestone checklist already separates "Core Backend" from "Mobile
App" as different phases, and practically, testing "does a real notification arrive" needs a real
Expo push token from a real device with the app installed and permission granted, which doesn't
exist without the mobile registration flow. The daily briefing job and the notification job are
kept as two genuinely separate functions, not one combined into the other — matching the
architecture doc's own description of them as two distinct scheduled jobs, not a decision made for
convenience.

**A real scheduling question, settled before writing any code**: what happens to Saturday/Sunday?
Confirmed empirically (during M17's earlier re-verification): FMP's sector-performance endpoint
returns 0 sectors on weekends, since markets are closed — meaning a weekend run of the daily
briefing job would still generate a *real, non-empty* briefing (FRED data doesn't stop on
weekends), just with no market/sector/company content at all, even for users who opted into those
topics. Decided: the daily briefing job still runs every day regardless (FRED data is still real
and meaningful), but the *notification* specifically does not fire on weekends — keeping "calm, not
a firehose" intact without adding complexity to generation itself. A second, related decision: a
quiet-day briefing (`sections=[]`, M18's fallback) also does not trigger a notification — pinging
someone with "nothing notable to report" isn't worth doing.

**What got built:**
- `app/models/device_token.py` — added `user_id` (nullable `UUID`, `ForeignKey("users.id",
  ondelete="SET NULL")` — nullable specifically to preserve anonymous-device support before a user
  ever signs in, per the plan doc). Migration generated, reviewed (simple: one column, one FK, no
  ordering concerns like the earlier legacy-table cleanup had), applied, and verified live via
  `inspect(engine)`.
- `app/schemas/device_token.py` — `DeviceTokenRegistration` (`expo_push_token`, `device_id`,
  `platform`, `timezone`), matching `DeviceToken`'s real fields.
- `app/routers/notifications.py` — `POST /v1/notifications/register`, following `users.py`'s exact
  pattern (`Depends(get_current_user)`, `Depends(get_db)`), looking up or creating a `DeviceToken`
  row by `expo_push_token` and linking its `user_id` to the signed-in user. No separate service
  file for this — the write is simple enough to live directly in the router, same precedent
  `put_preferences` already set.
- `app/services/notification_service.py`:
  - `send_push_notifications(client, token, title, body)` — a plain `httpx.AsyncClient` POST to
    Expo's real push endpoint (`https://exp.host/--/api/v2/push/send`), confirmed against Expo's
    own docs to need no access token for basic sending (`EXPO_ACCESS_TOKEN`, already reserved in
    `.env.example`, is only for an optional enhanced-security mode, not needed for V1). On an
    Expo-reported `DeviceNotRegistered` error specifically, marks that `DeviceToken.is_active =
    False`; any other error just logs a warning, since a transient failure shouldn't permanently
    deactivate a valid token.
  - `send_daily_notifications(as_of)` — the batch job: skips entirely on Saturday/Sunday, finds
    every `UserBriefing` for the given date, skips any with empty `sections` (quiet days), looks up
    each remaining user's active `DeviceToken`(s), and sends concurrently — one shared
    `httpx.AsyncClient`, semaphore-bounded, matching `fred_service.py`/`marketaux_service.py`'s
    established batch pattern exactly. Notification text reuses that day's real briefing headline
    directly, rather than a separate notification-copy system — it's already personalized and
    category-aware by construction.

**Real bugs found and fixed along the way:**
- `db.scaler` — the same typo already caught once in `briefings.py`, recurring here in
  `notifications.py`'s registration endpoint. Confirmed by `mypy`.
- The deactivation logic went through two wrong states before landing correctly. First draft:
  every error type caused deactivation, not just `DeviceNotRegistered` — meaning a transient
  failure could wrongly deactivate a valid token. The fix attempt then inverted the condition
  entirely: `DeviceNotRegistered` (the case that's actually supposed to deactivate) fell into the
  branch that only logged a warning and did nothing, while every *other* error type deactivated the
  token — backwards in a different way. Caught both times by tracing the actual control flow by
  hand, not by any tool — `mypy` had nothing to say about either version, since both were valid,
  type-correct Python that just did the wrong thing.
- `briefing.headline`, then `briefing.context["headline"]` — two separate wrong guesses at how to
  reach the briefing's headline before landing on the correct `briefing.content["headline"]`.
  `UserBriefing.content` is the actual JSONB field; neither `headline` nor `context` exist on the
  model directly. `mypy` caught both, the second time even suggesting the fix directly
  (`"UserBriefing" has no attribute "context"; maybe "content"?`).

**Verified live, not just type-checked:**
- `send_push_notifications` tested directly against a throwaway `DeviceToken` row with a
  deliberately fake token: Expo correctly rejected it, classified under `DeviceNotRegistered`, and
  the row's `is_active` flipped from `True` to `False` exactly as designed.
- `send_daily_notifications` tested end-to-end reusing a real, already-existing `UserBriefing`
  (2026-08-11's, from M19/M20's own verification — deliberately avoided generating a *new* one just
  for this test, since that would mean spending real OpenAI/FMP cost with nothing new to prove):
  correctly found the real briefing, correctly did not skip it (real content, not empty), found the
  test device token, and attempted the send via the real Expo API — same deactivation behavior
  confirmed again on the fake token.
- The weekend skip tested directly against a real Saturday (2026-08-08): returned immediately, no
  database queries, no send attempts.

### Milestone 20 — Personalized Briefing API (complete, 2026-08-11)

Per `docs/08` §12: an endpoint serving a signed-in user's own `user_briefings` row, replacing the
old single-briefing `GET /briefings/today` design (which made sense pre-pivot, when every user got
the same briefing — now it needs to be scoped to whoever's authenticated).

**What got built.** `backend/app/routers/briefings.py` — `GET /v1/users/me/briefing`, following
`users.py`'s exact established pattern (`Depends(get_current_user)` for auth, `Depends(get_db)`
for the request-scoped session). Chose this path over the plan doc's literal old name
(`/briefings/today`) deliberately, for consistency with the one other existing endpoint
(`/users/me/preferences`) rather than preserving a pre-pivot URL that no longer describes what the
resource actually is. `app/schemas/user_briefing.py` gained `UserBriefingResponse` (`date` +
`content: BriefingContent`) alongside the existing `BriefingContent`/`BriefingSection`. Registered
in `app/routers/__init__.py` the same way `users_router` is.

Logic: query `UserBriefing` for `user_id == current user AND date == today`. If found, unpack its
stored JSONB `content` back into a real `BriefingContent` and return it with the date. If not found
(the daily job hasn't run yet today, or a brand-new user), return a `200` — not a `404` — with a
friendly fallback message ("No briefing available yet for today.") in the exact same response
shape, so the client only ever has to handle one shape regardless of *why* there's nothing to show.
Deliberately distinct from M18's quiet-day message ("Nothing notable to report today."), since the
two mean different things: one says the job ran and found nothing relevant, the other says nothing
has run yet at all.

**Real bugs found and fixed along the way:**
- `user: User = Depends(get_db)` — passed the database-session dependency where the auth dependency
  belonged, meaning a `Session` object would have been injected where a `User` was expected. Not
  caught by `mypy`: FastAPI's `Depends()` stub accepts `Any`, so it never actually checks a
  dependency function's real return type against the parameter's annotation — this kind of mismatch
  is invisible to the type-checker no matter how carefully the rest of the file is typed.
- `db.scaler(...)` — typo for `db.scalar(...)`; this one `mypy` did catch (`"Session" has no
  attribute "scaler"`).
- **The most consequential one, found only by actually running it, not by reading or type-checking**:
  the route was declared as `@router.get("users/me/briefing", ...)` — missing its leading slash.
  Tested directly with `TestClient`: with the slash, `GET /v1/users/me/briefing` → `200`; without
  it, the same request → `404`, because the router's `/v1` prefix concatenates directly onto the
  route string with no separator, silently registering the endpoint at `/v1users/me/briefing`
  instead — a URL nothing would ever actually call. `mypy` and `ruff` both had nothing to say about
  either version; this only surfaced by hitting the app with a real request and checking the status
  code.
- Two typos in the fallback message text ("Np birefing" → "No briefing").

**Verified live, not just type-checked:**
- `TestClient` request to `GET /v1/users/me/briefing` with no auth token → `403 Forbidden`, not
  `404` — confirms the route is registered at the correct path and Clerk's auth guard is actually
  being reached.
- Called the endpoint function directly (bypassing HTTP-level Clerk auth, which needs a real token)
  against the real database: the "found" branch correctly retrieved and reconstructed the real
  `UserBriefing` row created during M19's live run that same day (headline, all 3 sections intact);
  the "not found" branch, tested against a date with no persisted row, correctly returned the exact
  fallback message with empty `sections`.

### Milestone 19 — Daily Briefing Orchestrator (complete, 2026-08-11)

Per `docs/08` §12, this milestone's job is `briefing_service.py`, wiring Milestones 15-18 together
end to end with one `job_runs` row per run. The code itself is done and reviewed; **it has not yet
been run against the real pipeline** — deliberately deferred to avoid a third same-day hit against
FMP's free-tier rate limit (see M17's amendment note above) and to combine it with finishing that
interrupted verification in one real run, scheduled for 2026-08-11.

**What got built.** `backend/app/services/briefing_service.py` — `run_daily_briefing_job(as_of)`:
creates a `JobRun` row (`job_name="daily_briefing_job"`, `status="running"`) and commits it
immediately, before anything risky runs, so a run's start is on record even if something crashes
unexpectedly later. Then: stage 1 (`fetch_covered_daily_data_candidates` →
`saved_covered_daily_data_candidates`) and stage 2 (`generate_and_persist_all_briefings`) run
inside one `try`/`except` — if stage 1 fails, stage 2 never runs, by design (a deliberate decision,
not an accident: no fresh data means nothing to personalize from). Stage 3
(`delete_stale_daily_data`) runs in its own separate `try`/`except` regardless of whether stages
1/2 succeeded, since it's independent maintenance (purging data older than 48 hours) unrelated to
today's fetch/generation outcome — the reasoning being that a bad day for fetching new data
shouldn't also mean old data stops aging out, which would work against the whole point of the
48-hour retention design. `MARKET_CAP_THRESHOLD = 10_000_000_000.0` is now a real named constant
in this file — previously every call site across the whole session (including all of M17/M18's
own testing) just typed the same $10B magic number by hand.

**Real bugs found and fixed, none caught by casual reading — all via `mypy` or direct testing:**
- Both async calls (`fetch_covered_daily_data_candidates`, `generate_and_persist_all_briefings`)
  were originally called without `await` — silently created coroutine objects that never actually
  ran, meaning neither the fetch nor the generation loop executed at all. `mypy`:
  `Value of type "Coroutine[...]" must be used`.
- `fetch_covered_daily_data_candidates`'s return value was discarded, and
  `saved_covered_daily_data_candidates` was called with only one argument (`as_of`) instead of its
  real two (`covered_candidates`, `as_of`) — meaning the date value would have bound to the wrong
  parameter entirely. `mypy` caught both.
- **The most dangerous one, caught by mypy on neither pass — only by actually running it**: an
  early draft's `with SessionLocal() as session:` block only wrapped the `JobRun` row's *creation*,
  not the rest of the function. Everything after — including the final `job_run.status = ...`
  assignments and the closing `session.commit()` — ran *after* the session had already closed.
  Proved live (using a disposable test row, no external APIs involved) that this doesn't raise any
  exception at all: the commit "succeeds" silently, but nothing actually gets written, because the
  detached `job_run` object is no longer tracked by the closed session. Every run would have shown
  `status="running"` forever, indistinguishable from a run that's still in progress, with no error
  to indicate anything was ever wrong. Fixed by extending the `with` block to cover the entire
  function body; re-verified live afterward that a full create → mutate → commit cycle within one
  session actually persists correctly.

**A separate, unrelated bug found and fixed along the way, while re-attempting M17's live
verification this morning**: `fred_service.py`'s `_log_request_error` (and a second, duplicate
`extra={...}` call in `fetch_all`'s `ValueError` branch) passed a context key literally named
`name` — which collides with `logging.LogRecord`'s own reserved `name` attribute (the logger's
name, unrelated to a FRED series' name) and raised `KeyError: "Attempt to overwrite 'name' in
LogRecord"` from *inside* the error-logging path itself. Net effect: a single transient network
timeout on one of 39 FRED indicators crashed the entire batch instead of being logged and skipped,
exactly defeating the "skip-and-continue per item" design M15 was built around. Renamed the
colliding key to `indicator_name` in both spots; confirmed live afterward that the real pipeline
run completed cleanly (all 39 FRED calls attempted, 29 covered by news; all 11 sectors correctly
persisted and 11 of 11 survived the coverage filter — full confirmation of M17's earlier sector
fix, up from yesterday's partial 10 of 11).

**Live end-to-end verification, run for real on 2026-08-11 (`run_daily_briefing_job(date.today())`,
completed in 46.6s)** — this run also fully closed out M17's gainer/loser confirmation, blocked
twice earlier in the week by FMP's rate limit:
- `JobRun`: `status="success"`, real `started_at`/`finished_at`, `error_message=None`.
- All 11 sectors persisted and covered. **Gainer/loser confirmed for the first time this
  week** — `company: SE` (+13.67%, gainer) and `company: ONON` (-19.37%, loser) both landed.
- The 48-hour cleanup fired for real (not just in isolated testing) and correctly purged genuinely
  stale data — 39 leftover rows from 2026-08-03 (over a week old) were gone after the run, verified
  directly against the live database, not just "the function didn't error."
- One real `UserBriefing` row generated (the one live user, category `student`, all 3 FMP topics
  opted in) — a coherent, well-grounded headline + 3 sections, correctly framed around
  internships/early-career hiring rather than generic market commentary, every figure traced back
  to real supplied data. One real content finding, deliberately left alone for now: the filtering
  pipeline correctly gathered all 29 relevant items including full market/sector/company data (per
  this user's opted-in topics), but the model's own editorial choice of "a few sections" didn't
  end up covering any of the market-related content that day — a prompt-design question to revisit
  once there's a full prototype to test against, not a bug (the data reached the model; it just
  chose not to write about all of it).

### Milestone 18 — Per-User OpenAI Briefing Generation (complete, 2026-08-09)

Per `docs/08` §9/§12, this milestone's job was `openai_service.py`, the `user_briefings` table +
migration, and the per-user generation loop — turning M13-17's per-user preferences and shared
daily data into one personalized `BriefingContent` per registered user per day.

**1. FRED/FMP relevance tables.** `backend/app/services/fmp_category_rules.py` (renamed from
`category_config.py` once it grew to hold FMP content too) — `CATEGORY_ITEM_KEYS`/
`TOPIC_ITEM_KEYS` (FRED series IDs per category/topic, transcribed from `docs/08` §5/§6 and
cross-checked programmatically against the real 39-series master list — all 39 accounted for, no
typos) and `MarketContentRules`/`CATEGORY_MARKET_CONTENT`/`TOPIC_MARKET_CONTENT` (FMP index/
sector/company rules per category/topic). A 9th additional-topic, `interest_rates_monetary_policy`,
was added to `mobile/app/(onboarding)/topics.tsx` — `docs/08` §5 tags FRED items 22-29 as their own
topic group, but the 8 topics originally implemented never exposed it. Home Owners' named-sector
filter (`"Real Estate"`, `"Financial Services"`, `"Consumer Cyclical"`) was verified against a live
call to FMP's sector-performance-snapshot endpoint, not assumed from the plan doc's looser wording
("Consumer Discretionary") — confirmed FMP's actual naming already matched what had been written.

**2. A real M17 pipeline fix, discovered as a blocker while building the tables above.**
`docs/08` §6 says Investors/"I Want Everything" should see all 11 sector performances, but M17's
`fetch_and_shape_fmp_candidates` only ever built candidates for the best and worst sector — the
other 9 were fetched from FMP but never turned into persisted `DailyDataItem` candidates at all.
Fixed by looping over the full `sector_performances` list instead of calling `pick_best_and_worst`
at fetch time; that computation now belongs to M18's own filtering logic instead (per-category, at
generation time, against the 11 persisted rows), since M17's job is raw collection, not deciding
which sectors matter to which user. Re-verified live afterward (see §6 below).

**3. Legacy table cleanup.** `Briefing`, `EconomicEvent`, `EnrichedEvent`, `FredSeries`, and
`NewsArticle` — the entire pre-personalization-pivot schema, superseded by `daily_data_items`/
`daily_data_news`/`user_briefings` but never actually removed — were still live tables in
Supabase and still registered in `app/models/__init__.py`. Deleted all five model files, generated
the drop migration, and caught a real autogenerate bug before applying it: the generated
`upgrade()`/`downgrade()` dropped/recreated tables in the wrong order relative to their own FK
dependency chain (`briefings ← economic_events ← {enriched_events, fred_series, news_articles}`),
which would have failed against Postgres's referential-integrity checks. Reordered by hand,
verified both an empty-table check (all 5 had 0 rows — safe to drop) and the post-migration live
schema (`inspect(engine)` — all 5 gone, nothing else touched).

**4. `user_briefings` table.** `backend/app/models/user_briefings.py` (`UserBriefing`) — `id`,
`user_id` (FK → `users.id`, `CASCADE`), `date`, `content` (JSONB), `fetched_at`, plus a
`(user_id, date)` unique constraint enabling skip-if-exists. Migration applied and verified live
(columns, FK, constraint, index all confirmed via direct `inspect(engine)` calls). Renamed from an
initial `DailyBriefing`/`daily_briefings` for consistency with the plan doc's own naming.

**5. `app/schemas/user_briefing.py`** — `BriefingContent` (`headline` + `sections`) and
`BriefingSection` (`heading` + `body`), the structured-output schema requested from OpenAI.
Verified to round-trip cleanly through `model_dump(mode="json")` → dict → `model_validate`, the
exact path it takes into and out of `UserBriefing.content`'s JSONB column.

**6. `app/services/prompt_services.py`** — `CATEGORY_MAIN_QUESTIONS` (the 7 categories' framing
questions from `docs/08` §6, not previously in code) and `build_developer_message`, generating the
system/developer message per category. `build_user_message` turns a user's filtered
`DailyDataItemWithNews` list into the actual data text sent to the model, branching per item shape
(FRED's flat `{name, value}`, FMP index/sector/company's differently-shaped `raw_data`) and
attaching each item's real news headlines/summaries. `build_quiet_day_briefing` is the static
fallback (`headline="Nothing notable to report today.", sections=[]`) used when a user's filtered
dataset is empty — deliberately returns a fresh instance per call, not a shared module constant,
since `BriefingContent` is a mutable Pydantic model. `DailyDataItemWithNews` itself lives here
(not in `openai_service.py`, where it was first written) specifically to keep the import direction
one-way once `openai_service.py` needed to call back into this module for the actual API call.

**7. `backend/app/services/openai_service.py`** — the full pipeline:
- `get_user_daily_data_with_news(user, as_of)` — resolves a user's category + topics into relevant
  FRED/FMP `DailyDataItem` rows for the day and attaches each one's linked news. Verified live
  against a real user (category `student`, all 3 FMP topics): 20 relevant items, 57 attached
  articles.
- `generate_briefing_content(user, as_of)` — the actual OpenAI call. Short-circuits to
  `build_quiet_day_briefing()` before ever building a prompt if the filtered dataset is empty (no
  API cost for quiet days — verified live: a date with no persisted data produced the fallback
  with zero network calls), and again if `response.output_parsed` comes back `None` (a real
  possible outcome per the SDK's own types, not assumed impossible). Uses `gpt-5-nano` — confirmed
  against OpenAI's own live docs as the cheapest current model by both input/output price, not
  taken from unreliable pricing-aggregator sites that surfaced inconsistent model names on the
  first attempt.
- `generate_and_persist_all_briefings(as_of)` — the per-user loop. Queries users with a set
  `category` (users who haven't finished onboarding are skipped rather than getting a confusing
  daily "nothing to report" push), filters out anyone already having a `UserBriefing` for the day
  in one batched query (not N individual ones), then runs the rest concurrently
  (`asyncio.Semaphore`-bounded, matching `fred_service.py`/`marketaux_service.py`'s existing
  pattern) with per-user failure isolation via `openai.OpenAIError` so one user's API failure can't
  take down the batch.

**Real bugs found and fixed, mostly through review rather than tooling** — this milestone had an
unusually high count, several repeating the same shape:
- The `backend.app.services.X` import-path typo (an extra, incorrect `backend.` prefix) recurred
  twice across two different files during the session.
- Three separate instances of a `return` statement (or, in one case, a whole conditional branch)
  sitting one indentation level too deep, inside a loop or an `if`/`else` block instead of after
  it — `filter_fmp_items_by_rules` (silently dropped every candidate but the first sector match and
  skipped company spotlights entirely for `wants_all_sectors` categories), `build_user_message`
  (returned after the first of 20 items instead of all of them), and `generate_briefing_content`
  (the quiet-day check never actually short-circuited the API call). Caught each time by tracing
  control flow by hand and then proving it with a live call, not by trusting that "it didn't error."
- A `list`/`set` type mismatch (`relevant_items: list[...] = set()`) combined with mixed
  `.extend()`/`.add()`/`.update()` calls on the same variable — real, `mypy`-confirmed, would have
  crashed on the very first item processed.
- A trailing comma inside a frozen dataclass's field defaults (`wants_all_sectors: bool = False,`)
  silently turning the default into a 1-tuple — Python-truthy, so it would have inverted the
  intended "Consumers get no market content by default" design without ever raising an error.
- `rules.named_secotrs` (typo) and a loop variable shadowing its own function's list parameter
  (`for item_with_news in item_with_news:`) — the latter didn't break at runtime (the `for`
  statement captures its iterable before reassignment happens) but broke `mypy`'s ability to check
  the rest of the function, masking a real, separate bug underneath it.
- A stray space inside an f-string format spec (`{value: +.2f}` instead of `{value:+.2f}`) —
  crashed with `ValueError` on the first sector item, only surfacing once the two bugs stacked
  above it were cleared.
- `item.raw_data`'s declared type (`dict | list | None`, kept broad for other potential uses)
  didn't match its actual guaranteed shape at the one call site that needed it — resolved with
  `cast`, the same idiom already used for `item.value`'s narrower-in-practice-than-declared type.
- `.scalar()` instead of `.scalars()`, `model_dunp` instead of `model_dump`, `extras=` instead of
  `extra=` (the last one meaning the very error-logging path meant to isolate one user's failure
  would itself have thrown a new, different exception) — all caught by `mypy` once surfaced.
- A DB session queried after its own `with SessionLocal()` block had already closed — not caught
  by any tool, only by reading the indentation.

**End-to-end verification, run live, not just type-checked:**
- The full generation path against a real user's real data produced a coherent, well-structured
  `BriefingContent` (1 headline, 4 sections) correctly framed around that user's category ("early-
  career prospects," "internships" for a `student` user). Spot-checked for fabrication: a set of
  HELOC/home-equity figures in the output initially looked hallucinated (never explicitly formatted
  into the prompt as structured data) — traced back and confirmed they came from a real attached
  Marketaux news article's summary text, correctly grounding the narrative in supplied news rather
  than inventing numbers, exactly as the developer message instructs.
- Quiet-day short-circuit confirmed to make zero API calls when a user's filtered dataset is empty.
- Skip-if-exists confirmed by running `generate_and_persist_all_briefings` twice against the same
  date — identical row count both times, no duplicate.
- M17's sector fix (item 2 above) re-verified live: 10 of 11 sectors correctly survived the
  Marketaux coverage filter against real data (only Consumer Defensive had no matching news that
  day) — up from the old ceiling of 2. Gainer/loser coverage wasn't confirmed in this same run;
  FMP's free-tier daily quota (250 requests/day) was exhausted partway through by the volume of
  live testing done this session. A reminder is scheduled for 2026-08-10 to finish that check once
  the quota resets.

### Milestone 17 — Daily Data Pipeline & Storage (complete, 2026-08-03)

*(Amended 2026-08-09 during M18: the sector-persistence gap described below — only the best/worst
of 11 sectors ever became a `DailyDataItem` — was found and fixed while building M18's category
mapping. See M18's write-up above for the fix and its live re-verification.)*

All three pieces from `docs/08` §8 are done, and the full chain has been verified end-to-end
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

### Milestone 12 — FMP Market Data Service (complete, formal sign-off closed out 2026-08-09)

The code itself was done and verified back on 2026-07-17; only the formal sign-off (this checklist
entry, this section header) was left open for several milestones. Closing it out now, alongside
Milestone 18, since both touch the same "Completed Milestones" list.

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
- **Resolved since this section was first written:**
  - **The re-scoping question** ("what do Milestones 13/16/18/20 even mean without discrete
    events") is what `docs/08-personalization-pivot-plan.md` turned out to answer — not a
    continuation of Milestone 12's original numbering, but a full pivot toward per-user
    personalization, with its own milestone breakdown (new Milestones 13-22) that's since been
    implemented through Milestone 18 (see above). The `economic_events`-based persistence model
    referenced below was itself superseded and later deleted (see Milestone 18's write-up, item 3).
- **Still open, not yet done:**
  - **Key rotation** — the FMP key was briefly printed into a terminal error message during
    ad-hoc testing early in this milestone (same category as the Milestone 6 Supabase key
    exposure). Worth rotating from the FMP dashboard; still not confirmed done, explicitly
    deferred as low-urgency.
  - `docs/01-product-requirements.md` §10 (MVP Definition) still describes "five most important
    economic events" — not yet reconciled with the personalization pivot's actual shape. Also
    likely worth checking `docs/02-system-architecture.md` §5/§12 for the same kind of staleness
    given how much has changed since either doc was last touched.

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
  milestone breakdown: `docs/08-personalization-pivot-plan.md`. This is reflected in `docs/01`
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
  `docs/07-code-reference-milestones-3-6-9.md` comes up again during later work (SQLAlchemy
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
- `docs/07-code-reference-milestones-3-6-9.md` — snapshot of the actual code from the three
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
  (e.g. custom native modules) or CI device testing later. **This means the app has never been run
  on Android at all** — a real, tracked gap surfaced explicitly during M34 scoping (2026-09-02).
  `docs/03`'s M34 (Mobile Integration Test Pass) was originally scoped for "both iOS and Android";
  decided to scope M34 to iOS-only rather than block on setting up Android tooling now — Android
  becomes its own follow-up once a device/emulator is available, not silently skipped.
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
- **Resolved for real (2026-08-25)** — the 2026-08-20 fix was incomplete (see history below); this
  time it's the actual root cause, confirmed live across all three auth methods.
  `redirectAfterAuth` used to get called twice on sign-up/sign-in (once explicitly inside
  `signUp.finalize()`/`setActive()`'s `navigate` callback, once via a `useEffect` watching
  `isSignedIn`), and the duplicate could lose a timing race against Clerk's session activation.
  Two real fixes landed together: (1) a `useRef` guard (`hasRedirected`), set **synchronously
  before** calling `finalize`/`setActive` — not inside their `navigate` callback, since that runs
  asynchronously and isn't guaranteed to execute before React reacts to `isSignedIn` changing and
  fires the effect; setting it before the call, on the same synchronous tick, closes that ordering
  gap for real. (2) Switched from the outer `getToken` (from `useAuth()`, which lags slightly
  behind session activation) to `session.getToken()` — the token method on the concrete session
  object Clerk hands directly to the `navigate` callback, tied to the session that's already
  confirmed active rather than the broader React hook state. Applied consistently across all three
  auth methods (password, Google, Apple) in both `sign-in.tsx` and `sign-up.tsx` — a real
  inconsistency was caught and fixed along the way: `sign-up.tsx` initially got the `session.getToken()`
  upgrade on all three flows while `sign-in.tsx`'s Apple flow was missed, still using the old
  outer-`getToken`/no-`navigate`-callback pattern; brought in line with the other two. The
  `useEffect` itself is untouched — still needed for a user landing back on `/sign-in`/`/sign-up`
  while already signed in — the fix is entirely in what happens around it.

  **History, for context:** originally found 2026-08-19 (M24 device verification), "fixed" 2026-08-20
  with a `getToken()` retry loop that reduced frequency but didn't eliminate the race — reopened
  2026-08-24 when it recurred live under exceptionally unstable network conditions (multiple
  hotspot switches, repeated backend restarts). A separate, real bug was also found and fixed
  2026-08-24: the `catch` block redirected to `/category` on *any* failure, not just a confirmed
  `category === null`, meaning a transient failure could make an already-onboarded user's profile
  look wiped (sending them back through onboarding) even though their real database row was
  completely untouched (confirmed directly against the DB at the time). That fix — only a confirmed
  null redirects to `/category`, anything else falls back to `/` — is independent of today's fix
  and stays in place.

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

*(Rewritten 2026-08-09, updated 2026-08-10, updated 2026-08-11 (twice), updated 2026-08-14, updated
2026-08-15, updated 2026-08-17 (M22/M23 both closed), updated 2026-08-19, updated 2026-08-20 (M24/M25
closed), updated 2026-08-20 (`redirectAfterAuth` fix confirmed live — later found incomplete),
updated 2026-08-20 (M26 closed), updated 2026-08-21 (M27 confirmed live and closed), updated
2026-08-21 (M28 confirmed live and closed), updated 2026-08-21 (M29 confirmed live and closed),
updated 2026-08-24 (backend indicator-data extension resolved M30's real blocker), updated
2026-08-24 (M30 itself deferred, not part of V1), updated 2026-08-24 (M31 backend done, mobile side
started), updated 2026-08-24 (M31 confirmed live and closed), updated 2026-08-24 (M32 in progress,
`redirectAfterAuth` reopened), updated 2026-08-25 (`redirectAfterAuth` genuinely fixed and confirmed
live), updated 2026-08-25 (M32 confirmed live and closed), updated 2026-08-25 (M33 code complete,
on-device verification still pending), updated 2026-09-02 (M33 confirmed live and closed), updated
again 2026-09-02 (M34 confirmed live and closed, iOS-only — Part 3 fully complete) — item 1 below
now points to Milestone 35, the start of Part 4.)*

1. **PRIORITY when resuming: start Milestone 35 — Expo Notifications Setup**, the first milestone
   of Part 4 (Notifications, QA, Deployment & Launch). Per `docs/03`: `expo-notifications`/
   `expo-device`, permission request, Expo push token retrieval, physical-device handling — client
   capability work that doesn't depend on the personalization model, so it carries over unchanged
   from the roadmap's original scope. Note: Milestone 21's backend notification-sending logic
   (`notification_service.py`) is already built and verified — this milestone is specifically the
   mobile side (requesting permission, obtaining the token) that was deliberately deferred to Part 3
   back when M21 was built. Android testing remains an explicit, tracked gap (see Known Issues) —
   worth deciding whether to address it before or during the notifications work, since push
   notification behavior genuinely differs between iOS and Android.
2. Two small Milestone 14 loose ends, not blocking anything: a name field (decided to live in
   onboarding, not Clerk sign-up fields) and a settings screen for changing category/topics later.
3. Rotate the FMP API key (briefly exposed in a terminal error message during Milestone 12
   testing) as a precaution — still not confirmed done.
4. Decide whether/how to wire `pytest` into CI (see Known Issues) — needs a decision on test
   database strategy before it's a simple config change.
5. `docs/01-product-requirements.md` §10 (MVP Definition) still describes "five most important
   economic events," not reconciled with the personalization pivot — worth checking
   `docs/02-system-architecture.md` §5/§12 for the same kind of staleness while at it.
6. A real product/prompt-design question surfaced during M19's live verification, deliberately
   deferred until there's a full prototype to test against: a user's opted-in market/sector/company
   topics correctly reach the model as real data, but the model's own editorial judgment about
   which "few sections" to write doesn't guarantee every opted-in topic actually shows up in the
   output. Worth revisiting whether the developer message needs to require covering every topic
   area, or whether letting the model choose is the intended behavior.
