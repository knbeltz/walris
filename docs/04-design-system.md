# Walris Design System

**Document:** docs/04-design-system.md
**Version:** 1.0
**Status:** Draft
**Product:** Walris
**Platform:** iOS & Android

---

## 1. Design Direction

Walris should feel like:

> A modern financial newsroom with the authority of a legacy institution.

The visual style is:

- Modern
- Minimalist
- Editorial
- Trustworthy
- Data-rich
- Calm
- Professional

The interface should make complex economic information feel clear, structured, and readable.

Walris should not feel like a noisy trading app.

It should feel like the user is reading a premium economic briefing.

## 2. Brand Personality

Walris should communicate:

- Trust
- Intelligence
- Clarity
- Calm authority
- Historical depth
- Modern speed

The app should avoid:

- Meme finance aesthetics
- Overly aggressive trading colors
- Excessive animations
- Crowded dashboards
- Gamified investing visuals

Walris is not Robinhood.

Walris is closer to: Financial Times, Bloomberg, The Economist, Reuters, FRED — but redesigned
for a mobile-first, AI-assisted economic briefing experience.

## 3. Core Design Principle

Every visual decision should support one goal:

> Help users understand today's economy in under five minutes.

This means:

- Strong visual hierarchy
- Clear event cards
- Calm spacing
- Readable summaries
- Minimal noise
- High trust
- Data that is easy to scan

## 4. Color System

### 4.1 Primary Colors

```text
background: #f8f9ff
surface: #f8f9ff
surface-container-lowest: #ffffff
on-surface: #0b1c30
primary: #000000
on-primary: #ffffff
primary-container: #131b2e
```

Use these for: App background, main text, primary buttons, event cards, main navigation elements.

### 4.2 Surface Colors

```text
surface-dim: #cbdbf5
surface-bright: #f8f9ff
surface-container-low: #eff4ff
surface-container: #e5eeff
surface-container-high: #dce9ff
surface-container-highest: #d3e4fe
surface-variant: #d3e4fe
```

Use these for: Card backgrounds, subtle content blocks, section containers, detail page panels,
empty states.

### 4.3 Text Colors

```text
on-surface: #0b1c30
on-surface-variant: #45464d
inverse-on-surface: #eaf1ff
on-background: #0b1c30
```

Usage:

- `on-surface`: primary text
- `on-surface-variant`: secondary text
- `inverse-on-surface`: text on dark backgrounds
- `on-background`: default page text

### 4.4 Functional Colors

```text
secondary: #006c49
on-secondary: #ffffff
secondary-container: #6cf8bb
on-secondary-container: #00714d

tertiary-container: #410004
on-tertiary-container: #ef4444

error: #ba1a1a
error-container: #ffdad6
on-error-container: #93000a
```

Use functional colors carefully.

**Green** — Use green for: positive economic surprise, improving indicators, soft landing
signals, positive trend direction, successful status.

**Red** — Use red for: negative surprise, economic stress, critical volatility, error states,
warning summaries.

Do not use green and red merely for decoration.

## 5. Typography

Walris uses three typefaces: Libre Caslon Text, Inter, JetBrains Mono.

This creates a balance between: editorial authority, interface clarity, technical precision.

### 5.1 Headline Font

**Font:** Libre Caslon Text

Use for: App title, daily briefing title, section headers, event detail headlines, editorial
summaries.

Typography tokens:

```text
display-lg:
  fontSize: 48px
  fontWeight: 700
  lineHeight: 56px
  letterSpacing: -0.02em

display-lg-mobile:
  fontSize: 36px
  fontWeight: 700
  lineHeight: 42px
  letterSpacing: -0.02em

headline-md:
  fontSize: 32px
  fontWeight: 600
  lineHeight: 40px

headline-sm:
  fontSize: 24px
  fontWeight: 600
  lineHeight: 32px
```

### 5.2 Body Font

**Font:** Inter

Use for: Body copy, summaries, labels, interface text, buttons, empty states, error messages.

Typography tokens:

```text
body-lg:
  fontSize: 18px
  fontWeight: 400
  lineHeight: 28px

body-md:
  fontSize: 16px
  fontWeight: 400
  lineHeight: 24px

caption:
  fontSize: 12px
  fontWeight: 500
  lineHeight: 16px
```

### 5.3 Data Font

**Font:** JetBrains Mono

Use for: Actual values, forecast values, previous values, time stamps, percentages, country
codes, economic indicator labels, market-style metadata.

Typography token:

```text
data-label:
  fontSize: 14px
  fontWeight: 500
  lineHeight: 20px
  letterSpacing: 0.02em
```

