# AI / Data Science Portfolio & Learning Platform

A full-stack portfolio, resume, project showcase and student learning platform for an AI engineer / data scientist / Python developer, with an interactive 3D neural-network hero.

- **Visitors** browse the portfolio, projects, study materials, interview questions and quizzes.
- **Students** also track lesson progress, bookmark lessons, keep notes, save quiz scores and get a learning dashboard.
- **Admins** manage all content (projects, courses, lessons, study files, quizzes, certificates, blog, resume) from the admin panel.

## Tech stack

```
                        FULL STACK
        ┌───────────────┴───────────────┐
     FRONTEND                         BACKEND
 HTML + CSS                        Python
 JavaScript                        Django REST API
                                   Django ORM ──► PostgreSQL / SQLite
```

| Layer | Technology |
|---|---|
| Frontend | `frontend/`: plain HTML pages, one stylesheet, vanilla JavaScript modules (no build step). marked + DOMPurify, highlight.js and model-viewer from CDNs |
| Backend | `backend/`: Django 6, Django ORM, Django REST Framework, SimpleJWT, Django admin |
| Database | PostgreSQL (SQLite fallback for quick local dev) |
| Storage | Local media in development, S3-compatible storage in production (`USE_S3=true`) |

## Architecture

```
Browser ──► frontend/ (static HTML + CSS + JS, e.g. http://localhost:3000)
              │  js/api.js     fetch() wrapper: JWT in localStorage, auto-refresh on 401
              │  js/ui.js      shared header/footer, helpers, cards, form errors
              │  js/pages/*.js one script per page, renders into <main id="app">
              ▼  JSON over HTTPS (CORS)
           backend/ Django REST API (http://localhost:8000/api/)  ──►  Django ORM  ──►  PostgreSQL
              └  /django-admin/   content management UI
```

