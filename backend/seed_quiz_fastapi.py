"""Seed the FastAPI category and its 20-question fundamentals quiz.

Usage: python seed_quiz_fastapi.py (run from backend/, same venv as manage.py)
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
        "prompt": "How does FastAPI commonly use Python type hints on path parameters?",
        "options": [
            "To parse and validate values, such as converting a path segment to an integer",
            "To create a database table automatically for every parameter",
            "To encrypt every request",
            "To disable request validation",
        ],
        "correct_option": 0,
        "explanation": "FastAPI uses annotations to parse and validate request data and to generate API schema information.",
    },
    {
        "prompt": "What does a Pydantic request model commonly provide in FastAPI?",
        "options": [
            "Parsing and validation of structured request data",
            "A production web server",
            "Automatic authorization for every user",
            "A database transaction for every route",
        ],
        "correct_option": 0,
        "explanation": "Pydantic models describe structured data and validate input against their fields and constraints.",
    },
    {
        "prompt": "What is one purpose of the `response_model` parameter on a path operation?",
        "options": [
            "Validate, serialize, and document the response shape",
            "Choose which database connection to use",
            "Replace request validation",
            "Configure the server's listening port",
        ],
        "correct_option": 0,
        "explanation": "A response model helps shape and validate output and contributes the response schema to API documentation.",
    },
    {
        "prompt": "How does a FastAPI endpoint commonly return a deliberate HTTP error such as 404?",
        "options": [
            "Raise `HTTPException` with the intended status code",
            "Return a Python `assert` statement",
            "Print an error to standard output only",
            "Change the path parameter's type",
        ],
        "correct_option": 0,
        "explanation": "Raising `HTTPException` communicates an HTTP status and detail through FastAPI's exception handling.",
    },
    {
        "prompt": "What is a common use of `Depends` in FastAPI?",
        "options": [
            "Declare reusable dependencies such as authentication, settings, or database sessions",
            "Start the ASGI server",
            "Create a Pydantic model from a SQL query",
            "Disable automatic OpenAPI generation",
        ],
        "correct_option": 0,
        "explanation": "Dependency injection provides reusable values and behavior to path operations and other dependencies.",
    },
    {
        "prompt": "What does `APIRouter` help organize?",
        "options": [
            "Related path operations that can be included in an application",
            "Database rows into sorted groups",
            "Python virtual environments",
            "Static files into a ZIP archive",
        ],
        "correct_option": 0,
        "explanation": "APIRouter groups related path operations and can be included in the main FastAPI application.",
    },
    {
        "prompt": "When is a synchronous `def` path operation useful in FastAPI?",
        "options": [
            "When using blocking libraries that do not provide async APIs",
            "Only when the endpoint returns no response",
            "When the endpoint must bypass all validation",
            "Whenever the application has more than one route",
        ],
        "correct_option": 0,
        "explanation": "FastAPI runs synchronous path operations in a thread pool, which is often appropriate for blocking libraries.",
    },
    {
        "prompt": "What is a risk of calling blocking I/O directly inside an `async def` endpoint?",
        "options": [
            "It can block the event loop and delay other asynchronous work",
            "It automatically creates a database migration",
            "It converts every response to plain text",
            "It disables Python type hints",
        ],
        "correct_option": 0,
        "explanation": "Blocking work on the event loop can prevent it from scheduling other tasks; use async-compatible APIs or an appropriate sync boundary.",
    },
    {
        "prompt": "What does `await` do in an async function?",
        "options": [
            "Suspends that coroutine until an awaitable completes, allowing other work to run",
            "Blocks every thread in the process",
            "Starts a new operating system process",
            "Automatically retries failed HTTP requests",
        ],
        "correct_option": 0,
        "explanation": "Awaiting yields control while the awaitable is pending, allowing the event loop to run other tasks.",
    },
    {
        "prompt": "Which HTTP status code is commonly used when a POST operation creates a resource?",
        "options": ["200", "201", "301", "404"],
        "correct_option": 1,
        "explanation": "201 Created is commonly used when a request creates a resource; the exact response contract should be documented.",
    },
    {
        "prompt": "What is a common purpose of an application lifespan handler?",
        "options": [
            "Manage startup and shutdown resources such as connection pools",
            "Validate each request body instead of Pydantic",
            "Render every response as HTML",
            "Replace all route definitions",
        ],
        "correct_option": 0,
        "explanation": "A lifespan context can acquire resources at application startup and release them at shutdown.",
    },
    {
        "prompt": "What does CORS configuration control in a browser context?",
        "options": [
            "Which browser origins are permitted to make cross-origin requests under the server's policy",
            "Which database tables can be migrated",
            "The password hashing algorithm",
            "The number of Python packages installed",
        ],
        "correct_option": 0,
        "explanation": "CORS headers control browser access to cross-origin responses; configure trusted origins narrowly.",
    },
    {
        "prompt": "What does `OAuth2PasswordBearer` commonly provide to a dependency?",
        "options": [
            "Extraction of a bearer token from the Authorization header",
            "Automatic verification of every token's signature and claims",
            "A persistent password database",
            "A TLS certificate for the server",
        ],
        "correct_option": 0,
        "explanation": "OAuth2PasswordBearer extracts the token; application code or a security library must still validate it and enforce authorization.",
    },
    {
        "prompt": "What can Starlette's `TestClient` help test?",
        "options": [
            "Application requests and responses without launching a separate production server",
            "A real remote user's browser cache only",
            "Database backups without connecting to a database",
            "The operating system's network driver",
        ],
        "correct_option": 0,
        "explanation": "TestClient exercises the ASGI application and allows assertions on responses and application behavior.",
    },
    {
        "prompt": "Why override a dependency during a test?",
        "options": [
            "Provide a controlled fake or test resource instead of the production dependency",
            "Disable all path operations",
            "Force the test to use a public database",
            "Skip response serialization permanently",
        ],
        "correct_option": 0,
        "explanation": "Dependency overrides let tests replace resources such as authentication providers or database sessions with controlled implementations.",
    },
    {
        "prompt": "What is one reason to use `UploadFile` for uploaded files?",
        "options": [
            "It provides file-like access and can use spooled storage for larger content",
            "It guarantees every upload is safe to execute",
            "It automatically stores files in an encrypted database",
            "It bypasses request-size limits in every deployment",
        ],
        "correct_option": 0,
        "explanation": "UploadFile offers file-like handling and spooling behavior; applications still need size, content, and access validation.",
    },
    {
        "prompt": "Are in-process background tasks a durable job queue by themselves?",
        "options": [
            "No; durable, distributed work generally needs a separate task system and persistence",
            "Yes; they survive every process crash automatically",
            "Yes; they guarantee exactly-once execution",
            "No; FastAPI cannot schedule any post-response work",
        ],
        "correct_option": 0,
        "explanation": "In-process background tasks are not a durable distributed queue and can be lost if the process stops.",
    },
    {
        "prompt": "What role does an ASGI server such as Uvicorn play?",
        "options": [
            "Serve an ASGI application and handle the network-facing server protocol",
            "Define Pydantic model fields",
            "Replace application authorization checks",
            "Generate SQL migrations from route decorators",
        ],
        "correct_option": 0,
        "explanation": "An ASGI server accepts connections and invokes the ASGI application according to the server interface.",
    },
    {
        "prompt": "What does FastAPI use to provide interactive API documentation by default?",
        "options": [
            "An OpenAPI schema rendered by interfaces such as Swagger UI",
            "A Django admin site generated from every route",
            "A database console embedded in every response",
            "A static HTML file that must be handwritten for each endpoint",
        ],
        "correct_option": 0,
        "explanation": "FastAPI generates an OpenAPI schema from route and model metadata and provides interactive documentation interfaces by default.",
    },
    {
        "prompt": "Where should authorization for a protected resource be enforced?",
        "options": [
            "On the server for each relevant operation, even if the UI hides controls",
            "Only in the browser by hiding a link",
            "Only in the OpenAPI description",
            "Only in a response model's field names",
        ],
        "correct_option": 0,
        "explanation": "Authorization must be checked server-side on every protected operation; client-side visibility is not a security boundary.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="fastapi",
            defaults={"name": "FastAPI", "icon": "code", "order": 110, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="fastapi-fundamentals-quiz",
            defaults={
                "title": "FastAPI Fundamentals Quiz",
                "description": "20 questions covering validation, dependency injection, async behavior, security, testing, and deployment.",
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