JetBrains Mono should make economic values easy to compare vertically.

## 6. Spacing System

Walris uses an 8px spacing system.

```text
base: 8px
gutter: 24px
margin-mobile: 16px
margin-desktop: 40px
container-max: 1280px
```

Recommended mobile spacing:

```text
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
2xl: 40px
3xl: 48px
```

Rules:

- Use generous whitespace around editorial summaries.
- Use tighter spacing inside compact data blocks.
- Keep card padding consistent.
- Avoid dense dashboards in V1.
- Prioritize mobile readability.

## 7. Layout System

Walris is phone-first.

### 7.1 Mobile

Breakpoint: < 600px
Grid: 4 columns
Margin: 16px

Primary target devices: iPhone SE-size screens, standard iPhones, large iPhones, common Android
phones.

### 7.2 Tablet

Breakpoint: 600px–1024px
Margin: 24px

V1 requirement: Tablet layouts should not break, but Walris does not need a custom tablet
experience.

### 7.3 Desktop / Future Web

Breakpoint: > 1024px
Margin: 40px
Max container width: 1280px

Desktop is not part of V1.

## 8. Shape System

Walris uses rounded corners to soften data-heavy layouts.

```text
sm: 0.25rem
default: 0.5rem
md: 0.75rem
lg: 1rem
xl: 1.5rem
full: 9999px
```

Usage:

```text
Buttons: 8px
Inputs: 8px
Cards: 12px
Modals: 12px
Chips: full pill
```

Event cards should feel structured but not harsh.

## 9. Elevation & Depth

Walris should use subtle elevation. Avoid aggressive shadows.

**Level 0 — Background**: `#f8f9ff` — used for app background, main screen background.

**Level 1 — Cards**: white surface, 1px border — used for event cards, news cards, detail
sections.

**Level 2 — Active / Pressed / Hover**: subtle shadow `0px 4px 12px rgba(15, 23, 42, 0.05)` —
used for pressed cards, active states, interactive content.

## 10. Component System

### 10.1 App Screen

Base screen wrapper.

Responsibilities: Safe area handling, background color, horizontal margin, scroll behavior,
bottom spacing.

### 10.2 Daily Briefing Header

Displays: Walris logo/name, current date, briefing title, briefing summary, generated timestamp.

Style: Serif title, calm spacing, editorial feel, minimal decoration.

### 10.3 Event Card

Primary content unit.

Displays: Country, release time, event name, importance score, actual value, forecast value,
previous value, short summary, affected group chips.

Layout:

```text
Country / Time
Event Name
Actual / Forecast / Previous
Summary
Impact Chips
```

Style: White card, 12px radius, subtle border, clear hierarchy, touchable area large enough for
mobile.

### 10.4 Event Data Panel

Used inside event detail pages.

Displays: Actual, Forecast, Previous

Rules:

- Use JetBrains Mono for values.
- Use Inter for labels.
- Highlight meaningful surprise only when available.
- Do not overuse color.

### 10.5 Importance Badge

Displays event importance.

Examples:

```text
★★★★★ Major
★★★★ Significant
★★★ Moderate
★★ Minor
★ Limited
```

Rules:

- Do not make the badge visually overwhelming.
- Importance should help scanability, not dominate the card.

### 10.6 Affected Group Chips

Examples: Homebuyers, Borrowers, Investors, Banks, Consumers, Employers

Style: Pill-shaped, light surface background, small text, comfortable horizontal padding.

### 10.7 News Card

Displays related Marketaux article.

Fields: Publisher, headline, summary, published time, topic or sentiment tag.

Style: 12px radius, subtle border, category label in JetBrains Mono, headline in Libre Caslon
Text, snippet in Inter.

### 10.8 Historical Chart

Used for FRED context.

Rules:

- Keep chart simple.
- Avoid excessive axes or labels.
- Show trend clearly.
- Do not make chart the dominant element.
- Include latest value context.

### 10.9 Empty State

Used when: No briefing exists, no related news exists, no historical data exists.

Tone: Calm, helpful, non-alarming.

Example:

> Today's briefing is not available yet.
> Check back shortly.

### 10.10 Error State

Used when: Backend fails, network request fails, response validation fails.

Tone: Clear, honest, recoverable.

Example:

> We couldn't load today's briefing.
> Please try again.

Include retry action when possible.

## 11. Button System

**Primary Button** — Use for: Retry, Continue, Enable notifications.

```text
background: #000000
text: #ffffff
radius: 8px
```

**Secondary Button** — Use for: Later, Cancel, Open article, View details.