The backend also still contains a server-rendered version of the site (`backend/apps/web`, served at http://localhost:8000/). It is optional.

## Project structure

```
frontend/
  *.html             28 pages (index, projects, project, study, lesson, quiz, student, admin, ...)
  css/style.css      design system: light/dark theme, layout, components
  js/config.js       API URL (edit PRODUCTION_API_URL before deploying)
  js/api.js          API client + auth token storage
  js/ui.js           layout, helpers, shared components
  js/parts.js        timeline / study-material markup
  js/pages/          one module per page
  serve.py           local dev server on port 3000
backend/
  config/            settings, urls
  apps/<domain>/     models, admin, serializers, API views
  apps/web/          optional server-rendered HTML version of the site
```

## Running locally

Prerequisites: Python 3.12+, Node.js 20.9+, and (recommended) PostgreSQL.

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # macOS/Linux: cp .env.example .env  — then edit it
python manage.py migrate
python manage.py seed_demo      # study categories, skills and 5 clearly-marked sample projects
python manage.py createsuperuser
python manage.py runserver      # http://localhost:8000
```

To use PostgreSQL, set `DATABASE_URL=postgres://user:password@localhost:5432/portfolio` in `backend/.env`. Without it, SQLite is used.

### 2. Frontend

In a second terminal:

```bash
cd frontend
python serve.py                 # http://localhost:3000
```

No Node.js, npm or build step is needed. Keep the Django server running on port 8000: the pages load their data from `http://localhost:8000/api`.

### 3. Log in

- **Admin:** log in at `login.html` with your superuser. You land on `admin.html` (overview, users, messages). Content is edited in the Django admin at `http://localhost:8000/django-admin/`.
- **Students:** register at `register.html`, then track lessons, bookmarks, notes and quiz scores on `student.html`. Visitors can upgrade to a student account on `account.html`.

## Adding your content

Everything is edited in the admin panel — nothing personal is hardcoded.

| What | Where in the admin |
|---|---|
| Your name, headline, photo, bio, links, resume PDF | Portfolio → Site profile |
| Skills (with optional proficiency labels) | Portfolio → Skills |
| Education / Experience / Achievements | Portfolio |
| Projects (screenshots, videos, code, pipeline diagram, 3D model, docs PDF) | Projects → Projects |
| Study materials: Category → Course (level) → Lessons (Markdown) → files | Learning |
| Interview questions | Learning → Interview questions |
| Quizzes (MCQ, coding, output, SQL, debugging, theory) | Quizzes → Quizzes |
| Certificates | Certificates |
| Blog posts | Blog |
| Contact messages | Contact |

Tips:
- Lesson content, project sections and blog posts support Markdown: headings, tables, code blocks (with syntax highlighting), images and links. Raw HTML is not rendered, which keeps pages XSS-safe.
- A project's **pipeline steps** field drives its interactive architecture diagram, e.g. `["Dataset", "Data Cleaning", "EDA", "Model Training", "Evaluation"]`.
- Upload a `.glb` / `.gltf` / `.obj` file on a project to enable the 3D model viewer.
- The 5 seeded projects are flagged **Sample** on the site. Edit or delete them once you add real work.
- Use the **Publish / Unpublish** bulk actions; unpublished items are hidden from the public site.

## Pages

`index` · `about` · `skills` · `experience` · `resume` · `projects` · `project?slug=` · `certifications` · `certificate?id=` · `blog` · `post?slug=` · `study` · `category?c=` · `lesson?c=&l=` · `interview` · `interview-category?c=` · `practice` · `quiz?slug=` · `contact` · `search?q=` · `login` · `register` · `forgot-password` · `reset-password?uid=&token=` · `account` · `student` · `admin` · `404` (all `.html` in `frontend/`)

## Environment variables

**backend/.env** (see `backend/.env.example`): `SECRET_KEY`, `JWT_SECRET`, `DEBUG`, `DATABASE_URL`, `ALLOWED_HOSTS`, `FRONTEND_URL`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `MEDIA_URL`, `MAX_UPLOAD_SIZE_MB`, `ADMIN_URL`, email settings, `USE_S3` + `AWS_*`.

**frontend/js/config.js**: `PRODUCTION_API_URL` (the deployed API address; local development is detected automatically).

## Security

- Passwords hashed with Argon2; Django password validators on register/reset/change.
- JWT access (15 min) + rotating refresh tokens (7 days) with blacklist on logout, kept in the browser's localStorage and refreshed automatically by `frontend/js/api.js`.
- Role-based permissions on every API endpoint; login/role checks on protected pages (`requireLogin()` in `frontend/js/ui.js`).
- CORS allow-list: only the configured frontend origins can call the API from a browser.
- Frontend escapes all API text and sanitises Markdown with DOMPurify (XSS protection).
- Rate limiting: login/register (10/min), password reset and contact form (5/hour), general API limits.
- Uploads: extension allow-lists, size caps and magic-byte checks.
- Security headers on both apps; HSTS, secure cookies and SSL redirect when `DEBUG=false`.
- Contact form spam protection: honeypot field, minimum fill time, throttling.

## Tests

```bash
cd backend && python manage.py test apps       # 22 API tests: auth, roles, learning, quizzes, contact
```

## Deployment

**Backend + database (Render):** `render.yaml` defines the Django service and a PostgreSQL database. Create a Blueprint from the repo, then set `FRONTEND_URL` and `CORS_ALLOWED_ORIGINS` on the API to the frontend's URL (e.g. `https://portfolio-frontend.onrender.com`). `backend/build.sh` installs dependencies, collects static files, migrates and seeds. Railway and AWS work the same way: run `build.sh`, then `gunicorn config.wsgi:application`.

**Frontend (Render static site, Netlify, Vercel or GitHub Pages):** publish the `frontend/` folder as-is. Before deploying, set `PRODUCTION_API_URL` in `frontend/js/config.js` to your API URL. `render.yaml` already includes a static site for it.

**Media files in production:** Render's disk is ephemeral, so set `USE_S3=true` with an S3 / Cloudflare R2 bucket for uploads.

Never commit `.env` files.

## Documentation

- `docs/Full-Stack-Platform-Guide.docx`: complete guide (setup, usage, content, development, deployment, troubleshooting)
- [API reference](docs/API.md)
- [Database schema](docs/DATABASE.md)

## Future improvements

- In-app admin editors (the Django admin covers CRUD today)
- Code execution sandbox for coding questions
- Certificates of completion for students
- Full-text search with PostgreSQL `SearchVector`
