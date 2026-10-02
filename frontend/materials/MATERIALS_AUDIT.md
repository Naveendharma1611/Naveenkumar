# Study Materials Audit (Step 1)

Audited by reading every `frontend/materials/*.txt` file directly (module/line counts via script,
not estimated) plus the backend's `StudyCategory` and `quizzes_quiz` tables, since "20 quiz
questions for the existing quiz system" means the separate Django quiz app, not the materials DSL.

## Part A — What exists today, subject by subject

All 21 files build cleanly via `build.py` (verified). "Interview module" = a dedicated
"Interview Questions" section with many `@topic Q: ...` pairs, distinct from the one-line
`@interview` summary every module already ends with (every subject has that one-liner, so it's
not listed as a separate column). "Project module" = a dedicated end-of-course project/portfolio
section, not just a passing mention of the word "project" inside another module.

| Subject | Modules | Notes + examples | Practice Qs | Interview module | Cheat sheet | Project module | Quiz (backend) |
|---|---:|---|---|---|---|---|---|
| java | 74 | ✅ | ✅ (74 blocks) | ❌ (one-liners only) | ❌ | ✅ (m73) | ❌ (0 quizzes in DB) |
| numpy | 39 | ✅ | ✅ (39) | ❌ | ❌ | ✅ (m38/39) | ❌ |
| data-science | 32 | ✅ | ✅ (32) | ❌ | ❌ | ✅ (m31) | ❌ |
| machine-learning | 28 | ✅ | ✅ (27) | ✅ (22 Q&A) | ❌ | ❌ | ❌ |
| excel | 25 | ✅ | ✅ (24) | ✅ (19 Q&A) | ❌ | ❌ | ❌ |
| cpp | 24 | ✅ | ✅ (24) | ❌ | ❌ | ✅ (m24) | ❌ |
| django | 24 | ✅ | ✅ (24) | ❌ | ❌ | ✅ (m23, capstone blog) | ❌ |
| sql | 24 | ✅ | ✅ (24) | ❌ | ❌ | ❌ | ❌ |
| deep-learning | 24 | ✅ | ✅ (23) | ✅ (21 Q&A) | ❌ | ❌ | ❌ |
| c | 23 | ✅ | ✅ (23) | ❌ | ❌ | ✅ (m24) | ❌ |
| statistics | 22 | ✅ | ✅ (21) | ✅ (20 Q&A) | ❌ | ❌ | ❌ |
| fastapi | 21 | ✅ | ✅ (20) | ✅ (16 Q&A) | ❌ | ❌ | ❌ |
| ai | 20 | ✅ | ✅ (19) | ✅ (19 Q&A) | ❌ | ❌ | ❌ |
| css | 20 | ✅ | ✅ (20) | ❌ | ❌ | ✅ (m20) | ❌ |
| pandas | 20 | ✅ | ✅ (19) | ✅ (17 Q&A) | ❌ | ❌ | ❌ |
| power-bi | 19 | ✅ | ✅ (19) | ✅ (17 Q&A) | ❌ | ❌ | ❌ |
| html | 19 | ✅ | ✅ (19) | ❌ | ❌ | ✅ (m19) | ❌ |
| matplotlib | 18 | ✅ | ✅ (17) | ✅ (14 Q&A) | ❌ | ❌ | ❌ |
| generative-ai | 18 | ✅ | ✅ (17) | ✅ (17 Q&A) | ❌ | ❌ | ❌ |
| agentic-ai | 16 | ✅ | ✅ (15) | ✅ (17 Q&A) | ❌ | ❌ | ❌ |
| seaborn | 16 | ✅ | ✅ (15) | ✅ (13 Q&A) | ❌ | ❌ | ❌ |
| **python** | — | ✅ (own page) | ✅ | ❌ | ❌ | ❌ | ❌ |

**python is a special case**: `python-material.html` exists and is linked from the tutorial
switcher/study page, but it is **not** generated from a `frontend/materials/python.txt` through
`build.py` — there's no `python.txt` in the folder at all. It was hand-authored directly as HTML
(`python-material-source.html` looks like an earlier draft of the same thing, currently unused/
unlinked). This means Python currently sits outside the DSL pipeline this whole audit is about —
flagging it rather than guessing why.

**Cheat sheet and dedicated project modules: zero subjects have a cheat sheet; 9 of 21 have a real
project module** (java, numpy, data-science, cpp, django, c, css, html — csv list above). **Zero
subjects have any quiz content** — `quizzes_quiz` has 0 rows in the database, for every category.

**StudyCategory rows (needed before any quiz can attach to a subject) exist for**: python, c, cpp,
sql, numpy, pandas, matplotlib, seaborn, statistics, machine-learning, deep-learning, power-bi,
excel, django, fastapi, data-science, generative-ai, agentic-ai (18 categories). **Missing entirely**:
html, css, java, and the broad "ai" subject — a StudyCategory row would need to be created for each
before quizzes (or the backend-driven lesson system) could reference them.

## Part B — Full syllabus checklist

Your message's subject list was introduced as "for example" inside a template bracket, so I want to
flag directly: I don't know if that's your real target list or a placeholder you meant to replace.
**I've audited against it as written** since it's a complete, sensible list and gives you something
concrete to react to — tell me if it should change before Step 2 starts.

