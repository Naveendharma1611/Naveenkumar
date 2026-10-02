# Security Report — Phase 1

Covers the security model after migration `supabase/migrations/0001_security_hardening.sql` and
the `grade-submission` Edge Function. Read `AUDIT.md` first for what Phase 0 found.

## ⚠️ Live verification status

I could not run live penetration tests against your actual Supabase project for this phase. Two
separate blockers, both worth knowing about:

1. **The project currently has no application tables at all.** Querying `profiles`, `topics`,
   `questions`, `test_cases`, and `submissions` via the REST API all return
   `PGRST205: Could not find the table 'public.<name>' in the schema cache` — i.e. the schema
   doesn't exist in this project right now, even though you reached a working login screen earlier
   in this project's life. I don't have a way to inspect your dashboard directly, so I can't tell
   you *why* (a few real possibilities: `schema.sql` was run against a different project than the
   one `.env` now points to, the free-tier project paused from inactivity and something didn't come
   back cleanly, or a reset happened) — but whatever the cause, **this needs to be resolved before
   any of Phase 1's SQL can be applied or verified.** See "What you need to do" at the bottom.
2. **Throwaway test-account signups hit Supabase's email rate limit** (`over_email_send_rate_limit`)
   when I tried to create two student accounts to prove cross-student isolation live. This is a
   platform-level limit on the default shared SMTP, not something wrong with the app.

Everything below is therefore a **static policy review**: I read every RLS policy, migration
statement and Edge Function line and reasoned through exactly what each role can and cannot do,
with the specific SQL that enforces it. It has not yet been exercised against a running database.
Once you've applied `schema.sql` → `seed.sql` → `migrations/0001_security_hardening.sql` and
deployed the Edge Function, tell me and I'll run the live tests (two throwaway accounts, or
reusing accounts you provide) and update this section with real results.

## Table-by-table access model

| Table | Student (own rows) | Student (others') | Faculty | Admin | Enforced by |
|---|---|---|---|---|---|
| `profiles` | read + update (own row; `role`/`is_admin` locked by trigger) | **read-only** (needed for leaderboard) | read-only | full | `profiles are readable by any signed-in user`, `a student can update their own profile`, `profiles_prevent_self_promotion` trigger |
| `topics` / `questions` | read-only | — | read-only | full (CRUD) | `topics/questions are readable by signed-in users`, `admins manage topics/questions` |
| `test_cases` (sample only) | read-only | — | read-only | full (CRUD) | `test cases are readable by signed-in users`, `admins manage test cases` |
| `hidden_test_cases` | **no policy — default deny** | **no policy — default deny** | **no policy — default deny** | full (CRUD) | `admins manage hidden test cases`; only the Edge Function's service-role key bypasses RLS to read these for grading |
| `submissions` | read own only; **cannot INSERT at all** | — | read own-assigned-department students' | full (read) | policy `read own submissions, assigned students, or admin`; INSERT policy removed entirely — only the service-role key (Edge Function) can write |
| `faculty_departments` | no access | — | read own assignment rows | full (CRUD) | `admins manage faculty assignments`, `faculty can see their own assignments` |
| `admin_activity_log` | no access | — | no access | read + insert own entries (append-only, no update/delete) | `admins can read the activity log`, `admins can write their own activity log entries` |

### Why `profiles` stays broadly readable

A student can read every other student's name/roll-number/department/row. This is intentional,
not an oversight — the leaderboard (`leaderboard` view, built on `profiles` + `solved_questions`)
is a core feature and is meant to show every student's name and score to every other student. If
this needs to be private in some deployment, the leaderboard feature would need to move behind a
view with its own, narrower security-definer function instead of a broad table-read policy — flag
this if you want that for your rollout.

### The hidden-test-cases fix (the headline change)

Before this migration, `test_cases` held both sample and hidden rows with one blanket
"readable by any signed-in user" policy — any student's browser devtools could see every hidden
test's `expected_output`. Migration 0001 moves every `is_sample = false` row into a new
`hidden_test_cases` table with **zero** select policy for `authenticated`/`anon` roles. In Postgres
RLS, no matching policy means the query returns nothing — there's no "allow by default" to opt out
of. The only thing that *can* read that table now is a client holding the **service-role key**
(which bypasses RLS entirely by design), and the only place that key exists is inside the
`grade-submission` Edge Function's environment (`SUPABASE_SERVICE_ROLE_KEY`, injected by the
platform, never sent to the browser).

### Why students can no longer fake a passing submission

