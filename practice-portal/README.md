# NK Practice Portal

A HackerRank-style Python practice site for college students: 10 topics (beginner → intermediate),
auto-graded practice questions, an in-browser code editor, hints/solutions unlocked after 3 failed
attempts, progress tracking, a college leaderboard, and an admin page for faculty to manage
questions and export results.

Student side and admin side both live in this one app; `/admin` is only reachable by accounts with
`profiles.role = 'admin'`. A `faculty` role also exists, scoped to students in its assigned
department(s) (see `SECURITY_REPORT.md`).

## Tech stack

- **React 18 + Vite + Tailwind CSS** — no custom backend server to run yourself.
- **Supabase** (Postgres + Auth + Edge Functions) — stores students, topics, questions, test cases,
  submissions, and grades submissions server-side. Free tier is enough to start.
- **Pyodide** (CPython compiled to WebAssembly) — runs **Run** (sample-test, instant-feedback) code
  client-side in a Web Worker, so an infinite loop freezes only the runner, not the page.
- **Piston** (emkc.org) — the free public judge the **Submit** Edge Function uses to actually grade
  code against hidden test cases server-side (see "How grading works" below).
- **CodeMirror 6** — the in-browser code editor.
- **SheetJS (xlsx)** — client-side Excel export on the admin Students page.

## 1. Create a Supabase project and apply the schema

1. Go to [supabase.com](https://supabase.com), create a free account and a new project.
2. In the project dashboard, open **SQL Editor → New query** and run, **in this order**:
   1. [`supabase/schema.sql`](supabase/schema.sql) — base tables, views, RLS.
   2. [`supabase/seed.sql`](supabase/seed.sql) — 10 topics + 30 sample questions (3 per topic).
   3. [`supabase/migrations/0001_security_hardening.sql`](supabase/migrations/0001_security_hardening.sql)
      — role model (student/faculty/admin), moves hidden test cases server-side-only, locks down
      direct submission writes, adds `admin_activity_log`. **Required** — the app's Submit button
      won't work without this (it calls the Edge Function this migration's RLS changes expect).
   Any further schema changes land as `supabase/migrations/0002_*.sql`, `0003_*.sql`, etc. — numbered,
   in order, never edited after being applied.
3. Deploy the grading Edge Function: **Edge Functions → New Function**, name it exactly
   `grade-submission`, paste in [`supabase/functions/grade-submission/index.ts`](supabase/functions/grade-submission/index.ts), deploy.
   (Or with the Supabase CLI installed and logged in: `supabase functions deploy grade-submission`
   from inside `practice-portal/`.) `SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` are injected by the
   platform automatically — don't set them yourself.
4. Go to **Project Settings → API** and copy the **Project URL** and **anon public** key.
5. In **Authentication → Providers**, Email is enabled by default — that's all this app uses. If you
   don't want students to confirm their email before logging in, turn off "Confirm email" under
   **Authentication → Settings** for faster classroom testing (re-enable it for a real rollout).

## 2. Configure and run the app

```bash
cd practice-portal
cp .env.example .env     # then paste your Supabase URL + anon key into .env
npm install
npm run dev               # http://localhost:5173/practice/
```

The portfolio serves the built portal at `http://localhost:3000/practice/`. To rebuild that integrated copy, run `npm run build` from this directory; Vite outputs to `../frontend/practice/`. The portal keeps its own Supabase authentication and database.

## 3. Create your first admin/faculty account

Sign up normally through the app (`/signup`), then in the Supabase SQL editor run:

```sql
update profiles set role = 'admin' where roll_number = 'YOUR-ROLL-OR-STAFF-ID';
-- or: update profiles set role = 'faculty' where roll_number = '...';
-- then assign a faculty account to a department it can see submissions for:
-- insert into faculty_departments (faculty_id, department)
--   select id, 'CSE' from profiles where roll_number = '...';
```

Reload the app — an **Admin** link now appears in the navbar, with a question manager (per topic:
add/edit/delete questions, sample test cases, and hidden test cases) and a Students page (progress
table + **Export to Excel** button).

## How grading works

- **Run** executes the student's code locally in a Web Worker via Pyodide, against the question's
  *sample* test case(s) only — instant feedback, nothing is saved to the database.
- **Submit** sends the code to the `grade-submission` Edge Function, which runs it against sample
  **and hidden** test cases using the public [Piston](https://github.com/engineer-man/piston) code
  execution API, then writes the graded `submissions` row itself using Supabase's service-role key.

This is a deliberate change from how this app worked before Phase 1: hidden test cases used to live
in a student-readable table and grading ran entirely client-side (documented then as an accepted
MVP trade-off). They're now in a separate `hidden_test_cases` table with **no** RLS policy granting
student/anon access at all — only the Edge Function's service-role key (never shipped to the
browser) can read them — and the `submissions` table has no INSERT policy for students either, so a
direct `supabase.from('submissions').insert(...)` call from the browser can no longer forge a
"passed" result. Full reasoning, the Piston-vs-Pyodide-in-Deno-vs-Judge0 trade-off, and the
exact policy SQL are in [`SECURITY_REPORT.md`](SECURITY_REPORT.md).

## Adding more content

- **As faculty/admin**: use `/admin` in the running app — no SQL needed. Every question needs at
  least one sample test case (shown to students) and at least one hidden test case (used for real
  grading).
- **In bulk**: write more `insert into questions (...) values (...)` /
  `insert into test_cases (...)` / `insert into hidden_test_cases (...)` statements following the
  pattern in `supabase/seed.sql` and run them as a new numbered migration file.

## Project structure

```
practice-portal/
  supabase/
    schema.sql          base tables, views (leaderboard, topic_progress, solved_questions), RLS
    seed.sql             10 topics + 30 sample questions (3 per topic) + test cases
    migrations/          numbered schema changes applied after schema.sql+seed.sql, in order
    functions/
      grade-submission/  Edge Function: grades Submit server-side via Piston, writes submissions
  public/
    pyodide-worker.js  loads Pyodide from CDN, runs sample-test Run attempts off the main thread
  src/
    lib/               supabaseClient.js, pyodideRunner.js (Worker wrapper), adminLog.js
    context/           AuthContext (session/profile), ThemeContext (dark/light, persisted)
    components/        Navbar, CodeEditor, ResultsPanel, DifficultyBadge, Markdown, route guards
    pages/             Login, Signup, Dashboard, TopicPage, QuestionPage, Leaderboard, Profile
    pages/admin/       AdminLayout, AdminQuestions (+ AdminQuestionForm), AdminStudents (Excel export)
AUDIT.md             Phase-by-phase gap list against the full product spec
SECURITY_REPORT.md   Table-by-table RLS model, the grading-architecture trade-off, known gaps
TEST_REPORT.md       Pass/Fail verification log, appended to after every phase
```

## Deployment

This is a static site once built. In this repository, `npm run build` outputs to `../frontend/practice/`, where the portfolio serves it at `/practice/`; Render's static-site configuration also rewrites nested routes to the app entry. Set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` in the hosting provider's build environment and allow the deployed `/practice/` redirect URL in Supabase Auth settings. Never commit `.env`. No portal server process is needed — Supabase remains its backend.
