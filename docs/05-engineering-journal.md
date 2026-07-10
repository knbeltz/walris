# Walris Engineering Journal

**Document:** docs/05-engineering-journal.md
**Version:** 1.0
**Status:** Living Document
**Product:** Walris

---

## Entry Template

```markdown
## Entry [N] — YYYY-MM-DD

### Session Goal



### Work Completed

-
```

## Entry 1 — 2026-07-08

### Session Goal

Set up the FastAPI app: initial config, logger, and health router.

### Work Completed

- Created a settings/config module so logging behavior can differ between development and production.
- Implemented `configure_logging`, which sets DEBUG-level logs in development and INFO-level logs in production.
- Created a health router returning `{"status": "ok"}` on `GET /health` with an HTTP 200 response.
- Wired settings, logging, and the health router together in `main.py`, creating the FastAPI app instance.

## Entry 2 — 2026-07-09

### Session Goal

Set up the frontend configuration which include routing, styling, component libraries, and data fetching as well as the backend tooling. 


### Work Completed

Routing: 
- expo-router: Turns app/ folder into screen list so that a manual navigation set up is not needed. 

- expo-linking, expo-constants, expo-status-bar: Small support pacakges. 

- react-native-screens, react-native-safe-area-context: Make navigation utilize native, GPU-backed containers instead of plain views, and let screens know where the notch/home-indicator safe zones are. 


Styling: 
- nativewind: Lets you write classnames on React Native components. Nativewind compiles those class names into real styles at build time (React Native has no CSS engine on its own). 

- tailwindcss: Underlying utility class system NativeWind is built on 

- react-native-reanimated + react-native-worklets: ANimation library NativeWind relies on internally, plus its own required companion package. 

- tailwindcss-animate: Adds animation-related utility classes (fade, slide, etc.) to Tailwind's vocabulary. 

Component library (React Native Reusables):
- class-variance-authority (cva): Snall helper for defining a component's style variants (e.g. a Button's "default" vs "destructive" vs "outline" look) in one place. 

- clsx: Conditonally joins class name strings together (e.g. "only add this class if the button is disabled"). 

- tailwind-merge: Resolves conflicts when two Tailwind classes fight over the same property (e.g. if both p-2 and p-4 end up on the same element, it keeps the one that should win). 

- @rn-primitives/portal: Lets a component (like a model or tooltip) render its content somewhere else in the tree - normally components can only render inside their own parent, but overlays need to appear on top of everything. 

-@react-native-reusables/cli: A command-line-tool (like a generator) that writes ready made component files (Button, Card, etc) into the project. 

Data Fetching: 
- @tanstack/react-query: Manages data that comes from the backend: caching it, tracking loading/error states, refetching in the background. 

Backend Tooling: 
- ruff: Tool that finds problems in Python code (unused imports, bug-prone patterns) and auto-formats it, replacing the older two-tool combo of a seperate linter + Black. 

- mypy: Checks whether or not type hints are consistent (e.g. catches passing a string where a function expects a number) without ever running the code. 

- pydantic's mypy plugin (referenced in pyproject.toml, bit a seperate install) which teaches mypy how to correctly understand Pydantic's models, which do some behind-the-scenes magic mypy can't follow on its own. 

Mobile Tooling: 
- eslint: JS/TS equivelent of Ruff's linting half: flags problems in code. 

- eslint-config-expo: Ready made rule set from Expo, turned React Native projects, so not just hand-picking dozens of individual rules. 

- prettier: Formatter (JS/TS's equivalent of Ruff's formatting half) 

- prettier-plugin-tailwindcss: Automatically sorts your tailwind class names into a consistent order (e.g. always layout classes before color classes)

- eslint-config-prettier: Turns off the handful of ESLint rules that would otherwise disagree with Prettier about formatting, so the two tools don't fight each other. 

ENV Variables: 
- ENVIRONMENT: Tells the backend whether its running in "development" or "production" which affects logging verbosity. 

- Everything else in backend/.env.example (DATABASE_URL, SUPABASE_URL, FINNHUB_API_KEY, etc) and mobile/.env.local.example's EXPO_PUBLIC_API_BASE_URL: These are placeholders documenting what configuration will be needed once their owning milestones. 


## Decision Log

Use this section to record important decisions.

### Decision 1 — Use React Native + Expo

**Decision**: Walris will use React Native with Expo for mobile development.

**Reason**: Expo simplifies development, testing, builds, and eventual App Store / Google Play
deployment.

**Tradeoff**: Some native customization may be harder later, but the speed advantage is worth it
for V1.

### Decision 2 — Use FastAPI Backend

**Decision**: Walris will use FastAPI for the backend.

**Reason**: The app has a data-heavy and AI-heavy backend. Python is better suited for API
integrations, data processing, Pydantic schemas, and OpenAI workflows.

**Tradeoff**: The frontend and backend will use different languages, but the architectural fit
is stronger.

### Decision 3 — Use Supabase PostgreSQL

**Decision**: Walris will use Supabase PostgreSQL as the database and content cache.

**Reason**: The data model is relational: briefings, events, enriched summaries, FRED context,
news articles, and device tokens.

**Tradeoff**: Supabase is more structured than a NoSQL database, but the structure is beneficial
for this project.

### Decision 4 — No Authentication in V1

**Decision**: Walris V1 will not include user accounts.

**Reason**: The MVP does not include personalization, bookmarks, watchlists, or premium
features. Authentication would add friction without immediate value.

**Tradeoff**: User-specific features must be deferred to V2.

### Decision 5 — Static Daily Briefing for V1

**Decision**: Walris V1 will generate one daily briefing on a scheduled morning job.

**Reason**: This is significantly simpler than an event-driven live briefing architecture and is
sufficient to validate the core product hypothesis.

**Tradeoff**: The briefing may not reflect economic releases that occur later in the day until
the next scheduled update.

### Decision 6 — Use Expo Notifications

**Decision**: Walris will use Expo Notifications for morning push notifications.

**Reason**: Expo Notifications integrates naturally with the chosen mobile stack and supports
iOS and Android push workflows.

**Tradeoff**: Future advanced notification logic may require deeper native or provider-specific
configuration.
