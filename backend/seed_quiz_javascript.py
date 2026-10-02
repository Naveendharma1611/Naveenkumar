"""Seed the JavaScript category and its 20-question fundamentals quiz.

Usage: python seed_quiz_javascript.py (run from backend/, same venv as manage.py)
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
        "prompt": "Which statement about a variable declared with `const` is correct?",
        "options": [
            "Neither the binding nor an assigned object can ever change",
            "The binding cannot be reassigned, but an assigned object may be mutated",
            "The variable is automatically frozen",
            "The variable is only available inside loops",
        ],
        "correct_option": 1,
        "explanation": "`const` prevents reassignment of the binding; it does not make referenced objects immutable.",
    },
    {
        "prompt": "Which equality operator compares values without implicit type coercion?",
        "options": ["=", "==", "===", "!"],
        "correct_option": 2,
        "explanation": "`===` is strict equality and does not coerce operands to a common type.",
    },
    {
        "prompt": "What does `typeof null` evaluate to in JavaScript?",
        "options": ["`null`", "`undefined`", "`object`", "`boolean`"],
        "correct_option": 2,
        "explanation": "`typeof null` returns `\"object\"` due to a historical language quirk.",
    },
    {
        "prompt": "Which method is designed to transform each element and return a new array?",
        "options": ["`map`", "`forEach`", "`find`", "`some`"],
        "correct_option": 0,
        "explanation": "`map` calls a transformation callback for each element and returns the results in a new array.",
    },
    {
        "prompt": "Which array method returns the first element that satisfies a condition?",
        "options": ["`filter`", "`find`", "`reduce`", "`every`"],
        "correct_option": 1,
        "explanation": "`find` returns the first matching element, or `undefined` when there is no match.",
    },
    {
        "prompt": "What does `filter` return when called on an array?",
        "options": [
            "The index of the first matching element",
            "A new array containing elements that pass the test",
            "A boolean indicating whether every item passed",
            "The original array after deleting non-matches",
        ],
        "correct_option": 1,
        "explanation": "`filter` creates a new array with the elements for which its callback returns a truthy value.",
    },
    {
        "prompt": "What is the main copying limitation of `{ ...original }`?",
        "options": [
            "It only copies string properties",
            "It creates a shallow copy, so nested object references are shared",
            "It freezes the new object",
            "It copies only inherited properties",
        ],
        "correct_option": 1,
        "explanation": "Object spread copies enumerable own properties into a new object but does not recursively clone nested values.",
    },
    {
        "prompt": "What does a closure allow a function to do?",
        "options": [
            "Access variables from its surrounding lexical scope later",
            "Pause execution without a promise",
            "Create a new JavaScript runtime",
            "Change a `const` binding in another scope",
        ],
        "correct_option": 0,
        "explanation": "A closure retains access to variables from the lexical environment where the function was created.",
    },
    {
        "prompt": "How is `this` determined inside an arrow function?",
        "options": [
            "It is always the global object",
            "It is captured lexically from the surrounding scope",
            "It is always the function's first argument",
            "It is selected by the last property accessed",
        ],
        "correct_option": 1,
        "explanation": "Arrow functions do not have their own `this`; they capture it from the surrounding lexical scope.",
    },
    {
        "prompt": "Which loop form directly iterates over values from an array?",
        "options": ["`for...in`", "`for...of`", "`while...of`", "`for...keys`"],
        "correct_option": 1,
        "explanation": "`for...of` iterates over values from an iterable such as an array.",
    },
    {
        "prompt": "Which collection can use an object as a key and is designed for key-value entries?",
        "options": ["`Set`", "`Map`", "`WeakSet`", "`Array`"],
        "correct_option": 1,
        "explanation": "A `Map` supports keys of any value type, including object references.",
    },
    {
        "prompt": "What happens when the same value is added twice to a `Set`?",
        "options": [
            "The second value replaces the first with a duplicate entry",
            "The set keeps only one instance of that value",
            "The set converts into an array",
            "JavaScript throws a duplicate-key error",
        ],
        "correct_option": 1,
        "explanation": "A `Set` stores unique values; adding an existing value does not create a duplicate entry.",
    },
    {
        "prompt": "What does an `async` function always return?",
        "options": ["A generator", "A promise", "An array", "A callback"],
        "correct_option": 1,
        "explanation": "An `async` function always returns a promise, even when its body returns a plain value.",
    },
    {
        "prompt": "What does `await` do inside an async function?",
        "options": [
            "Blocks the entire JavaScript thread until completion",
            "Suspends that async function until the awaited value settles",
            "Converts a value into a callback",
            "Cancels the current promise",
        ],
        "correct_option": 1,
        "explanation": "`await` suspends the async function while allowing the JavaScript thread to continue other work.",
    },
    {
        "prompt": "What happens when one input promise rejects in `Promise.all`?",
        "options": [
            "The result fulfills with the rejected error",
            "The combined promise rejects",
            "The rejected promise is silently ignored",
            "All input promises are automatically canceled",
        ],
        "correct_option": 1,
        "explanation": "`Promise.all` rejects when an input rejects; it does not cancel the other operations.",
    },
    {
        "prompt": "After the current synchronous JavaScript finishes, which is generally processed before a timer task?",
        "options": ["A promise reaction microtask", "A later script download", "A CSS repaint callback", "A new synchronous call stack"],
        "correct_option": 0,
        "explanation": "In browser scheduling, queued microtasks such as promise reactions are generally processed before the next task, such as a timer callback.",
    },
    {
        "prompt": "Which operator returns the right-hand fallback only when the left side is `null` or `undefined`?",
        "options": ["`||`", "`&&`", "`??`", "`?.`"],
        "correct_option": 2,
        "explanation": "The nullish coalescing operator `??` preserves other falsey values such as `0` and an empty string.",
    },
    {
        "prompt": "What kind of values does `localStorage` store?",
        "options": ["String key-value pairs", "Functions and closures", "Only JSON objects", "Binary files by default"],
        "correct_option": 0,
        "explanation": "Web Storage stores keys and values as strings; serialize structured data when needed.",
    },
    {
        "prompt": "Which DOM property should be preferred to display untrusted plain text?",
        "options": ["`innerHTML`", "`textContent`", "`outerHTML`", "`document.write`"],
        "correct_option": 1,
        "explanation": "`textContent` treats the value as text instead of parsing it as HTML, reducing injection risk.",
    },
    {
        "prompt": "What is true of ES modules?",
        "options": [
            "They cannot export values",
            "They are strict mode by default and have their own top-level scope",
            "They share all top-level variables globally",
            "They can only run in Node.js",
        ],
        "correct_option": 1,
        "explanation": "ES modules have module scope and run in strict mode by default; browsers and Node.js support them.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="javascript",
            defaults={"name": "JavaScript", "icon": "code", "order": 21, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="javascript-fundamentals-quiz",
            defaults={
                "title": "JavaScript Fundamentals Quiz",
                "description": "20 questions covering JavaScript values, functions, collections, modules, asynchronous code, and browser APIs.",
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