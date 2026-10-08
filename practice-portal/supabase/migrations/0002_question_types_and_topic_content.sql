-- Migration 0002 — Question types (MCQ, fill-in-the-blank) + richer topic content (Phase 2)
--
-- Run this in the Supabase SQL editor AFTER 0001_security_hardening.sql.
--
-- What this does:
--   1. Adds question_type to `questions` ('code' | 'mcq' | 'fill_blank'), with MCQ options/
--      correct_option and fill-blank correct_answer stored directly on the row (not secret —
--      same trade-off as sample test cases; these are quick-check questions, not graded exams).
--   2. Expands `topics` with try_it_examples (multiple runnable examples) and a common_mistakes
--      section, on top of the existing single explanation/example_code/example_output.
--   3. Updates the questions/hidden_test_cases "admins manage" policies implicitly cover the new
--      columns already (policies are row-level, not column-level) — no RLS change needed here.

alter table questions add column if not exists question_type text not null default 'code';
alter table questions add constraint questions_type_check
  check (question_type in ('code', 'mcq', 'fill_blank'));

-- MCQ: options is a JSON array of option strings, correct_option is its 0-based index.
alter table questions add column if not exists options jsonb not null default '[]';
alter table questions add column if not exists correct_option int;

-- Fill-in-the-blank: the expected answer, compared case-insensitively/trimmed.
alter table questions add column if not exists correct_answer text not null default '';

-- code-only columns (starter_code, solution_code, hint) stay as-is and are simply unused/blank
-- for mcq/fill_blank rows; test_cases/hidden_test_cases rows only ever exist for 'code' questions.

alter table topics add column if not exists try_it_examples jsonb not null default '[]';
-- try_it_examples shape: [{ "description": "...", "code": "...", "output": "..." }, ...]
alter table topics add column if not exists common_mistakes text not null default '';
-- common_mistakes is markdown, rendered the same way topics.explanation is.