| Area | Subject | Status | Note |
|---|---|---|---|
| Programming | Java | 🟡 Partial | 74 modules, notes/code/practice all present; missing interview module, cheat sheet, project-module quiz wiring |
| Programming | Python | 🟡 Partial | Exists but outside the `.txt`→`build.py` pipeline (see above) — needs a real `python.txt` to be "reused" the way this audit's DSL rule expects |
| Programming | C | 🟡 Partial | Same gaps as Java (interview module, cheat sheet) |
| Programming | C++ | 🟡 Partial | Same |
| Programming | JavaScript | ❌ Missing | No file at all |
| Programming | TypeScript | ❌ Missing | No file at all |
| Programming | PHP | ❌ Missing | No file at all |
| Web | HTML | 🟡 Partial | Same gaps as C/C++ |
| Web | CSS | 🟡 Partial | Same |
| Web | React | ❌ Missing | No file at all |
| Web | Node.js | ❌ Missing | No file at all |
| Web | Express | ❌ Missing | No file at all |
| Web | MongoDB | ❌ Missing | No file at all (also listed under Database) |
| Web | REST APIs | ❌ Missing | Touched on inside Django/FastAPI materials, no dedicated subject |
| Database | SQL | 🟡 Partial | 24 modules, no interview module, no cheat sheet, no project module |
| Database | MySQL | ❌ Missing | Distinct from the generic SQL material (dialect-specific) |
| Database | PostgreSQL | ❌ Missing | Same |
| Database | MongoDB | ❌ Missing | Duplicate of the Web-section entry |
| CS Core | Data Structures | ❌ Missing | No dedicated subject (touched inside language materials only) |
| CS Core | Algorithms | ❌ Missing | Same |
| CS Core | OOP | ❌ Missing | Covered piecemeal inside Java/C++/Python, no standalone cross-language treatment |
| CS Core | DBMS (theory) | ❌ Missing | Distinct from SQL-the-language: ER modeling, normalization, transactions/ACID, indexing theory |
| CS Core | Operating Systems | ❌ Missing | No file |
| CS Core | Computer Networks | ❌ Missing | No file |
| CS Core | Software Engineering | ❌ Missing | No file |
| CS Core | Compiler Design | ❌ Missing | No file |
| Tools | Git and GitHub | ❌ Missing | No file |
| Tools | Linux | ❌ Missing | No file |
| Tools | Docker | ❌ Missing | No file |
| Tools | Postman | ❌ Missing | No file |
| Tools | VS Code | ❌ Missing | No file |
| Data/AI | NumPy | 🟡 Partial | No interview module/cheat sheet (has a project module) |
| Data/AI | Pandas | ✅ Present | Has interview module; missing cheat sheet + project module |
| Data/AI | Matplotlib | ✅ Present | Same gaps |
| Data/AI | Seaborn | ✅ Present | Same gaps |
| Data/AI | Statistics | ✅ Present | Same gaps |
| Data/AI | Power BI | ✅ Present | Same gaps |
| Data/AI | Excel | ✅ Present | Same gaps |
| Data/AI | ML | ✅ Present | Same gaps |
| Data/AI | Deep Learning | ✅ Present | Same gaps |
| Data/AI | NLP | ❌ Missing | AI material has one NLP module, not a dedicated subject |
| Data/AI | Computer Vision | ❌ Missing | Same — one module inside `ai.txt`, not standalone |
| Data/AI | GenAI | ✅ Present | As `generative-ai`; same cheat-sheet/project gaps |
| Aptitude | Quantitative | ❌ Missing | No file, and this content type doesn't fit the current DSL well (needs numeric-answer practice, not code) |
| Aptitude | Logical Reasoning | ❌ Missing | Same |
| Aptitude | Verbal | ❌ Missing | Same |
| Aptitude | Interview prep (general/HR) | 🟡 Partial | Every subject has technical interview Q&A baked in; no standalone behavioral/HR-round material exists |

**Tally**: 13 Present, 15 Partial (12 existing subjects need upgrading + 1 special-case Python +
general interview prep), **24 flat-out Missing**.

## What I need from you before Step 2

1. **Confirm the syllabus list above is the real target** (or send the real one) — it changes the
   scope a lot (24 new subjects is a bigger undertaking than the 15 "Partial" upgrades).
2. **The priority order** — your message's Rules section says "work on subjects in this priority
   order: [list your top 5]" but the bracket was never filled in. I don't want to guess which 5 of
   ~39 subjects matter most to you.
3. **A call on the Aptitude category**: Quantitative/Logical/Verbal reasoning questions (numeric
   answers, no code) don't map cleanly onto the current `@code`/`@practice` DSL, which is built
   around runnable examples. I can adapt it (e.g. `@practice` items with the answer inline, no
   `@code` block required) rather than changing the DSL's actual syntax/parser — flagging this now
   since you said not to change the DSL, and I want to confirm that interpretation before building
   three subjects' worth of content against it.
4. **A call on Python**: should I write a real `python.txt` (bringing it into the same pipeline as
   everything else, replacing the current hand-authored page), or leave the existing
   `python-material.html` alone and treat Python as out of scope for this audit?

Stopped here per Step 1's instruction — no content has been written yet.
