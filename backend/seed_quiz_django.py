"""Seed the Django category and its 20-question fundamentals quiz.

Usage: python seed_quiz_django.py (run from backend/, same venv as manage.py)
"""
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction

from apps.learning.models import StudyCategory
from apps.quizzes.models import Quiz, QuizQuestion

QUESTIONS = [
    {
        "prompt": "What is a Django project compared with a Django app?",
        "options": [
            "A project configures the whole site; an app packages a focused feature",
            "A project is a database row; an app is a template",
            "They are two required names for the same object",
            "An app contains settings and a project contains only views",
        ],
        "correct_option": 0,
        "explanation": "A project holds site-level configuration and installed apps; an app is a reusable component for a feature area.",
    },
    {
        "prompt": "Which sequence best describes Django's request flow?",
        "options": [
            "URL configuration → view → response (possibly rendered from a template)",
            "Template → database migration → URL configuration",
            "Model → browser cache → middleware only",
            "Static file → model form → app installation",
        ],
        "correct_option": 0,
        "explanation": "Django resolves a request through URL patterns to a view, which returns a response or renders a template.",
    },
    {
        "prompt": "What does Django's ORM primarily provide?",
        "options": [
            "A Python API for defining and querying database-backed models",
            "A browser rendering engine",
            "A JavaScript package manager",
            "A replacement for HTTP",
        ],
        "correct_option": 0,
        "explanation": "The ORM maps model classes and QuerySets to database operations.",
    },
    {
        "prompt": "What does it mean that a Django QuerySet is lazy?",
        "options": [
            "The database query is generally evaluated when the QuerySet is consumed",
            "The query is always run when the QuerySet is first constructed",
            "The query can never be evaluated",
            "The QuerySet runs only during a migration",
        ],
        "correct_option": 0,
        "explanation": "QuerySets usually build a query description first and execute SQL when evaluated, for example by iteration or conversion to a list.",
    },
    {
        "prompt": "Which ORM method is suited to loading a ForeignKey relation with a SQL join?",
        "options": ["`prefetch_related`", "`select_related`", "`only_related`", "`join_related`"],
        "correct_option": 1,
        "explanation": "`select_related` follows single-valued ForeignKey and OneToOne relations using a SQL join.",
    },
    {
        "prompt": "Which ORM method is commonly used to avoid repeated queries for many-to-many relations?",
        "options": ["`select_related`", "`prefetch_related`", "`get_or_create_related`", "`join_table`"],
        "correct_option": 1,
        "explanation": "`prefetch_related` runs additional queries and joins results in Python for many-valued relations.",
    },
    {
        "prompt": "What do Django migrations represent?",
        "options": [
            "Versioned changes to database schema and related state",
            "Browser navigation history",
            "Static file compression settings",
            "A replacement for model definitions",
        ],
        "correct_option": 0,
        "explanation": "Migrations record and apply incremental changes to the database schema based on model changes.",
    },
    {
        "prompt": "What is the usual distinction between `null=True` and `blank=True` on a model field?",
        "options": [
            "`null` affects database storage; `blank` affects validation",
            "`null` affects templates; `blank` affects URL routing",
            "They always have identical effects",
            "`blank=True` makes a field unique",
        ],
        "correct_option": 0,
        "explanation": "`null` concerns database representation, while `blank` controls whether validation permits an empty value.",
    },
    {
        "prompt": "What does a valid `ModelForm` provide?",
        "options": [
            "Form validation and a model instance that can be saved when appropriate",
            "Automatic authorization for every user",
            "A database backup on each request",
            "Automatic URL patterns for all models",
        ],
        "correct_option": 0,
        "explanation": "A ModelForm derives fields and validation from a model and can create or update an instance after valid input.",
    },
    {
        "prompt": "What does Django's CSRF protection help prevent?",
        "options": [
            "Cross-site request forgery using a trusted user's authenticated browser",
            "SQL query syntax errors",
            "All cross-site scripting vulnerabilities",
            "Unauthorized access to static files only",
        ],
        "correct_option": 0,
        "explanation": "CSRF protection checks a token on unsafe requests to help prevent forged requests made through an authenticated browser.",
    },
    {
        "prompt": "How does Django's template system help reduce XSS risk by default?",
        "options": [
            "It autoescapes variable output in HTML templates by default",
            "It encrypts every string before rendering",
            "It disables all user input",
            "It strips every HTML tag from the database",
        ],
        "correct_option": 0,
        "explanation": "Django templates autoescape variable output by default; marking content safe must be deliberate and justified.",
    },
    {
        "prompt": "When should a custom Django user model generally be configured?",
        "options": [
            "Before the first migration of a new project",
            "Only after the production database has years of data",
            "Inside every view function",
            "After replacing all passwords with plaintext",
        ],
        "correct_option": 0,
        "explanation": "Set `AUTH_USER_MODEL` before the initial migrations because changing the user model later can require a complex migration plan.",
    },
    {
        "prompt": "What is Django middleware used for?",
        "options": [
            "Hooks that process requests and responses across the request/response cycle",
            "A database table editor only",
            "A model field type for file uploads",
            "A template inheritance syntax",
        ],
        "correct_option": 0,
        "explanation": "Middleware provides request/response hooks for concerns such as sessions, security, authentication, and common headers.",
    },
    {
        "prompt": "What does `get_object_or_404(Model, ...)` do when no row matches?",
        "options": [
            "Raises `Http404` so the request can produce a 404 response",
            "Creates an empty model row",
            "Redirects to the admin page",
            "Returns every row in the table",
        ],
        "correct_option": 0,
        "explanation": "The shortcut raises `Http404` when the object does not exist, which Django converts to a 404 response.",
    },
    {
        "prompt": "What does `transaction.atomic()` provide?",
        "options": [
            "A transaction boundary that commits on success and rolls back on an exception",
            "Automatic caching of all queries",
            "A lock covering every database in the system",
            "A replacement for database migrations",
        ],
        "correct_option": 0,
        "explanation": "An atomic block groups database operations so they commit together or roll back together on failure.",
    },
    {
        "prompt": "What is the distinction between static files and media files?",
        "options": [
            "Static files are application assets; media files are typically user uploads",
            "Static files are database rows; media files are URL patterns",
            "They are interchangeable names for templates",
            "Media files can only contain CSS",
        ],
        "correct_option": 0,
        "explanation": "Static assets ship with the application; media is user-provided content and needs its own storage and access policy.",
    },
    {
        "prompt": "What is a critical production setting for Django?",
        "options": [
            "Set `DEBUG=False` and keep secret values outside source control",
            "Set `DEBUG=True` to show users detailed tracebacks",
            "Hard-code the production secret key in a public repository",
            "Disable host validation for every request",
        ],
        "correct_option": 0,
        "explanation": "Production should disable debug pages and load secrets from protected configuration, with allowed hosts configured explicitly.",
    },
    {
        "prompt": "What can Django's test client do?",
        "options": [
            "Exercise application URLs and inspect response status, content, and behavior without a live browser",
            "Compile Python into Java bytecode",
            "Automatically prove every permission rule is correct",
            "Replace all database migration tests",
        ],
        "correct_option": 0,
        "explanation": "The test client simulates requests to the Django application and lets tests assert on responses and state.",
    },
    {
        "prompt": "Where should object-level authorization usually be enforced?",
        "options": [
            "On the server for every relevant request or service operation",
            "Only by hiding a button in the template",
            "Only in client-side JavaScript",
            "Only in the database column label",
        ],
        "correct_option": 0,
        "explanation": "Authorization must be enforced server-side; hiding UI controls does not prevent direct requests.",
    },
    {
        "prompt": "In Django REST Framework, what is a serializer commonly responsible for?",
        "options": [
            "Converting and validating data between complex objects and primitive representations",
            "Serving CSS files from a CDN",
            "Opening database network ports",
            "Defining URL names only",
        ],
        "correct_option": 0,
        "explanation": "DRF serializers validate incoming data and represent model or other complex values in primitive formats such as JSON.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="django",
            defaults={"name": "Django", "icon": "code", "order": 60, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="django-fundamentals-quiz",
            defaults={
                "title": "Django Fundamentals Quiz",
                "description": "20 questions covering request flow, models, QuerySets, forms, security, testing, and deployment.",
                "category": category,
                "difficulty": Quiz.Difficulty.MEDIUM,
                "time_limit_minutes": 20,
                "show_leaderboard": True,
                "order": 1,
                "is_published": True,
            },
        )
        if quiz.category_id != category.id or not quiz.is_published:
            quiz.category = category
            quiz.is_published = True
            quiz.save(update_fields=["category", "is_published"])

        QuizQuestion.objects.filter(quiz=quiz, order__gt=len(QUESTIONS)).delete()
        for index, question in enumerate(QUESTIONS, start=1):
            QuizQuestion.objects.update_or_create(
                quiz=quiz,
                order=index,
                defaults={
                    "type": QuizQuestion.Type.MCQ,
                    "prompt": question["prompt"],
                    "options": question["options"],
                    "correct_option": question["correct_option"],
                    "explanation": question["explanation"],
                    "points": 1,
                },
            )

    print(f"Category: {category.slug} (published={category.is_published})")
    print(f"Quiz: {quiz.slug} - {quiz.questions.count()} questions")


if __name__ == "__main__":
    run()