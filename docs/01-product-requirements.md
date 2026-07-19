# Walris Product Requirements Specification (PRS)

**Document:** 01-product-requirements-specification.md
**Status:** Draft
**Product:** Walris
**Platform:** iOS & Android
**Author:** Kai Beltz

---

## Part I — Executive Summary & Product Vision

### 1. Executive Summary

#### Product Overview

Walris is a mobile-first economic intelligence platform that helps users understand the world's
most important macroeconomic events in under five minutes per day.

Unlike traditional financial news applications that overwhelm users with hundreds of headlines,
dense economic calendars, and technical jargon, Walris delivers a curated daily briefing that
explains:

- What happened
- Why it matters
- How unusual it is historically
- How financial media is interpreting it
- Who is most affected

Walris is not designed to replace professional financial terminals or real-time trading
platforms. Instead, it serves as an interpretation layer that transforms complex economic
information into concise, trustworthy, and actionable insights.

The initial release focuses on one experience: a daily briefing personalized to the user's
selected category (Investors, Small Business Owners/Entrepreneurs, Consumers, Home Owners/Home
Buyers, Students, Job Seekers, or "I Want Everything"), generated from trusted public data sources
(FRED, Financial Modeling Prep, Marketaux) and enriched with AI-powered explanations.

### 2. Vision Statement

**Vision**

> To become the world's most trusted platform for understanding the economy.

Walris seeks to make macroeconomics accessible without sacrificing depth or accuracy.

Rather than teaching economics through textbooks or reporting isolated news events, Walris
explains how today's economic developments fit into the broader economic narrative.

Over time, Walris aims to become the daily destination where students, professionals, investors,
entrepreneurs, policymakers, and curious citizens begin their day to understand the state of the
economy.

### 3. Mission Statement

**Mission**

> Help anyone understand today's economy in less than five minutes.

The application should reduce the time and expertise required to stay informed about important
economic developments while maintaining a high standard of factual accuracy and clarity.

### 4. Product Philosophy

Walris is built on five guiding principles.

#### 4.1 Clarity Over Complexity

Economic information should become easier to understand—not simplified to the point of being
misleading.

Whenever possible, explanations should use plain language while preserving economic accuracy.

#### 4.2 Context Over Headlines

A number without context has limited value.

Every economic release should answer questions such as:

- Is this historically high or low?
- Was it expected?
- What changed?
- Why is this important?

Users should never have to search elsewhere to understand the significance of an economic event.

#### 4.3 Explanation Over Information

Traditional financial applications primarily deliver information.

Walris delivers explanations.

The objective is not to maximize the number of articles consumed but to maximize user
understanding.

#### 4.4 Trust Before Speed

Accuracy is more important than being the first to publish.

All factual information should originate from authoritative external sources.

Artificial intelligence should explain information—not create facts.

Whenever uncertainty exists, the application should communicate that uncertainty rather than
speculate.

#### 4.5 Simplicity Wins

Every screen should answer a single question.

Every feature should support the product's central objective.

Features that increase complexity without significantly improving understanding should be
postponed until future versions.

### 5. Problem Statement

The modern economic news ecosystem suffers from four primary problems.

#### Problem 1 — Information Overload

Users are presented with:

- Large economic calendars
- Continuous financial news
- Numerous simultaneous market events

Few applications distinguish between events that are truly significant and those that are
routine.

#### Problem 2 — Lack of Context

Most economic releases are presented as isolated statistics.

Example:

> CPI: 3.1%

Without additional context, users cannot determine:

- Whether the value is historically significant
- Whether it exceeded expectations
- Whether it meaningfully changes the economic outlook

#### Problem 3 — Technical Language

Economic reporting frequently assumes prior knowledge.

Terms such as:

- Core CPI
- PCE
- Yield Curve
- Quantitative Tightening
- Hawkish
- Basis Points

are rarely explained for non-specialists.

This creates a high barrier to entry for many potential users.

#### Problem 4 — Fragmented Information

Understanding a single economic event often requires consulting multiple sources:

- Economic calendar
- Historical database
- Financial news outlets
- Market commentary
- Central bank releases

Users must manually synthesize these sources into a coherent understanding.

Walris automates this synthesis.

### 6. Opportunity

There is an opportunity to create a product that sits between traditional financial news
platforms and educational economics resources.

Rather than competing with Bloomberg, Reuters, or Trading Economics on the quantity of
information published, Walris competes on the quality of interpretation.

The product delivers one clear value proposition:

> Explain today's economy faster than anyone else.

### 7. Product Positioning

Walris occupies a unique position within the financial information ecosystem.

| Product | Primary Purpose |
|---|---|
| Bloomberg Terminal | Professional financial terminal |
| Reuters | Breaking financial news |
| Trading Economics | Economic calendar and data |
| Yahoo Finance | Retail investing news |
| FRED | Historical economic data |
| **Walris** | **AI-powered economic understanding** |

Walris complements these platforms rather than replacing them.

### 8. Value Proposition

Walris combines four trusted sources into a single daily briefing.

| Source | Purpose |
|---|---|
| Finnhub | Economic events |
| FRED | Historical context |
| Marketaux | News coverage |
| OpenAI | Interpretation and synthesis |

Together, they answer six questions for every event:

1. What happened?
2. Was it expected?
3. Why does it matter?
4. Is it historically significant?
5. How is the financial media interpreting it?
6. Who is affected?

### 9. Product Principles

Every feature proposed for Walris should satisfy the following principles.

**Principle 1** — A user should understand today's economy in under five minutes.

**Principle 2** — Every event should explain why it matters.

**Principle 3** — Historical context should always accompany important economic releases.

**Principle 4** — Artificial intelligence should explain data—not generate facts.

**Principle 5** — Professional-quality information should be accessible to non-professionals.

**Principle 6** — The interface should reduce cognitive load through clear visual hierarchy,
concise writing, and intentional prioritization.

### 10. MVP Product Definition

Version 1 focuses on a personalized daily briefing:

**Your Economic Briefing**

Users create an account (via Clerk) and select the one category that best describes them:
Investors, Small Business Owners/Entrepreneurs, Consumers, Home Owners/Home Buyers, Students, Job
Seekers, or "I Want Everything." Users may optionally add extra topics on top of their category
(Inflation, Employment and Labor, Economic Growth, Housing, Consumer Costs, Major Market Indices,
Industry Sector Performance, Company Spotlights).

Every morning, Walris generates an individually-tailored briefing for each user, built from:

- Federal Reserve Economic Data (FRED) — the macroeconomic indicators relevant to their category
- Financial Modeling Prep (FMP) — market indices, sector performance, and a notable company
  spotlight
- Marketaux — recent news tied to whichever indicators had fresh coverage that day
- OpenAI — a plain-English explanation synthesizing the above into their personal briefing

Users receive a morning push notification with their briefing. Preferences (category and
additional topics) can be changed anytime from a settings screen.

See `docs/09-personalization-pivot-plan.md` for the full technical plan behind this.

The MVP succeeds if users consistently return because Walris is the fastest way to understand
what matters in the economy — for their specific situation — each morning.

### 11. Long-Term Vision

Walris is designed to evolve beyond a daily briefing application.

Future versions may include:

- Interactive indicator dashboards
- Country-specific economic overviews
- AI-powered question answering
- Educational learning modules
- Weekly and monthly economic reports
- Economic relationship visualizations
- Professional research tools
- Custom alerts and watchlists

Despite future expansion, the core philosophy remains unchanged:

> Help users understand the economy—not simply consume economic information.
