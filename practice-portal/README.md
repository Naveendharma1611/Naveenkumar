# NK Practice Portal

A HackerRank-style Python practice site for college students: 10 topics (beginner → intermediate),
3+ auto-graded practice questions each, an in-browser code editor and Python runtime (Pyodide — no
backend execution server), hints/solutions unlocked after 3 failed attempts, progress tracking,
a college leaderboard, and an admin page for faculty to manage questions and export results.

Student side and admin side both live in this one app; `/admin` is only reachable by accounts with
`profiles.is_admin = true`.

## Tech stack

- **React 18 + Vite + Tailwind CSS** — no separate backend server.
- **Supabase** (Postgres + Auth) — stores students, topics, questions, test cases, submissions. Free tier is enough to start.
- **Pyodide** (CPython compiled to WebAssembly) — runs student code entirely in the student's browser, inside a Web Worker so an infinite loop freezes only the runner, not the page.
- **CodeMirror 6** — the in-browser code editor.
- **SheetJS (xlsx)** — client-side Excel export on the admin Students page.

## 1. Create a Supabase project

1. Go to [supabase.com](https://supabase.com), create a free account and a new project.
2. In the project dashboard, open **SQL Editor → New query**, paste the contents of
   [`supabase/schema.sql`](supabase/schema.sql), and run it.
3. In a second query, paste the contents of [`supabase/seed.sql`](supabase/seed.sql) and run it —
   this loads the 10 topics and 30 sample questions (3 per topic).
4. Go to **Project Settings → API** and copy the **Project URL** and **anon public** key.
5. In **Authentication → Providers**, Email is enabled by default — that's all this app uses. If you
   don't want students to confirm their email before logging in, turn off "Confirm email" under
   **Authentication → Settings** for faster classroom testing (re-enable it for a real rollout).

## 2. Configure and run the app

```bash
cd practice-portal
cp .env.example .env     # then paste your Supabase URL + anon key into .env
npm install
npm run dev               # http://localhost:5173
```

## 3. Create your first admin/faculty account

Sign up normally through the app (`/signup`), then in the Supabase SQL editor run:

```sql
update profiles set is_admin = true where roll_number = 'YOUR-ROLL-OR-STAFF-ID';
```

Reload the app — an **Admin** link now appears in the navbar, with a question manager (per topic:
add/edit/delete questions and their test cases) and a Students page (progress table + **Export to
Excel** button).

## How grading works (and an important trade-off to know about)

When a student clicks **Run**, their code executes locally in a Web Worker via Pyodide against the
topic's *sample* test case(s) only — fast feedback, nothing is saved. **Submit** runs the code
against every test case (sample + hidden), records the attempt in `submissions`, and — if all cases
pass — counts the question as solved (adds its points to the leaderboard and topic progress).

Because there is deliberately no backend execution server, grading happens entirely in the
student's own browser: their Supabase session can read every test case's `expected_output` and
every question's `solution_code` (that's how the Pyodide runner and the "show solution" button get
their data). **"Hidden" test cases and the locked solution are a UI convention, not a cryptographic
secret** — a student determined enough to open devtools and query Supabase directly could see them
early. For a learning/practice tool this is a normal, accepted trade-off (the alternative is running
a real grading server, which the brief explicitly avoided). If this ever needs to be exam-grade
tamper-proof, the fix is a Supabase Edge Function that keeps `expected_output`/`solution_code` in a
table only the function's service-role key can read, and have the client send it the code's output
to compare server-side instead.

## Adding more content

- **As faculty**: use `/admin` in the running app — no SQL needed.
- **In bulk**: write more `insert into questions (...) values (...)` / `insert into test_cases (...)`
  statements following the pattern in `supabase/seed.sql` and run them in the SQL editor.

## Project structure

```
practice-portal/
  supabase/
    schema.sql        tables, views (leaderboard, topic_progress, solved_questions), RLS policies
    seed.sql           10 topics + 30 sample questions (3 per topic) + test cases
  public/
    pyodide-worker.js  loads Pyodide from CDN, runs student code against test cases, off the main thread
  src/
    lib/               supabaseClient.js, pyodideRunner.js (Worker wrapper + timeout handling)
    context/           AuthContext (session/profile), ThemeContext (dark/light, persisted)
    components/        Navbar, CodeEditor, ResultsPanel, DifficultyBadge, Markdown, route guards
    pages/             Login, Signup, Dashboard, TopicPage, QuestionPage, Leaderboard, Profile
    pages/admin/       AdminLayout, AdminQuestions (+ AdminQuestionForm), AdminStudents (Excel export)
```

## Deployment

This is a static site once built (`npm run build` → `dist/`) — deploy `dist/` to Netlify, Vercel,
GitHub Pages, or Render's static site hosting, the same way `frontend/` elsewhere in this repo is
deployed. Set the `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY` environment variables in your
hosting provider's dashboard (don't commit `.env`). No server process is needed — Supabase is the
only external service.
