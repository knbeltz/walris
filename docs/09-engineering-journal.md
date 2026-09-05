# Walris Engineering Journal

**Document:** docs/09-engineering-journal.md
**Version:** 1.0
**Status:** Living Document
**Product:** Walris

This journal starts fresh from 2026-09-02 onward — it does not backfill prior work, which is
already covered in detail in `docs/05-resume-prompt.md`'s per-milestone write-ups. A previous
version of this document (`docs/05-engineering-journal.md`) existed earlier in the project and was
removed once `docs/05-resume-prompt.md` took over as the living document; this one picks the
practice back up at the next available doc number.

---

## Entry Template

```markdown
## Entry [N] — YYYY-MM-DD

### Session Goal



### Work Completed

-
```

## Entry 1 — 2026-09-02

### Session Goal

Begin Milestone 35 (Expo Notifications Setup): give the mobile app the ability to request
notification permission and obtain a real Expo push token.

### Work Completed

- Installed `expo-notifications` and `expo-device`.
- Built `mobile/lib/notifications.ts`'s `registerForPushNotificationsAsync`: gates on
  `Device.isDevice` (push tokens don't work on simulators), checks existing permission before
  re-prompting, requests permission if needed, and returns a real Expo push token once granted.
- Found and fixed a real bug during review: a duplicate denial-check after the permission request
  used the stale pre-request `existingStatus` instead of the post-request `finalStatus`, as two
  separate non-nested `if` statements — meaning a user granting permission for the first time (the
  primary case this feature exists for) was incorrectly reported as having denied it. Confirmed via
  a direct trace of all three cases (fresh allow, fresh deny, returning user already granted), then
  fixed by removing the redundant check.
- Fixed a "physicial" typo.
- Confirmed Milestone 36 (Device Token Registration API) is already fully built — it was completed
  as part of Milestone 21's backend work and live-verified during M22/M23's integration pass, ahead
  of this roadmap position.
- Added the Android notification channel setup (`Notifications.setNotificationChannelAsync`,
  gated on `Platform.OS === 'android'`, `AndroidImportance.MAX`) — kept as standard boilerplate
  even though Android testing itself remains out of scope.
- Wired `registerForPushNotificationsAsync` into `topics.tsx`'s `handleContinue`, called right
  after preferences save successfully (matching `docs/02`'s "after onboarding" guidance), logging
  the token for now — wrapped in its own try/catch so a failure never blocks the user from
  reaching the app.
- Created this journal (`docs/09-engineering-journal.md`), picking the practice back up after the
  original `docs/05-engineering-journal.md` was removed earlier in the project.
- Still outstanding: on-device verification of the permission prompt and token retrieval.

## Entry 2 — 2026-09-04

### Session Goal

Get Milestone 35's on-device verification unblocked and running.

### Work Completed

- Started the backend dev server fresh (`uvicorn`, port 8000) after confirming the LAN IP was
  unchanged and `mobile/.env.local` still pointed at it correctly.
- Hit a real blocker: Expo Go on the test device had auto-updated and refused to open the project,
  first reporting a generic SDK mismatch, then specifically requiring SDK 57 — a 3-version gap
  from the project's SDK 54.
- Upgraded the mobile app's Expo SDK incrementally, one version at a time (54 → 55 → 56 → 57) per
  Expo's own upgrade guidance, rather than jumping straight to 57 — `npm install expo@^X.0.0` →
  `npx expo install --fix` → `npx expo-doctor` → `npx tsc --noEmit` at each step, to isolate
  exactly which version introduced each break.
- Found and fixed two real breaks:
  - SDK 56 dropped `expo-router`'s dependency on `@react-navigation/native` in favor of its own
    internal navigation stack. Switched `ThemeProvider`/`DarkTheme`/`DefaultTheme`/`Theme`
    (`app/_layout.tsx`, `lib/theme.ts`) and the `Router` type, now `ImperativeRouter`
    (`lib/redirectAfterAuth.ts`), to import from `expo-router` directly.
  - SDK 57 pulled in TypeScript 6, which added a stricter diagnostic (TS2882) for side-effect
    imports lacking ambient module declarations, surfaced on `import '@/global.css'`. Fixed by
    restoring `mobile/expo-env.d.ts` (Expo's standard generated, gitignored boilerplate), which
    had gone missing.
- `expo install --fix` also auto-registered `expo-splash-screen` and `expo-status-bar` as explicit
  config plugins in `mobile/app.json`, now required as of SDK 56.
- Landing on SDK 57 also resolved a known Hermes V1 memory regression present in SDK 56 (flagged
  by `expo-doctor`) affecting apps using `react-native-reanimated`/`react-native-worklets`, both
  already dependencies here — fixed for free by the upgrade.
- Verified clean at each intermediate step and at the final SDK 57 state: `npx tsc --noEmit`,
  `npx eslint .`, and `npx expo-doctor`.
- Restarted the Metro dev server after the upgrade; worked through a port collision caused by two
  separate `expo start` processes running at once (mine in the background, plus one already
  running in another terminal) — resolved by settling on a single instance.
- Still outstanding: the on-device permission prompt / token verification itself, now unblocked
  but not yet re-attempted.
