-- NK Practice Portal — database schema
-- Run this once in the Supabase SQL editor (Project -> SQL Editor -> New query),
-- on a fresh Supabase project, before running seed.sql.

-- ============================================================================
-- 1. profiles — one row per student/faculty, linked 1:1 to Supabase auth.users
-- ============================================================================
create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null,
  roll_number text not null,
  department text not null,
  is_admin boolean not null default false,
  created_at timestamptz not null default now()
);

-- Auto-create a profile row right after someone signs up, from the metadata
-- passed to supabase.auth.signUp({ options: { data: {...} } }) in the app.
create or replace function handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, roll_number, department)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'full_name', 'Student'),
    coalesce(new.raw_user_meta_data->>'roll_number', ''),
    coalesce(new.raw_user_meta_data->>'department', '')
  );
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function handle_new_user();

-- Lets a RLS policy check "is the current user an admin" without recursive
-- self-reference problems on the profiles table.
create or replace function is_admin()
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select coalesce((select p.is_admin from public.profiles p where p.id = auth.uid()), false);
$$;

-- The update policy below lets a student update their OWN profile row, but
-- RLS only restricts which ROWS a policy allows, not which COLUMNS — without
-- this guard a student could call the Supabase client directly and set
-- is_admin = true on themselves. Non-admins silently keep their old
-- is_admin value no matter what they send.
create or replace function prevent_self_promotion()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  if new.is_admin is distinct from old.is_admin and not is_admin() then
    new.is_admin := old.is_admin;
  end if;
  return new;
end;
$$;

drop trigger if exists profiles_prevent_self_promotion on profiles;
create trigger profiles_prevent_self_promotion
  before update on profiles
  for each row execute function prevent_self_promotion();

-- ============================================================================
-- 2. topics — the 10 learning levels, in order
-- ============================================================================
create table if not exists topics (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null,
  order_index int not null,
  explanation text not null,       -- markdown
  example_code text not null,      -- python
  example_output text not null default '',
  created_at timestamptz not null default now()
);

-- ============================================================================
-- 3. questions — 3+ practice questions per topic, easy -> medium -> hard
-- ============================================================================
create table if not exists questions (
  id uuid primary key default gen_random_uuid(),
  topic_id uuid not null references topics(id) on delete cascade,
  title text not null,
  prompt text not null,            -- markdown problem statement
  difficulty text not null check (difficulty in ('easy', 'medium', 'hard')),
  points int not null default 10,
  starter_code text not null default '',
  hint text not null default '',
  solution_code text not null default '',
  order_index int not null default 0,
  created_at timestamptz not null default now()
);

-- ============================================================================
-- 4. test_cases — stdin/expected-stdout pairs used to auto-grade a question.
--    is_sample = true  -> shown to the student on the question page up front.
--    is_sample = false -> "hidden": not shown until after a Run/Submit, then
--                          revealed with expected vs actual (see README for
--                          the client-side-grading trade-off this implies).
-- ============================================================================
create table if not exists test_cases (
  id uuid primary key default gen_random_uuid(),
  question_id uuid not null references questions(id) on delete cascade,
  stdin text not null default '',
  expected_output text not null,
  is_sample boolean not null default false,
  order_index int not null default 0
);

-- ============================================================================
-- 5. submissions — every Run/Submit attempt, used for grading history,
--    hint/solution unlocking (3 failed attempts) and the leaderboard/streak.
-- ============================================================================
create table if not exists submissions (
  id uuid primary key default gen_random_uuid(),
  student_id uuid not null references profiles(id) on delete cascade,
  question_id uuid not null references questions(id) on delete cascade,
  code text not null,
  passed boolean not null,
  is_submit boolean not null default true,   -- false = "Run" (not graded as an attempt), true = "Submit"
  results jsonb not null default '[]',       -- [{stdin, expected, actual, passed}, ...]
  attempt_number int not null default 1,
  created_at timestamptz not null default now()
);

create index if not exists submissions_student_idx on submissions(student_id);
create index if not exists submissions_question_idx on submissions(question_id);

-- ============================================================================
-- 6. Views: per-student solved questions, topic progress and leaderboard
-- ============================================================================

-- First passing SUBMIT per student/question (distinct solve), with its points.
create or replace view solved_questions as
select distinct on (s.student_id, s.question_id)
  s.student_id, s.question_id, q.topic_id, q.points, s.created_at as solved_at
from submissions s
join questions q on q.id = s.question_id
where s.passed = true and s.is_submit = true
order by s.student_id, s.question_id, s.created_at asc;

create or replace view leaderboard as
select
  p.id as student_id,
  p.full_name,
  p.roll_number,
  p.department,
  coalesce(sum(sq.points), 0) as score,
  count(sq.question_id) as solved_count
from profiles p
left join solved_questions sq on sq.student_id = p.id
group by p.id, p.full_name, p.roll_number, p.department
order by score desc, solved_count desc;

create or replace view topic_progress as
select
  p.id as student_id,
  t.id as topic_id,
  t.slug as topic_slug,
  count(distinct q.id) as total_questions,
  count(distinct sq.question_id) as solved_questions
from profiles p
cross join topics t
left join questions q on q.topic_id = t.id
left join solved_questions sq on sq.topic_id = t.id and sq.student_id = p.id
group by p.id, t.id, t.slug;

-- ============================================================================
-- 7. Row Level Security
-- ============================================================================
alter table profiles enable row level security;
alter table topics enable row level security;
alter table questions enable row level security;
alter table test_cases enable row level security;
alter table submissions enable row level security;

-- profiles: everyone can read every profile (needed for the leaderboard /
-- admin student list); a student can only update their own row; only an
-- admin can change is_admin (handled in the app layer — see README).
create policy "profiles are readable by any signed-in user" on profiles
  for select using (auth.role() = 'authenticated');
create policy "a student can update their own profile" on profiles
  for update using (auth.uid() = id);

-- topics / questions / test_cases: readable by any signed-in user (there is
-- no server here, so "hidden" means "not shown in the UI until you submit",
-- not cryptographically secret — see README).
create policy "topics are readable by signed-in users" on topics
  for select using (auth.role() = 'authenticated');
create policy "questions are readable by signed-in users" on questions
  for select using (auth.role() = 'authenticated');
create policy "test cases are readable by signed-in users" on test_cases
  for select using (auth.role() = 'authenticated');

-- only admins can write topics/questions/test_cases (the admin question manager).
create policy "admins manage topics" on topics for all using (is_admin()) with check (is_admin());
create policy "admins manage questions" on questions for all using (is_admin()) with check (is_admin());
create policy "admins manage test cases" on test_cases for all using (is_admin()) with check (is_admin());

-- submissions: a student can insert/read their own; admins can read all.
create policy "a student can insert their own submissions" on submissions
  for insert with check (auth.uid() = student_id);
create policy "a student can read their own submissions" on submissions
  for select using (auth.uid() = student_id or is_admin());

-- To promote the first faculty/admin account, run this once in the SQL
-- editor after that person has signed up through the app:
--   update profiles set is_admin = true where roll_number = 'FACULTY-ID';