```text
transparent background
1px border
dark text
radius: 8px
```

**Destructive Button** — Use only for: Remove token, Delete setting, Future account deletion.

```text
error color
```

Avoid destructive actions in V1 unless necessary.

## 12. Notification Permission UI

When asking for notifications, do not show the system prompt immediately on first app open.

Recommended flow:

```text
User opens app
  ↓
User views briefing
  ↓
App explains value of notifications
  ↓
User taps Enable Morning Briefing
  ↓
System notification prompt appears
```

Copy example:

> **Get the morning briefing**
> Walris can send you one notification each morning with the top economic events to watch.

Buttons: Enable Morning Briefing, Maybe Later

## 13. Content Style

Walris writing should be: Clear, concise, calm, trustworthy, non-hype, non-partisan, financially
responsible.

Avoid:

- "Markets will crash"
- "This guarantees"
- "You should buy"
- "This is bullish"
- "This is bearish"

Prefer:

> This may increase pressure on the Federal Reserve to keep rates elevated.

instead of:

> This means stocks are doomed.

## 14. Data Display Rules

Economic values should be displayed consistently.

Examples:

```text
Actual: 3.1%
Forecast: 2.9%
Previous: 3.0%
```

Rules:

- Always label actual, forecast, and previous.
- Do not show unlabeled values.
- Use consistent decimal precision.
- Preserve the unit from source data.
- If a value is missing, show "—" rather than fake data.
- Do not infer values on the frontend.

## 15. Color Usage for Data

Use color only when meaning is clear.

Green can indicate: Better-than-expected result, improving trend, positive surprise.

Red can indicate: Worse-than-expected result, deteriorating trend, negative surprise.

Neutral color should be used when: The meaning is ambiguous, higher/lower is not inherently good
or bad, the app cannot confidently classify the event.

Example: Higher CPI may be "red" from an inflation perspective, but not every higher value is
automatically negative. The backend should provide semantic interpretation when possible.

## 16. Accessibility Requirements

Walris should support: Readable font sizes, strong color contrast, large touch targets, screen
reader labels, avoiding color-only meaning, reduced motion compatibility.

Minimum touch target: 44px height

Do not rely on red/green alone to communicate economic meaning.

Use labels such as: Above forecast, Below forecast, In line with forecast.

## 17. Mobile Responsiveness

V1 should prioritize phones.

Test on: Small iPhone, standard iPhone, large iPhone, common Android phone.

Rules:

- Cards should not overflow horizontally.
- Long event names should wrap gracefully.
- Chips should wrap onto multiple lines.
- Charts should resize to screen width.
- Event detail pages should scroll naturally.

## 18. NativeWind Implementation Guidance

Use NativeWind for Tailwind-style utility classes.

However:

- Do not hardcode random colors.
- Prefer theme tokens.
- Avoid one-off spacing unless justified.
- Keep repeated patterns in components.

Example: `EventCard`, `DailyBriefingHeader`, `NewsArticleCard`, `AppScreen` should own repeated
design logic.

## 19. React Native Reusables Guidance

Use React Native Reusables for shadcn-like primitives where helpful.

Recommended primitives: Button, Card, Badge, Separator, Sheet / Modal (later), Input (later).

Avoid over-customizing primitives early.

The goal is consistency, not novelty.

## 20. Screen Design Requirements

### Home Screen

Must communicate: **What matters today?**

Required sections: App header, date, daily summary, top 5 events, notification CTA if not
enabled.

### Event Detail Screen

Must communicate: **Why does this event matter?**

Required sections: Event title, actual/forecast/previous, importance explanation, plain-English
summary, historical context, news context, affected groups, related articles.

## 21. Visual Hierarchy

Use this hierarchy:

1. Briefing title
2. Event names
3. Plain-English summaries
4. Actual / forecast / previous values
5. Context sections
6. Metadata

Do not let metadata overpower the explanation.

The user should understand the event before studying the numbers.

## 22. Design QA Checklist

Before shipping any screen, verify:

- Does the screen feel calm?
- Is the main action obvious?
- Can the user understand the content quickly?
- Are the numbers labeled?
- Does the layout work on small phones?
- Are loading and error states present?
- Are touch targets large enough?
- Does the design match the Walris brand?

## 23. Summary

The Walris design system should create a product that feels: Serious, editorial, modern,
trustworthy, fast, understandable.

The product should not feel like a trading dashboard.

It should feel like a premium economic briefing designed for mobile.

The design system succeeds if users can open Walris, scan the top events, and understand the
economy without feeling overwhelmed.
