# Database schema

PostgreSQL in production (SQLite works for local development). All tables are created by Django migrations (`python manage.py migrate`). Most content models share `created_at` / `updated_at`, and publishable models have an indexed `is_published` flag.

```
User 1──1 StudentProfile
User 1──* Progress *──1 Lesson
User 1──* Bookmark *──1 Lesson
User 1──* LessonNote *──1 Lesson
User 1──* QuizAttempt *──1 Quiz 1──* QuizQuestion

StudyCategory 1──* Course 1──* Lesson 1──* StudyMaterial
StudyCategory 1──* Lesson            (denormalised for /study-materials/<category>/<lesson> URLs)
Course        1──* StudyMaterial
StudyCategory 1──* InterviewQuestion
StudyCategory 1──* Quiz

Project *──* Technology
Project 1──* ProjectImage | ProjectVideo | ProjectCodeSnippet

BlogCategory 1──* BlogPost *──* Tag;  User 1──* BlogPost (author)
SiteProfile (singleton) · Skill · Education · Experience · Achievement · Certificate · ContactMessage
```

## accounts

| Model | Key fields |
|---|---|
| **User** | `email` (unique, login), `full_name`, `role` ADMIN/STUDENT/VISITOR (indexed), `avatar`, Django auth fields. Passwords hashed with Argon2 |
| **StudentProfile** | `user` (1:1), `phone`, `institution`, `course_of_study`, `graduation_year`, `bio`, `interests` |

## portfolio

| Model | Key fields |
|---|---|
| **SiteProfile** | Singleton: name, headline, tagline, bio/about, objective, interests, goals, hero badges, contact info, social links, `photo`, `resume_pdf` |
| **Skill** | `name`, `category`, `description`, admin-controlled `proficiency_label` / optional `proficiency_percent`, `icon`, `order`, `is_featured`. Unique (name, category) |
| **Education** | `degree`, `institution`, years, `score` (percentage/CGPA) |
| **Experience** | `role`, `organization`, `type` (job/internship/freelance/volunteer), dates, `description`, `technologies` |
| **Achievement** | `title`, `description`, `date` |

## projects

| Model | Key fields |
|---|---|
| **Project** | `slug` (unique), `title`, `category` (indexed), `summary`, `cover_image`, M2M `technologies`, Markdown sections (problem statement, objective, dataset, architecture, data flow, implementation, algorithm, training, evaluation, results, future improvements, documentation), `pipeline_steps` (JSON list), `documentation_pdf`, `model_3d` (GLB/GLTF/OBJ), links, `is_featured`, `is_sample`. Index (is_published, category) |
| **Technology** | `name` (unique), `slug` |
| **ProjectImage / ProjectVideo / ProjectCodeSnippet** | FK `project`, media file or URL / code + language, `order` |

## learning

| Model | Key fields |
|---|---|
| **StudyCategory** | `name` (unique), `slug`, `description`, `icon`, `order` |
| **Course** | FK `category`, `title`, `slug`, `level` (Beginner, Intermediate, Advanced, Interview Preparation, Projects, Practice Questions) |
| **Lesson** | FK `course`, FK `category` (auto from course), `title`, `slug` (**unique per category**), `summary`, Markdown `content`, `video_url`, `estimated_minutes`, `order`. Index (course, order) |
| **StudyMaterial** | FK `course` or `lesson`, `kind` (PDF, notes, code, video, slides, dataset), `file` or `external_url`, `is_downloadable`, `requires_login` |
| **InterviewQuestion** | FK `category`, `question`, `short_answer`, `detailed_answer`, `example`, `code`, `interview_tip`, `difficulty` (indexed) |
| **Progress** | FK `user`, FK `lesson` — one row per completed lesson. Unique (user, lesson) |
| **Bookmark** | FK `user`, FK `lesson`. Unique (user, lesson) |
| **LessonNote** | FK `user`, FK `lesson`, `content`. Unique (user, lesson) |

## quizzes

| Model | Key fields |
|---|---|
| **Quiz** | `slug`, `title`, FK `category` (nullable), `difficulty`, `time_limit_minutes`, `show_leaderboard` |
| **QuizQuestion** | FK `quiz`, `type` (MCQ, coding, output, SQL, debugging, theory), `prompt`, `code`, `options` (JSON), `correct_option`, `accepted_answers` (JSON), `explanation`, `points` |
| **QuizAttempt** | FK `user`, FK `quiz`, `started_at`, `submitted_at` (indexed), `answers` (JSON), `score`, `max_score`, `percent`, `timed_out`. Index (quiz, -percent) for leaderboards |

## certificates, blog, contact

| Model | Key fields |
|---|---|
| **Certificate** | `name`, `provider`, `issue_date`, `expiry_date`, `credential_id` (unique, used in `/certificate/<id>`), `credential_url`, `image`, `pdf`, `skills` |
| **BlogPost** | `slug`, `title`, `excerpt`, Markdown `content`, `featured_image`, FK `category`, M2M `tags`, FK `author`, `published_at` (set on first publish, indexed), `is_featured` |
| **BlogCategory / Tag** | `name` (unique), `slug` |
| **ContactMessage** | `name`, `email`, `subject`, `message`, `ip_address`, `user_agent`, `is_read` (indexed) |

JWT refresh-token blacklisting uses the `token_blacklist` tables from SimpleJWT.
