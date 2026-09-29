# -*- coding: utf-8 -*-
"""Generate standalone HTML study notes and seed the Django database."""

import os
import sys
import html
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from apps.learning.models import StudyCategory, Course, Lesson, StudyMaterial, InterviewQuestion, Level
from apps.learning.curriculum_data import COURSES_DATA, INTERVIEW_QUESTIONS_DATA

def generate_html_notes():
    """Generates a complete, beautiful, responsive, self-contained HTML document."""

    css = """
    :root {
      --bg: #090d16;
      --card-bg: #111827;
      --card-border: #1f293d;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --accent: #818cf8;
      --accent-green: #34d399;
      --accent-amber: #fbbf24;
      --code-bg: #0b1120;
      --code-border: #1e293b;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.65;
      display: flex;
      min-height: 100vh;
    }
    /* Layout */
    #sidebar {
      width: 320px;
      background: #0d1322;
      border-right: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      padding: 1.75rem 1.25rem;
      flex-shrink: 0;
    }
    #content {
      flex: 1;
      padding: 2.5rem 3.5rem;
      max-width: 1100px;
      overflow-y: auto;
    }
    /* Typography */
    h1, h2, h3, h4 {
      color: #f8fafc;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    h1 {
      font-size: 2.5rem;
      margin-bottom: 0.75rem;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .lead {
      font-size: 1.15rem;
      color: var(--text-muted);
      margin-bottom: 2rem;
    }
    h2 {
      font-size: 1.75rem;
      margin: 2.5rem 0 1.25rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    h3 {
      font-size: 1.3rem;
      margin: 1.75rem 0 0.75rem;
      color: #93c5fd;
    }
    p {
      margin-bottom: 1rem;
      color: #cbd5e1;
    }
    /* Navigation */
    .brand-title {
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .brand-subtitle {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-bottom: 1.5rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .nav-group-title {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
      margin: 1.25rem 0 0.5rem;
    }
    .nav-link {
      display: block;
      padding: 0.35rem 0.5rem;
      font-size: 0.875rem;
      color: var(--text-muted);
      text-decoration: none;
      border-radius: 6px;
      transition: all 0.15s ease;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .nav-link:hover {
      color: #fff;
      background: rgba(56, 189, 248, 0.1);
      transform: translateX(3px);
    }
    /* Cards & Containers */
    .module-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.75rem;
      margin-bottom: 2rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      font-size: 0.75rem;
      font-weight: 600;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      margin-bottom: 0.75rem;
    }
    .badge-amber {
      background: rgba(251, 191, 36, 0.15);
      color: var(--accent-amber);
    }
    .badge-green {
      background: rgba(52, 211, 153, 0.15);
      color: var(--accent-green);
    }
    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.25rem 0;
      font-size: 0.925rem;
      background: #0b1120;
      border-radius: 8px;
      overflow: hidden;
    }
    th, td {
      padding: 0.85rem 1.1rem;
      text-align: left;
      border: 1px solid var(--card-border);
    }
    th {
      background: #1e293b;
      color: #38bdf8;
      font-weight: 600;
    }
    tr:nth-child(even) {
      background: rgba(255, 255, 255, 0.02);
    }
    /* Code Blocks */
    pre {
      background: var(--code-bg);
      border: 1px solid var(--code-border);
      border-radius: 8px;
      padding: 1.2rem;
      overflow-x: auto;
      margin: 1rem 0;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 0.9rem;
      color: #f1f5f9;
      line-height: 1.5;
    }
    code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: rgba(56, 189, 248, 0.1);
      color: #38bdf8;
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      font-size: 0.875em;
    }
    pre code {
      background: transparent;
      padding: 0;
      color: inherit;
    }
    /* Callout Alert */
    .callout {
      border-left: 4px solid var(--primary);
      background: rgba(56, 189, 248, 0.08);
      padding: 1rem 1.25rem;
      border-radius: 0 8px 8px 0;
      margin: 1.25rem 0;
    }
    .callout-title {
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 0.35rem;
    }
    /* Q&A Accordion Style */
    .qa-card {
      background: #0e1626;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      margin-bottom: 1rem;
      padding: 1.25rem;
      transition: border-color 0.2s;
    }
    .qa-card:hover {
      border-color: #38bdf8;
    }
    .qa-question {
      font-size: 1.1rem;
      font-weight: 600;
      color: #f8fafc;
      margin-bottom: 0.5rem;
    }
    .qa-short {
      font-weight: 500;
      color: #38bdf8;
      margin-bottom: 0.75rem;
    }
    .qa-tip {
      font-size: 0.85rem;
      color: var(--accent-amber);
      margin-top: 0.75rem;
      padding-top: 0.5rem;
      border-top: 1px dashed var(--card-border);
    }
    /* Print */
    @media print {
      #sidebar { display: none; }
      #content { max-width: 100%; padding: 0; }
      body { background: white; color: black; }
      .module-card, pre { border-color: #ccc; }
    }
    @media (max-width: 860px) {
      body { flex-direction: column; }
      #sidebar { width: 100%; height: auto; position: static; }
      #content { padding: 1.5rem; }
    }
    """

    # Build Sidebar Navigation
    nav_html = """
    <div class="brand-title">🐍 Python Complete Guide</div>
    <div class="brand-subtitle">Zero to Advanced / AI Engineer</div>
    """

    for course_idx, c in enumerate(COURSES_DATA, start=1):
        nav_html += f'<div class="nav-group-title">Part {course_idx}: {html.escape(c["title"])}</div>\n'
        for l in c["lessons"]:
            nav_html += f'<a class="nav-link" href="#{l["slug"]}">{html.escape(l["title"])}</a>\n'

    nav_html += """
    <div class="nav-group-title">Interview Mastery</div>
    <a class="nav-link" href="#interview-questions">Top 25 Technical Q&amp;A</a>
    """

    # Build Content Body
    body_html = """
    <header>
      <h1>🐍 Python Complete Masterclass Syllabus &amp; Notes</h1>
      <p class="lead">A complete, end-to-end reference from zero → intermediate → advanced → Data Science/AI developer level. Fully populated with explanations, code examples, comparison tables, and interview solutions.</p>
    </header>
    """

    for course_idx, c in enumerate(COURSES_DATA, start=1):
        body_html += f"""
        <section id="{c['slug']}">
          <h2>{course_idx}. {html.escape(c['title'])}</h2>
          <p class="lead">{html.escape(c['description'])}</p>
        """

        for l in c["lessons"]:
            # Convert basic markdown formatting into HTML
            content = l["content"]
            # Render headings
            lines = content.split("\n")
            rendered_lines = []
            in_code = False
            for line in lines:
                if line.startswith("```"):
                    if not in_code:
                        rendered_lines.append("<pre><code>")
                        in_code = True
                    else:
                        rendered_lines.append("</code></pre>")
                        in_code = False
                elif in_code:
                    rendered_lines.append(html.escape(line))
                elif line.startswith("# "):
                    rendered_lines.append(f"<h3>{html.escape(line[2:])}</h3>")
                elif line.startswith("### "):
                    rendered_lines.append(f"<h4>{html.escape(line[4:])}</h4>")
                elif line.startswith("#### "):
                    rendered_lines.append(f"<h5>{html.escape(line[5:])}</h5>")
                elif line.startswith("> "):
                    rendered_lines.append(f'<div class="callout"><div class="callout-title">Tip</div><p>{html.escape(line[2:])}</p></div>')
                elif line.startswith("- "):
                    rendered_lines.append(f"<li>{html.escape(line[2:])}</li>")
                elif line.strip() == "---":
                    rendered_lines.append("<hr style='border: 0; border-top: 1px solid var(--card-border); margin: 1.5rem 0;'>")
                else:
                    if line.strip():
                        rendered_lines.append(f"<p>{html.escape(line)}</p>")

            lesson_body = "\n".join(rendered_lines)

            body_html += f"""
            <article class="module-card" id="{l['slug']}">
              <span class="badge">Est. {l['estimated_minutes']} Mins</span>
              <h3>{html.escape(l['title'])}</h3>
              <p><em>{html.escape(l['summary'])}</em></p>
              <div class="lesson-content">
                {lesson_body}
              </div>
            </article>
            """

        body_html += "</section>\n"

    # Add Dedicated 25 Interview Questions Section
    body_html += """
    <section id="interview-questions">
      <h2>Top 25 Python Technical Interview Questions &amp; Deep-Dive Answers</h2>
      <p class="lead">Frequently asked questions in Python, Data Science, and Machine Learning technical interviews with direct answers, code demonstrations, and interviewer tips.</p>
    """

    for idx, q in enumerate(INTERVIEW_QUESTIONS_DATA, start=1):
        diff_badge = "badge-green" if q["difficulty"] == "EASY" else ("badge" if q["difficulty"] == "MEDIUM" else "badge-amber")
        body_html += f"""
        <div class="qa-card" id="q-{idx}">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="qa-question">{idx}. {html.escape(q['question'])}</div>
            <span class="badge {diff_badge}">{q['difficulty']}</span>
          </div>
          <div class="qa-short"><strong>Quick Answer:</strong> {html.escape(q['short_answer'])}</div>
          <p>{html.escape(q['detailed_answer'])}</p>
          <pre><code>{html.escape(q['code'])}</code></pre>
          <div class="qa-tip">💡 <strong>Interview Pro-Tip:</strong> {html.escape(q['interview_tip'])}</div>
        </div>
        """

    body_html += "</section>\n"

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Python Complete Masterclass Syllabus &amp; Notes — Beginner to Advanced</title>
  <style>{css}</style>
