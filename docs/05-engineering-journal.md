# Walris Engineering Journal

**Document:** docs/05-engineering-journal.md
**Version:** 1.0
**Status:** Living Document
**Product:** Walris

---

## Purpose

The Engineering Journal is a running record of what was built, what was learned, what decisions
were made, and what problems were encountered while developing Walris.

This document should be updated after every meaningful development session.

The goal is not perfection.

The goal is to build the habit of thinking like an engineer.

## Why This Matters

Walris is not only a product project.

It is also a learning project.

The Engineering Journal helps track:

- Technical decisions
- Bugs encountered
- Debugging process
- Architecture tradeoffs
- Claude Code interactions
- Lessons learned
- Questions to revisit
- Refactoring opportunities

Over time, this journal becomes evidence of engineering growth.

## How to Use This Journal

After each development session, spend 10–15 minutes writing an entry.

Each entry should answer:

- What did I build?
- What problem did I run into?
- How did I solve it?
- What did I learn?
- What still feels unclear?
- What should I do next?

Do not write vague notes.

Write enough detail that future-you can understand what happened.

## Journal Entry Template

```markdown
## Entry [Number] — [Date]

### Session Goal

What was I trying to accomplish?

### Work Completed

-
-
-

### Technical Decisions Made

-
-
-

### Bugs / Problems Encountered

-
-
-

### How I Debugged

-
-
-

### What I Learned

-
-
-

### Claude Code Notes

What did Claude Code help with?

What did I understand myself?

What did I rely on too heavily?

### Questions / Confusions

-
-
-

### Next Steps

-
-
-
```

## Example Entry

> The entry below is an illustrative example only — not a real journal entry. Real entries must
> be written by the developer, not generated on their behalf.

### Entry 1 — YYYY-MM-DD

#### Session Goal

Set up the initial Walris repository structure and create the `mobile`, `backend`, and `docs`
directories.

#### Work Completed

- Created the root `walris` repository.
- Added `mobile/`, `backend/`, and `docs/`.
- Added initial documentation files.
- Initialized Git and pushed the first commit to GitHub.

#### Technical Decisions Made

- Decided to keep mobile and backend in one monorepo.
- Decided to keep documentation in version control.
- Decided to use FastAPI for backend and Expo for mobile.

#### Bugs / Problems Encountered

- I was initially unsure whether to use separate repositories for mobile and backend.
- I also needed to decide whether documentation should live in Notion or GitHub.

#### How I Debugged

- Compared monorepo vs multi-repo tradeoffs.
- Chose monorepo because the project is solo-developed and easier to manage in one place.

#### What I Learned

- A clean folder structure reduces future confusion.
- Documentation should live close to the code because product and engineering decisions change
  as implementation evolves.

#### Claude Code Notes

Claude Code helped explain the purpose of each folder.

I made the final decision to use a monorepo.

#### Questions / Confusions

- How detailed should each documentation file become before coding?
- Should deployment config live at the root or inside each app?

#### Next Steps

- Scaffold the FastAPI backend.
- Scaffold the Expo mobile app.
- Add `.env.example` files.
- Configure formatting and linting.

## Engineering Reflection Prompts

Use these when you are stuck or after a difficult session.

### Architecture Reflection

- Did I put this logic in the right layer?
- Should this belong in the frontend, backend, database, or external service?
- Will this still make sense when the app grows?

### Debugging Reflection

- What did I expect to happen?
- What actually happened?
- What changed recently?
- What is the smallest reproducible version of the bug?
- What logs or errors give me evidence?

### AI Tutor Reflection

- Did I understand the code Claude gave me?
- Could I explain it back in my own words?
- Did I ask for hints before asking for the answer?
- Did I review the code before accepting it?
- Did I test the code myself?

### Product Reflection

- Does this feature help users understand the economy faster?
- Am I building something users need now or something I personally find interesting?
- Is this necessary for V1?
- Can this be deferred?

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

## Technical Debt Log

Use this section to track shortcuts or deferred improvements.

```markdown
## Debt Item [Number] — [Title]

### Description

What shortcut was taken?

### Why It Was Acceptable

Why was this okay for now?

### Risk

What could happen if this is ignored?

### Future Fix

How should this be resolved later?
```

## Bug Log

Use this section for significant bugs.

```markdown
## Bug [Number] — [Title]

### Date Found

YYYY-MM-DD

### Description

What happened?

### Expected Behavior

What should have happened?

### Actual Behavior

What actually happened?

### Root Cause

What caused it?

### Fix

How was it fixed?

### Lesson

What did this teach me?
```

## Claude Code Session Template

Use this before starting a Claude Code session.

```markdown
## Claude Code Session — [Date]

### Milestone

Which roadmap milestone am I working on?

### Context to Provide Claude

- Relevant docs:
- Relevant files:
- Current bug or task:
- Constraints:
- What I want to learn:

### Prompt

[Paste the exact Claude Code prompt used]

### Output Review

Did I understand the output?

Did the code follow the architecture?

Did it introduce unnecessary complexity?

Did it use correct types?

Did it require tests?

### Follow-Up Actions

-
-
-
```

## Weekly Review Template

Use this once per week.

```markdown
## Weekly Review — Week of [Date]

### What I Built This Week

-
-
-

### Biggest Technical Lesson

### Biggest Product Lesson

### Biggest Challenge

### What I Avoided or Deferred

### Quality of My Code This Week

Rate 1–10:

Why?

### Quality of My Understanding This Week

Rate 1–10:

Why?

### Next Week Priorities

1.
2.
3.
```

## Final Rule

This journal is not for performative note-taking.

It is for becoming a better engineer.

Every entry should help future-you answer:

> What did I learn while building Walris?
