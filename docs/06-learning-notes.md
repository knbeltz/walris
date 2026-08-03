# Walris Learning Notes

**Document:** docs/06-learning-notes.md
**Status:** Living Document

---

## Purpose

This is where I keep the concepts and debugging lessons I actually want to remember from building
Walris — the "what did I learn" content that the engineering journal deliberately doesn't carry
(that stays Session Goal + Work Completed only). New milestones get their own section below.

---

## Milestone 6 — Supabase Setup

### The big picture analogy

The backend was like an office with no filing cabinet — everything it "knew" lived only in memory
while it was running, and vanished when it stopped. Milestone 6 built the filing cabinet
(Supabase/Postgres) and taught the code how to actually put things in it and take them out.

### The pieces, and what each one is for

- **Supabase** — Postgres (the actual database software), hosted for you. Supabase runs the
  servers so I don't have to install and maintain database software myself.
- **SQLAlchemy** — a *translator*. My Python code thinks in objects (`Briefing.title`); the
  database only understands SQL (`INSERT INTO briefings (title) VALUES (...)`). SQLAlchemy
  translates between the two. This category of tool is called an "ORM" (Object-Relational Mapper).
- **psycopg** — SQLAlchemy is the translator, but it doesn't speak over the wire to Postgres
  itself. `psycopg` is the actual "phone" underneath the translator, handling the real network
  conversation in Postgres's native protocol.
- **`engine`** — the standing connection setup: a phone line installed and ready, configured with
  the number to dial (`DATABASE_URL`). Doesn't mean a call is happening, just that the line exists.
- **A "session"** — one individual conversation using that phone line. Pick up the line, have the
  conversation (run queries), hang up. You don't keep one call open forever.
- **`get_db()`** — a librarian: hands over a session when a request needs one, and always takes it
  back and closes it afterward (via `try`/`finally`), success or failure, so connections never leak.
- **`Base`** — the master blueprint template every model class inherits from, so SQLAlchemy knows
  which Python classes represent real database tables.
- **The 7 model files** — each one is the actual blueprint for one table: its columns, their
  types, how it relates to other tables.
- **`TimestampMixin`** — six of the seven tables wanted the identical `created_at`/`updated_at`
  pair. Rather than retyping it six times, it's a reusable stamp mixed into each model.
- **UUID primary keys** — random, unguessable fingerprints instead of sequential numbers (1, 2,
  3...). Nobody can infer how much data exists, or guess at other rows, from a UUID.
- **Foreign keys + cascade delete** — a pointer saying "this row belongs to that one." Cascade
  means deleting the parent automatically deletes everything pointing back to it too — like
  deleting a folder and everything inside it, rather than leaving orphaned files scattered around.
- **JSONB columns** — for the handful of fields that are naturally a list or small flexible
  structure (e.g. "which groups does this affect"), rather than inventing a whole separate table
  just to store a list of tags.
- **Alembic** — version control for the database's *structure*, the same way Git is version
  control for code. Each schema change becomes a "migration" file; replaying all of them in order
  rebuilds the exact same table structure anywhere.
- **`--autogenerate`** — a diffing tool: compares the Python model blueprints against what the
  live database currently looks like, and writes the migration that closes the gap.
- **`GET /health` checking the database** — the difference between confirming a patient is
  physically in the room vs. actually checking for a pulse.
- **Session pooler vs. direct connection** — the database lives on one server either way. Direct
  connection dials it directly; the pooler is a receptionist in front of it managing a shared set
  of open lines. I needed the pooler because this machine's network can't reach the
  direct-connection address (an IPv6-only limitation), not because of anything wrong with the
  database itself.
- **`extra="ignore"` in Settings** — `.env` intentionally documents future config ahead of the
  code that reads it. Without this, any unrecognized env var made the whole app refuse to start —
  a forgiving mailbox instead delivers what it recognizes and quietly sets aside what it doesn't.
- **Excluding `alembic/versions/` from Ruff** — migrations are auto-generated historical records,
  not hand-maintained code, the same way you don't rewrite yesterday's meeting minutes to match
  today's formatting preferences.
- **Allow-listing `Depends()`/`Query()` for Ruff's bugbear rule** — FastAPI's dependency-injection
  pattern calls a function inside an argument's default value, which normally looks like a classic
  bug (a mutable default argument) but is actually the intended API for that framework.

### The debugging saga: what took so long, and how it actually got fixed

**The setup:** connecting the backend to the real database for the first time. A few early
problems were quick to diagnose because each produced a distinct, specific error (a special
character breaking the connection string's format; SQLAlchemy picking the wrong driver by
default; the direct-connection address being unreachable from this network's IPv6 setup). Those
weren't what made this take a long time.

**The actual long saga:** once on the Session pooler, one single error repeated over and over —
"password authentication failed." The password was never actually wrong. I just didn't know that
yet.

**The mistake — guessing instead of testing:** my first instinct was to treat it like the earlier
problems: find a plausible cause, fix it, retry. Reset the password (special characters?).
Failed. Reset again, alphanumeric only (encoding?). Failed. Wait a couple minutes (propagation
delay?). Failed. Three different reasonable-sounding fixes producing the identical failure is a
signal that the *theory* is wrong, not that the details of each attempt need refining — like
getting "this number is disconnected" and trying to dial more carefully three times instead of
ever asking whether your own phone is connected to the network at all.

**The turning point — isolating the failure one layer at a time:** instead of changing another
variable and hoping, I tested each link in the chain separately, from the most basic possible
connection toward the actual failure point:
- Raw connection via `psycopg` directly, nothing else involved → worked.
- The same credentials structured the way the app structures them → worked.
- The app's own ready-to-use connection object → worked.
- Going through Alembic specifically → failed.

This is the technique worth remembering: **isolating a failure by testing each layer
independently**, sometimes called bisecting a problem — instead of guessing at final causes,
repeatedly cut "where could this be" in half until only one place is left. It's like a detective
checking each stage of a delivery (left the sender? reached the local post office? reached the
destination town? reached the actual mailbox?) instead of re-interviewing the same suspect.

**What was actually wrong:** Alembic's setup file wasn't reusing the app's already-working
connection. It took that correct connection info, converted it to plain text, and handed that
text to a separate piece of code that rebuilt a brand-new connection from scratch by re-reading
it. Like reading a correctly-written address out loud to someone who writes it down again from
what they heard, then mails that copy — if anything gets slightly misheard in the retelling, the
letter goes somewhere wrong, even though the original address was fine the whole time.

**The fix:** stop playing telephone. Alembic was changed to directly reuse the exact same
connection object the app already builds — no converting to text and reconstructing it a second
time. Worked immediately. Notably, the exact character-level reason the text version got garbled
was never pinned down — and that was fine. Once you know *where* a problem lives, you don't
always need the precise mechanism to fix it; removing the risky step fixed it regardless of the
exact cause.

**The lesson to keep:** when the third reasonable-sounding fix in a row produces the identical
failure, that's the signal to stop varying inputs and start testing where, specifically, the
behavior changes. The bug is almost never right where the error message points — usually it's one
or two steps upstream, at a handoff between two things that seem like they should behave
identically but don't.
