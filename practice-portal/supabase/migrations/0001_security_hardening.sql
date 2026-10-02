-- Migration 0001 — Security hardening (Phase 1)
--
-- Run this in the Supabase SQL editor AFTER schema.sql + seed.sql have already
-- been applied. It is safe to run once on the existing project.
--
-- What this does:
--   1. Adds a real role model (student / faculty / admin) + section/is_active,
--      replacing the old is_admin-boolean-only model (is_admin is kept as a
--      generated column for backward compatibility with existing code).
--   2. Adds a faculty_departments assignment table + is_faculty_for() so
--      faculty can see only their assigned students' submissions.
--   3. Moves HIDDEN test cases to a new table with NO student-readable RLS
--      policy at all — only the grade-submission Edge Function's service-role
--      key (which bypasses RLS entirely) can read them. test_cases now only
--      ever holds sample (student-visible) rows.
--   4. Removes the ability for students to INSERT submissions directly —
--      only the Edge Function (service role) can write a submissions row now,
--      so a student can no longer forge a "passed: true" result via a direct
--      API call.
--   5. Adds admin_activity_log.
--
-- See SECURITY_REPORT.md for the reasoning and the live tests that verified
-- each of these.

-- ============================================================================
-- 1. Role model
-- ============================================================================
alter table profiles add column if not exists role text;
update profiles set role = case when is_admin then 'admin' else 'student' end where role is null;
alter table profiles alter column role set not null;
alter table profiles alter column role set default 'student';
alter table profiles add constraint profiles_role_check check (role in ('student', 'faculty', 'admin'));

alter table profiles add column if not exists section text;
alter table profiles add column if not exists is_active boolean not null default true;

-- is_admin becomes a generated column derived from role, so any existing code
-- (or a reader of this schema) that still looks at is_admin keeps working,
-- but role is now the single source of truth — you cannot set is_admin
-- directly or have it drift out of sync with role.
alter table profiles drop column is_admin;
alter table profiles add column is_admin boolean generated always as (role = 'admin') stored;

-- is_admin() now reads role instead of the old boolean column. Every existing
-- policy that calls is_admin() keeps working unchanged.
create or replace function is_admin()
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select coalesce((select p.role = 'admin' from public.profiles p where p.id = auth.uid()), false);
$$;

create or replace function is_faculty()
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select coalesce((select p.role = 'faculty' from public.profiles p where p.id = auth.uid()), false);
$$;

-- Extend the self-promotion guard to the new role column (a non-admin can no
-- longer set their own role to 'faculty' or 'admin' via a direct update,
-- same protection the old is_admin trigger gave, now covering role too).
create or replace function prevent_self_promotion()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  if new.role is distinct from old.role and not is_admin() then
    new.role := old.role;
  end if;
  return new;
end;
$$;
-- (trigger `profiles_prevent_self_promotion` already exists from schema.sql
-- and calls this function — no need to recreate it, only the function body.)

-- ============================================================================
-- 2. Faculty assignment — "faculty see their assigned students"
-- ============================================================================
create table if not exists faculty_departments (
  faculty_id uuid not null references profiles(id) on delete cascade,
  department text not null,
  primary key (faculty_id, department)
);
alter table faculty_departments enable row level security;

create policy "admins manage faculty assignments" on faculty_departments
  for all using (is_admin()) with check (is_admin());
create policy "faculty can see their own assignments" on faculty_departments
  for select using (faculty_id = auth.uid());

create or replace function is_faculty_for(target_student_id uuid)
returns boolean
language sql
security definer set search_path = public
stable
as $$
  select exists (
    select 1
    from faculty_departments fd
    join profiles student on student.department = fd.department
    where fd.faculty_id = auth.uid()
      and student.id = target_student_id
  );
$$;

-- ============================================================================
-- 3. Hidden test cases move server-side-only
-- ============================================================================
create table if not exists hidden_test_cases (
  id uuid primary key default gen_random_uuid(),
  question_id uuid not null references questions(id) on delete cascade,
  stdin text not null default '',
  expected_output text not null,
  order_index int not null default 0
);
alter table hidden_test_cases enable row level security;
-- Deliberately NO select policy for authenticated/anon here at all — RLS
-- defaults to deny, so only a service-role key (the Edge Function) or an
-- admin policy below can read this table. Admins can still manage it from
-- the question-editor UI.
create policy "admins manage hidden test cases" on hidden_test_cases
  for all using (is_admin()) with check (is_admin());

-- Move every existing non-sample row out of test_cases into hidden_test_cases.
insert into hidden_test_cases (question_id, stdin, expected_output, order_index)
select question_id, stdin, expected_output, order_index
from test_cases
where is_sample = false;

delete from test_cases where is_sample = false;

-- test_cases now only ever holds sample (student-visible) rows; is_sample is
-- kept (always true going forward) rather than dropped, to avoid touching
-- every call site that still reads it.

-- ============================================================================
-- 4. Submissions can only be written by the Edge Function (service role)
-- ============================================================================
drop policy if exists "a student can insert their own submissions" on submissions;
-- No insert policy for authenticated/anon remains — RLS defaults to deny, so
-- only a service-role key bypasses it. Select stays allowed for the owner,
-- now also for faculty over their assigned students, and for admins.
drop policy if exists "a student can read their own submissions" on submissions;
create policy "read own submissions, assigned students, or admin" on submissions
  for select using (
    auth.uid() = student_id or is_admin() or is_faculty_for(student_id)
  );

-- Let faculty read assigned students' profiles too (the admin-student list /
-- a future faculty dashboard needs this; the existing broad "any signed-in
-- user can read any profile" policy already covers it, so no change needed
-- there — see SECURITY_REPORT.md for why that policy stays broad).

-- ============================================================================
-- 5. admin_activity_log
-- ============================================================================
create table if not exists admin_activity_log (
  id uuid primary key default gen_random_uuid(),
  admin_id uuid not null references profiles(id) on delete cascade,
  action text not null,
  target_table text not null,
  target_id uuid,
  details jsonb not null default '{}',
  created_at timestamptz not null default now()
);
create index if not exists admin_activity_log_admin_idx on admin_activity_log(admin_id);
alter table admin_activity_log enable row level security;

create policy "admins can read the activity log" on admin_activity_log
  for select using (is_admin());
create policy "admins can write their own activity log entries" on admin_activity_log
  for insert with check (is_admin() and admin_id = auth.uid());
-- No update/delete policy — append-only audit log, same pattern as submissions.
