# Phase 0 Audit — NK Practice Portal vs. full spec

Audited by reading every file in `src/`, `supabase/schema.sql`, `supabase/seed.sql` against the
8-phase spec. Status legend: ✅ exists · 🟡 partial · ❌ missing.

## Security check (required by Phase 0)

✅ **Only the anon/publishable key is used in the frontend.** `src/lib/supabaseClient.js` reads
only `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY`. Grepped the whole `src/` tree for
`service_role`/`SERVICE_ROLE` — zero matches. No service-role key is shipped to the client anywhere.

## What exists (built in earlier sessions)

- **Auth & profiles**: signup/login (name, roll number, department), `profiles` table, a trigger
  that creates the profile row from signup metadata, and a trigger that blocks non-admins from
  setting `is_admin` on themselves via a direct client update (a real privilege-escalation bug
  that was caught and fixed when this was written).
- **Content**: 10 topics, 3 questions each (30 total, easy/medium/hard), 120 test cases (1 sample +
  2-4 hidden per question). Every solution was executed against every test case in a real Python
  interpreter when this was built — verified again below, still true.
- **Student flow**: topic list with progress bars, topic page (explanation + example + question
  list), question page with a CodeMirror editor, Run (sample tests only, client-side Pyodide) and
  Submit (all tests, client-side Pyodide, writes a `submissions` row), hint/solution unlock after 3
  failed submits, results panel with expected vs actual.
- **Progress & leaderboard**: `leaderboard`, `topic_progress`, `solved_questions` SQL views; a
  Profile page with score/solved-count/day-streak (streak computed client-side from submission
  dates).
- **Admin**: per-topic question + test-case CRUD (`AdminQuestions`/`AdminQuestionForm`), a student
  progress table with client-side Excel export (`AdminStudents`, via the `xlsx` package).
- **Theming**: dark/light toggle persisted to `localStorage`.
- **Grading architecture**: 100% client-side Pyodide in a Web Worker, with a hard timeout that
  terminates + replaces the worker (so an infinite loop can't freeze the page). This is the thing
  Phase 1 of the new spec requires changing — see AUDIT and SECURITY_REPORT below.

## Bugs found during this audit

None beyond the already-fixed self-promotion issue. `npm run build` still succeeds cleanly
(re-verified as part of this audit).

## Gap list against the new 8-phase spec

### Phase 1 — Security
- ❌ **RLS does not distinguish faculty from admin.** Only `is_admin` (boolean) exists; there is no
  `faculty` role, no "faculty sees their assigned students" concept, and no `admin_activity_log`.
- ❌ **Hidden test cases are readable by any authenticated student** via `test_cases` with
  `is_sample = false` — this was a documented, deliberate trade-off for a backend-less MVP, but the
  new spec explicitly requires fixing it with server-side grading.
- ❌ **Grading runs 100% client-side** — nothing stops a student from reading Supabase responses in
  devtools, or from calling `supabase.from('submissions').insert(...)` directly with a forged
  `passed: true` (the current INSERT policy only checks `student_id = auth.uid()`, not who computed
  `passed`).
- ❌ No rate limiting on submissions.
- ❌ No input validation beyond HTML `required` attributes and the DB's `difficulty` check constraint.
- ❌ No `admin_activity_log`.

### Phase 2 — Content
- 🟡 30 questions exist (3/topic), spec wants 100 (10/topic: 4 easy/4 medium/2 hard).
- ❌ No MCQs, no fill-in-the-blank questions (schema only supports code questions).
- ❌ No per-topic "short notes" / "Try it" examples / "common mistakes" section (topics only have
  one `explanation` + one `example_code`).

### Phase 3 — Learning flow
- ❌ Topics are not locked/gated by score — all topics are open immediately.
- ❌ No "continue where you left off", no bookmarks, no per-question private notes.
- 🟡 Editor is CodeMirror, not Monaco (functionally similar; spec explicitly names Monaco).
- 🟡 Drafts auto-save to `localStorage` (not synced/multi-device). No custom stdin box, font-size
  control, visible error line numbers, or output size limit. The 10s client-side timeout exists
  (`pyodideRunner.js`) but the spec asks for 5s plus an output size cap.

### Phase 4 — Progress & motivation
- 🟡 Basic score/solved/streak exist on Profile; no accuracy %, no weak-topic breakdown, no charts,
  no recent-submissions list.
- ❌ No badges system at all.
- 🟡 One global leaderboard exists; no department/section/weekly leaderboards (there's no `section`
  field on `profiles` yet, and no week-scoped query).

### Phase 5 — Tests & contests
- ❌ Entirely missing: no `tests`/`contests` tables, no faculty test-builder, no timed student test
  mode, no tab-switch detection, no copy/paste blocking, no live contest leaderboard.

### Phase 6 — Faculty & admin
- ❌ No bulk CSV/Excel question upload.
- ❌ Admin cannot view a student's submitted code from a UI (data exists in `submissions`, no page
  for it).
- ❌ No manual marks override, no announcements.
- ❌ No bulk student import, no "create faculty account" flow (promotion is currently a manual SQL
  `update` run by whoever owns the Supabase project).
- ❌ No disable/reset-user actions, no department/section management UI, no branding settings.
- ❌ No plagiarism detection.

### Phase 7 — Reports & extras
- 🟡 Excel export exists for the student leaderboard only; no PDF export, no per-test/class/
  weak-topic reports.
- ❌ No certificates, no `/verify/:id` page.
- ❌ No notifications/announcements, no doubt/discussion threads, no help/FAQ, no feedback form, no
  profile-edit or change-password page (Profile is currently read-only).

### Phase 8 — Final QA
- ❌ No automated tests at all (no Vitest, no Playwright, no test runner configured).
- 🟡 Mobile layout and dark mode exist and look reasonable by design (Tailwind responsive classes
  used throughout) but have not been verified against a real viewport/screen reader in this audit.
- ✅ `npm run build` succeeds with zero errors (re-verified).
- 🟡 README exists and documents setup/env vars/deployment for the current architecture; will need
  updating once Phase 1's grading architecture changes land.

## Plan

Given the size of this gap list, phases will be executed and verified one at a time, each ending in
its own commit, per your instructions. **Phase 1 (Security) is next**, since Phases 2-8 all build on
top of whatever the grading/RLS architecture ends up being.
