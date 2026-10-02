# Test Report

Running log of verification performed after each phase, Pass/Fail per item. Appended to, never
rewritten, so earlier phases' results stay visible.

## Phase 0 — Audit

| Check | Result | Notes |
|---|---|---|
| `npm run build` succeeds | ✅ Pass | Zero errors/warnings beyond the pre-existing chunk-size notice. |
| Frontend uses only the anon/publishable key | ✅ Pass | Grepped `src/` for `service_role`/`SERVICE_ROLE` — zero matches. Only `VITE_SUPABASE_ANON_KEY` is read, in `src/lib/supabaseClient.js`. |
| Gap list against the 8-phase spec | ✅ Pass | Written to `AUDIT.md`. |
| Bugs found requiring a fix before continuing | ✅ Pass (none found) | The one real bug from earlier (profile self-promotion to admin) was already fixed and re-verified present in `schema.sql`'s `prevent_self_promotion` trigger. |

## Phase 1 — Security

| Check | Result | Notes |
|---|---|---|
| `npm run build` succeeds after all Phase 1 frontend changes | ✅ Pass | 294 modules transformed, zero errors (same pre-existing chunk-size notice as before). |
| Migration SQL reviewed for correctness (role backfill order, generated-column dependency, policy drops/creates) | ✅ Pass | See reasoning in `SECURITY_REPORT.md`. Not yet executed against a live database — see below. |
| Edge Function (`grade-submission/index.ts`) syntax | 🟡 Not independently verified | No Deno runtime available in this environment to run/typecheck it directly; `npm run build` doesn't cover Deno files (they're outside Vite's build). Manually re-read line by line for syntax correctness. **Will re-verify once deployed and callable.** |
| `test_cases`/`hidden_test_cases` split wired into `AdminQuestionForm`/`AdminQuestions` | ✅ Pass (code review) | `npm run build` compiles cleanly; logic manually traced for both create and edit paths. Not exercised against a live admin session. |
| `QuestionPage.jsx` Submit now calls the Edge Function instead of writing `submissions` directly | ✅ Pass (code review) | `handleSubmit` now calls `supabase.functions.invoke('grade-submission', ...)`; `handleRun` is unchanged (still local Pyodide against sample tests only). |
| `ResultsPanel.jsx` handles hidden-test results with no `expected`/`actual` | ✅ Pass (code review) | Added explicit branch for `r.expected === undefined`. |
| Live RLS proof: hidden test cases unreadable by a student | ❌ **Blocked** | Attempted via REST against the live project — every application table (`profiles`, `topics`, `questions`, `test_cases`, `submissions`) currently returns `PGRST205: table not found in schema cache`. The base schema isn't present in this project right now, for reasons I can't diagnose remotely. Nothing in Phase 1 can be live-verified until this is resolved (see `SECURITY_REPORT.md`'s blocker section) and the migration + Edge Function are deployed. |
| Live RLS proof: cross-student submission isolation | ❌ **Blocked** | Same root cause as above, plus hit Supabase's `over_email_send_rate_limit` when trying to create throwaway test accounts. |
| Live RLS proof: forged `submissions` insert is rejected | ❌ **Blocked** | Same root cause. |
| `admin_activity_log` writes on question create/update/delete | 🟡 Not live-verified | Code wired in (`logAdminAction` calls in both admin pages); blocked from live testing for the same reason. |
