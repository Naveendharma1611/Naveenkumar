# API reference

Base URL: `http://localhost:8000/api/`. JSON everywhere. Auth: `Authorization: Bearer <access>` (the Next.js proxy adds it from the httpOnly cookie).

**Errors** always look like `{"detail": "Human readable message", "errors": {"field": ["message"]}}`.
**Lists** are paginated: `{"count", "next", "previous", "results"}` with `?page=` and `?page_size=` (max 100), except where noted.
**Filtering / search / ordering:** `?field=value`, `?search=text`, `?ordering=-created_at`.

Permissions: **Public** = anyone · **Auth** = any logged-in user · **Student** = STUDENT or ADMIN · **Admin** = ADMIN.
Content endpoints are public for reading **published** items; admins can read unpublished items and create/update/delete (POST/PUT/PATCH/DELETE).

## Authentication — `/auth/`

| Method | Path | Access | Notes |
|---|---|---|---|
| POST | `auth/register/` | Public | `{email, full_name, role: STUDENT\|VISITOR, password, password_confirm}` → `{user, access, refresh}` |
| POST | `auth/login/` | Public | `{email, password}` → `{user, access, refresh}`. Throttled 10/min |
| POST | `auth/refresh/` | Public | `{refresh}` → `{access, refresh}` (rotating) |
| POST | `auth/logout/` | Public | `{refresh}` → 204, blacklists the token |
| GET/PATCH | `auth/me/` | Auth | Profile; PATCH `{full_name, student_profile: {...}}` |
| POST | `auth/upgrade-to-student/` | Auth | Visitor → Student; returns new tokens |
| POST | `auth/change-password/` | Auth | `{current_password, new_password}` |
| POST | `auth/password-reset/` | Public | `{email}`; always 200. Throttled 5/hour |
| POST | `auth/password-reset/confirm/` | Public | `{uid, token, new_password}` |

Access tokens carry `role` and `name` claims.

## Portfolio

| Method | Path | Notes |
|---|---|---|
| GET/PATCH | `profile/` | Site owner profile (singleton). PATCH: Admin |
| GET | `resume/` | Profile + education + experience + grouped skills + featured projects + certificates + achievements |
| GET | `stats/` | Counts of published projects, certifications, skills, lessons |
| CRUD | `skills/` | Not paginated. Filter `category`, `is_featured` |
| CRUD | `education/`, `experience/`, `achievements/` | Not paginated |

## Projects

| Method | Path | Notes |
|---|---|---|
| CRUD | `projects/` , `projects/{slug}/` | Filter `category`, `category__in`, `is_featured`, `technologies__slug`; search title/summary/technology. Write `technology_names: [..]` |
| GET | `technologies/` | Not paginated |

## Learning

| Method | Path | Access | Notes |
|---|---|---|---|
| CRUD | `study/categories/`, `study/categories/{slug}/` | Public / Admin | List has `lesson_count`, `course_count`; detail includes courses → lessons + materials |
| CRUD | `study/courses/{slug}/` | Public / Admin | Filter `category__slug`, `level` |
| CRUD | `study/lessons/{id}/` | Public / Admin | Admin CRUD by id |
| GET | `study/lesson/{category}/{lesson}/` | Public | Lesson with `previous`, `next`, `course_lessons`, and `user_state` when logged in |
| CRUD | `study/materials/` | Public / Admin | Files hidden when `requires_login` and anonymous |
| POST | `study/progress/` | Student | `{lesson, completed}` |
| GET/POST | `study/bookmarks/` | Student | POST `{lesson}` toggles |
| PUT | `study/notes/` | Student | `{lesson, content}` |
| GET | `student/dashboard/` | Student | Progress per category, counts, average quiz score, recent activity |
| GET | `student/quiz-attempts/` | Student | Own submitted attempts |
| GET | `interview/categories/` | Public | Categories with `question_count` |
| CRUD | `interview/questions/` | Public / Admin | Filter `category__slug`, `difficulty`; search |

## Quizzes

| Method | Path | Access | Notes |
|---|---|---|---|
| CRUD | `quizzes/`, `quizzes/{slug}/` | Public / Admin | Detail includes questions **without answers** |
| POST | `quizzes/{slug}/start/` | Student | → `{attempt_id, started_at}` |
| POST | `quizzes/{slug}/submit/` | Public | `{attempt_id?, answers: {questionId: answer}}` → score, percent, per-question results + explanations. Saved only with a valid student attempt |
| GET | `quizzes/{slug}/leaderboard/` | Public | Top 10 best scores (first names only) |
| CRUD | `quiz-questions/` | Admin | Includes answers |

Grading: MCQ compares the option index; text questions compare against `accepted_answers` (case/whitespace-insensitive). Questions without accepted answers are self-review and not scored.

## Certificates, blog, contact, search, admin

| Method | Path | Access | Notes |
|---|---|---|---|
| CRUD | `certificates/`, `certificates/{credential_id}/` | Public / Admin | Not paginated |
| CRUD | `blog/posts/`, `blog/posts/{slug}/` | Public / Admin | Filter `category__slug`, `tags__slug`; write `category_id`, `tag_names` |
| CRUD | `blog/categories/` · GET `blog/tags/` | Public / Admin | |
| POST | `contact/` | Public | `{name, email, subject, message, website (honeypot), elapsed_ms}`. Throttled 5/hour |
| GET | `search/?q=` | Public | Grouped results across projects, courses, lessons, interview questions, blog, certificates |
| GET | `admin/overview/` | Admin | Dashboard counts |
| GET/PATCH/DELETE | `admin/users/` | Admin | Filter `role`, `is_active`; search |
| GET/PATCH/DELETE | `admin/messages/` | Admin | Contact messages; filter `is_read` |
| GET | `health/` | Public | `{"status": "ok"}` |