Before: a student could call `supabase.from('submissions').insert({..., passed: true})` directly —
the only check was `auth.uid() = student_id`, nothing validated that `passed` was actually true.
After: the INSERT policy for `submissions` is dropped entirely for `authenticated`/`anon`. The
**only** way a row can be inserted now is through the Edge Function's service-role client, which
computes `passed` itself from real Piston judge results before writing the row. A direct
`supabase.from('submissions').insert(...)` call from the browser now fails with a Postgres
"new row violates row-level security policy" error — there is no policy that would allow it.

### Grading architecture trade-off: Piston vs. Pyodide-in-Deno vs. Judge0

The Edge Function needs to run untrusted Python server-side. Three options considered:

- **Pyodide inside the Edge Function (Deno runtime)** — avoids any third-party dependency, but
  Pyodide is a large WASM CPython build designed to load once in a long-lived browser tab and be
  reused; reloading it on every cold-started, time-boxed Edge Function invocation (and running it
  multiple times per submission, once per test case) would be slow and risks hitting Supabase's
  function execution/memory limits. Not chosen.
- **Self-hosted Judge0** — the most "proper" online-judge architecture, but means standing up and
  maintaining another service, which is a meaningful new piece of infrastructure for a student
  project. Documented here as the natural next step if Piston's limits ever become a real problem.
- **Piston (emkc.org/api/v2/piston)** — **chosen.** Free, public, no signup/API key required
  (keeps setup friction at the same level as the rest of this app), purpose-built for exactly this
  (sandboxed per-request code execution, supports Python and many other languages). Trade-off:
  it's a public shared instance with a modest, undocumented-but-real rate limit and no uptime SLA —
  fine for a classroom-scale practice tool, not something to bet a production grading SLA on. If
  this becomes a bottleneck, swapping `runOnPiston()` in `supabase/functions/grade-submission/index.ts`
  for a self-hosted Judge0 call is a contained, one-function change — the rest of the architecture
  (service-role grading, hidden tables, locked-down submissions) doesn't change.

### Rate limiting & input validation (Edge Function)

- Max 1 submission per 5 seconds per student (any question) — returns HTTP 429.
- Max 40 submissions per hour per student — returns HTTP 429.
- `questionId` must be a syntactically valid UUID; `code` must be a non-empty string under 20,000
  characters. Both checked before any DB or judge call.
- Judge output is capped at 20,000 characters before being stored/returned, so a student can't make
  the judge print gigabytes and blow up `submissions.results`.

### admin_activity_log

Logs `create`/`update`/`delete` on questions from the admin question manager (wired into
`AdminQuestionForm.jsx` / `AdminQuestions.jsx`), capturing `admin_id`, `action`, `target_table`,
`target_id`, and a small `details` JSON blob (question title + sample/hidden test case counts).
Append-only — there's no update or delete policy, matching the `submissions` pattern, so the log
can't be edited after the fact even by the admin who wrote it.

### Known gaps carried forward (being transparent, not hiding them)

- `profiles.department` and `profiles.section` are still student-editable on their own row (same
  column-vs-row RLS limitation that `is_admin`/`role` had, now fixed for those two specifically via
  the generated column + trigger). A student could claim a different department to try to dodge a
  faculty assignment. Low severity (it doesn't expose or corrupt anyone else's data), and the right
  long-term fix is Phase 6's "admin manages departments/sections" UI, where department/section
  become admin-set rather than self-reported at signup. Flagging now rather than silently leaving
  it for later.
- "Faculty see their assigned students" is implemented as department-level matching
  (`faculty_departments` + `is_faculty_for()`), not an explicit per-student assignment — simplest
  thing that satisfies the spec today; Phase 6 may want finer-grained (per-section or per-student)
  assignment, which would just mean extending `faculty_departments`/`is_faculty_for()`, not
  redesigning them.
- No promotion UI yet for making someone faculty/admin — still a manual
  `update profiles set role = 'faculty' where roll_number = '...'` run in the SQL editor by whoever
  owns the project (documented in schema.sql). Phase 6 ("create faculty accounts") replaces this.

## What you need to do before this phase is "live"

1. **Figure out why the live project has no tables** (see the blocker above) — most likely re-run
   `supabase/schema.sql` then `supabase/seed.sql` in the SQL Editor for whichever project your
   `.env` actually points at (double-check the URL in `.env` matches the project you're looking at
   in the dashboard).
2. Run `supabase/migrations/0001_security_hardening.sql` in the SQL Editor.
3. Deploy the Edge Function — easiest path without the CLI: Supabase Dashboard → **Edge Functions**
   → **New Function**, name it exactly `grade-submission`, paste in the contents of
   `supabase/functions/grade-submission/index.ts`, deploy. (Or, with the CLI installed and logged
   in: `supabase functions deploy grade-submission`.)
4. Tell me once that's done and I'll run the live verification (cross-student read attempts, a
   direct-insert-forgery attempt, a hidden-test-case read attempt) and fill in real results here.
