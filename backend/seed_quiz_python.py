"""Seed the Python category and its 20-question fundamentals quiz.

Usage: python seed_quiz_python.py (run from backend/, same venv as manage.py)
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
        "prompt": "What does a Python function return when it reaches the end without a return statement?",
        "options": ["0", "False", "None", "An empty string"],
        "correct_option": 2,
        "explanation": "A function without an explicit return value returns `None`.",
    },
    {
        "prompt": "Which operator performs floor division in Python?",
        "options": ["/", "//", "%", "**"],
        "correct_option": 1,
        "explanation": "`//` performs floor division; `/` performs true division.",
    },
    {
        "prompt": "Which expression is the recommended way to check whether `value` is None?",
        "options": ["value == null", "value is None", "value = None", "None(value)"],
        "correct_option": 1,
        "explanation": "Use identity comparison with the singleton: `value is None`.",
    },
    {
        "prompt": "What does the slice `items[1:4]` include?",
        "options": [
            "Indexes 1 through 4, inclusive",
            "Indexes 1, 2, and 3",
            "Indexes 0, 1, 2, and 3",
            "Only index 4",
        ],
        "correct_option": 1,
        "explanation": "A slice includes its start and excludes its stop index.",
    },
    {
        "prompt": "Which statement adds each element of `new_items` to the end of a list named `items`?",
        "options": ["items.append(new_items)", "items.extend(new_items)", "items.add(new_items)", "items.push(new_items)"],
        "correct_option": 1,
        "explanation": "`extend` iterates over its argument and adds each element; `append` adds the argument as one element.",
    },
    {
        "prompt": "Which built-in collection stores unique hashable values and supports set intersection?",
        "options": ["list", "tuple", "set", "dict_values"],
        "correct_option": 2,
        "explanation": "Sets store unique hashable values and support operations such as intersection with `&`.",
    },
    {
        "prompt": "What does `range(5)` produce when iterated?",
        "options": ["0 through 5", "1 through 5", "0 through 4", "1 through 4"],
        "correct_option": 2,
        "explanation": "`range(stop)` starts at zero and excludes the stop value.",
    },
    {
        "prompt": "Which built-in function is useful for looping over values together with their indexes?",
        "options": ["zip", "enumerate", "iter", "index"],
        "correct_option": 1,
        "explanation": "`enumerate(iterable)` yields index-value pairs and can take a custom starting index.",
    },
    {
        "prompt": "What type does `*args` collect extra positional arguments into?",
        "options": ["A list", "A tuple", "A set", "A dictionary"],
        "correct_option": 1,
        "explanation": "Extra positional arguments are collected into a tuple named by the `*args` parameter.",
    },
    {
        "prompt": "What type does `**kwargs` collect extra keyword arguments into?",
        "options": ["A tuple", "A list", "A dictionary", "A set"],
        "correct_option": 2,
        "explanation": "Extra keyword arguments are collected into a dictionary named by the `**kwargs` parameter.",
    },
    {
        "prompt": "Why should a function usually avoid a list as a default parameter value?",
        "options": [
            "Lists cannot be passed to functions",
            "The same list object can be reused across calls",
            "Default values must be strings",
            "Python copies every default and loses its contents",
        ],
        "correct_option": 1,
        "explanation": "Default expressions are evaluated once when the function is defined, so a mutable default can retain changes between calls.",
    },
    {
        "prompt": "Which exception should commonly be handled when `int(text)` receives non-numeric text?",
        "options": ["KeyError", "IndexError", "ValueError", "AttributeError"],
        "correct_option": 2,
        "explanation": "Converting a string that is not a valid integer raises `ValueError`.",
    },
    {
        "prompt": "When does the `else` clause of a `try` statement run?",
        "options": [
            "Whenever an exception is raised",
            "Only when the `try` block completes without an exception",
            "Only when `finally` is absent",
            "Before the `try` block runs",
        ],
        "correct_option": 1,
        "explanation": "The `else` suite runs only if execution leaves the `try` suite without raising an exception.",
    },
    {
        "prompt": "What is a key benefit of opening a file with a `with` statement?",
        "options": [
            "It automatically encrypts file contents",
            "It closes the file when the block exits",
            "It makes every file read asynchronous",
            "It prevents all file-related exceptions",
        ],
        "correct_option": 1,
        "explanation": "A file context manager closes the file when control leaves the block, including when an exception occurs.",
    },
    {
        "prompt": "Which keyword is used in a generator function to produce a value lazily?",
        "options": ["return", "yield", "await", "defer"],
        "correct_option": 1,
        "explanation": "`yield` produces a value and suspends a generator function so it can continue later.",
    },
    {
        "prompt": "What does `self` conventionally refer to in an instance method?",
        "options": [
            "The class's parent class",
            "The current instance",
            "The module containing the class",
            "The method's return value",
        ],
        "correct_option": 1,
        "explanation": "Instance methods receive the current instance as their first argument, conventionally named `self`.",
    },
    {
        "prompt": "Which relationship is usually represented by composition?",
        "options": ["Is-a", "Has-a", "Runs-before", "Overrides"],
        "correct_option": 1,
        "explanation": "Composition models a has-a relationship by having an object contain or collaborate with other objects.",
    },
    {
        "prompt": "Are ordinary Python type hints automatically enforced by the runtime?",
        "options": [
            "Yes, every call is checked automatically",
            "No, they are not automatically enforced",
            "Only for built-in types",
            "Only when a function has a return annotation",
        ],
        "correct_option": 1,
        "explanation": "Annotations are not automatically enforced by Python; static analysis tools can use them to find mismatches.",
    },
    {
        "prompt": "What does a Python virtual environment primarily isolate?",
        "options": [
            "Project dependencies and their installation location",
            "The operating system kernel",
            "The Python language syntax",
            "The source files from the project folder",
        ],
        "correct_option": 0,
        "explanation": "A virtual environment separates a project's interpreter environment and installed packages from other projects.",
    },
    {
        "prompt": "Which command runs pytest using the currently selected Python interpreter?",
        "options": ["python pytest", "python -m pytest", "pip test pytest", "python --pytest"],
        "correct_option": 1,
        "explanation": "`python -m pytest` runs pytest as a module under that Python interpreter.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="python",
            defaults={"name": "Python", "icon": "python", "order": 20, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="python-fundamentals-quiz",
            defaults={
                "title": "Python Fundamentals Quiz",
                "description": "20 questions covering Python syntax, collections, functions, files, exceptions, and core concepts.",
                "category": category,
                "difficulty": Quiz.Difficulty.EASY,
                "time_limit_minutes": 15,
                "show_leaderboard": True,
                "order": 1,
                "is_published": True,
            },
        )
        if quiz.category_id != category.id or not quiz.is_published:
            quiz.category = category
            quiz.is_published = True
            quiz.save(update_fields=["category", "is_published"])

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