</head>
<body>
  <nav id="sidebar">
    {nav_html}
  </nav>
  <main id="content">
    {body_html}
  </main>
</body>
</html>
"""
    return full_html

def seed_database():
    """Seeds Python category, courses, lessons, materials, and interview questions."""
    print("Starting database transaction...")
    with transaction.atomic():
        # 1. StudyCategory: Python
        category, _ = StudyCategory.objects.get_or_create(
            slug="python",
            defaults={
                "name": "Python",
                "description": "Comprehensive Python programming track: syntax, data structures, OOP, functional patterns, algorithms, and Data Science foundations.",
                "icon": "python",
                "order": 1,
                "is_published": True,
            }
        )
        category.name = "Python"
        category.icon = "python"
        category.is_published = True
        category.save()
        print(f"Category ensured: {category.name}")

        # 2. Courses & Lessons
        for c_data in COURSES_DATA:
            course, _ = Course.objects.get_or_create(
                category=category,
                slug=c_data["slug"],
                defaults={
                    "title": c_data["title"],
                    "level": c_data["level"],
                    "description": c_data["description"],
                    "order": c_data["order"],
                    "is_published": True,
                }
            )
            course.title = c_data["title"]
            course.level = c_data["level"]
            course.description = c_data["description"]
            course.order = c_data["order"]
            course.is_published = True
            course.save()
            print(f"  Course: {course.title} ({course.level})")

            for l_data in c_data["lessons"]:
                lesson, _ = Lesson.objects.get_or_create(
                    category=category,
                    slug=l_data["slug"],
                    defaults={
                        "course": course,
                        "title": l_data["title"],
                        "summary": l_data["summary"],
                        "content": l_data["content"],
                        "estimated_minutes": l_data["estimated_minutes"],
                        "order": l_data["order"],
                        "is_published": True,
                    }
                )
                lesson.course = course
                lesson.title = l_data["title"]
                lesson.summary = l_data["summary"]
                lesson.content = l_data["content"]
                lesson.estimated_minutes = l_data["estimated_minutes"]
                lesson.order = l_data["order"]
                lesson.is_published = True
                lesson.save()
                print(f"    Lesson: {lesson.title}")

        # 3. Seed Interview Questions
        InterviewQuestion.objects.filter(category=category).delete()
        for q_data in INTERVIEW_QUESTIONS_DATA:
            InterviewQuestion.objects.create(
                category=category,
                question=q_data["question"],
                difficulty=q_data["difficulty"],
                short_answer=q_data["short_answer"],
                detailed_answer=q_data["detailed_answer"],
                example=q_data["example"],
                code=q_data["code"],
                code_language="python",
                interview_tip=q_data["interview_tip"],
                is_published=True
            )
        print(f"Seeded {len(INTERVIEW_QUESTIONS_DATA)} Interview Questions.")

        # 4. Attach StudyMaterial pointing to HTML notes
        first_course = Course.objects.filter(category=category).first()
        StudyMaterial.objects.filter(course__category=category).delete()

        material = StudyMaterial.objects.create(
            title="Python Complete Syllabus — End-to-End Notes (HTML)",
            kind=StudyMaterial.Kind.NOTES,
            course=first_course,
            external_url="/study/python-complete-study-notes.html",
            description="Interactive standalone single-page HTML notes covering beginner to advanced Python, memory structures, OOP, and 25 interview questions with executable code examples.",
            is_downloadable=True,
            requires_login=False,
            order=1
        )
        print(f"Study Material created: {material.title}")
        print(f"Study Material created: {material.title}")

    print("Database seeding completed successfully!")

if __name__ == "__main__":
    html_content = generate_html_notes()
    
    # Served by Django at /study/python-complete-study-notes.html (see apps/web/urls.py)
    notes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps", "web", "study", "python-complete-study-notes.html")
    os.makedirs(os.path.dirname(notes_path), exist_ok=True)
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML notes written to: {notes_path}")

    seed_database()
