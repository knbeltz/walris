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
