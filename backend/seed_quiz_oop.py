"""Seed the OOP category and its 20-question fundamentals quiz.

Usage: python seed_quiz_oop.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is the difference between a class and an object?",
        "options": [
            "A class defines a type; an object is a particular instance",
            "An object is a file; a class is a database row",
            "A class is always a function and an object is always a string",
            "They are interchangeable terms in every language",
        ],
        "correct_option": 0,
        "explanation": "A class describes structure or behavior; an object is a concrete runtime instance with identity and state.",
    },
    {
        "prompt": "What is encapsulation primarily intended to do?",
        "options": [
            "Protect state and expose a deliberate interface",
            "Make every field public",
            "Prevent objects from calling methods",
            "Guarantee that a class has no dependencies",
        ],
        "correct_option": 0,
        "explanation": "Encapsulation groups state and behavior behind an interface that can enforce invariants and hide implementation details.",
    },
    {
        "prompt": "What does abstraction provide to a caller?",
        "options": [
            "Useful operations and guarantees without requiring implementation details",
            "Access to every private field",
            "A guarantee that the implementation never changes",
            "Automatic persistence for all object state",
        ],
        "correct_option": 0,
        "explanation": "An abstraction describes what a client can do and rely on while hiding how the behavior is implemented.",
    },
    {
        "prompt": "When is inheritance generally the best fit?",
        "options": [
            "When a subtype is substitutable for a base type under its contract",
            "Whenever two classes share one line of code",
            "Whenever one object stores another object",
            "When a class needs to call a database",
        ],
        "correct_option": 0,
        "explanation": "Inheritance is most appropriate for a genuine is-a relationship where the subtype preserves the base type's promises.",
    },
    {
        "prompt": "What is polymorphism?",
        "options": [
            "Using different implementations through a shared contract",
            "Storing multiple values in one integer",
            "Making every method static",
            "Copying a class definition into each object",
        ],
        "correct_option": 0,
        "explanation": "Polymorphism allows client code to use multiple implementations through a common interface or contract.",
    },
    {
        "prompt": "Which relationship is most naturally represented by composition?",
        "options": ["A service has a repository collaborator", "A square is a kind of shape", "A number is less than another number", "A method overrides a base method"],
        "correct_option": 0,
        "explanation": "Composition models a has-a or collaboration relationship, such as a service using a repository.",
    },
    {
        "prompt": "What does the Liskov Substitution Principle require?",
        "options": [
            "A valid subtype should preserve behavior expected by base-type clients",
            "Every class must have exactly one subclass",
            "Subtypes must expose all implementation fields publicly",
            "Base classes may not define methods",
        ],
        "correct_option": 0,
        "explanation": "Subtypes should be usable where the base contract is expected without violating its behavioral guarantees.",
    },
    {
        "prompt": "What is the Single Responsibility Principle about?",
        "options": [
            "Keeping a module's responsibilities cohesive around a primary reason to change",
            "Limiting every class to one method",
            "Ensuring every function has one parameter",
            "Forbidding classes from collaborating",
        ],
        "correct_option": 0,
        "explanation": "The principle encourages cohesive responsibilities; it does not require one method or one field per class.",
    },
    {
        "prompt": "What does the Interface Segregation Principle recommend?",
        "options": [
            "Prefer small client-focused interfaces over forcing clients to depend on unused methods",
            "Combine every interface into one global interface",
            "Avoid using interfaces in all designs",
            "Make every interface expose internal state",
        ],
        "correct_option": 0,
        "explanation": "Clients should not be forced to depend on operations they do not use; cohesive interfaces reduce unnecessary coupling.",
    },
    {
        "prompt": "What is dependency injection?",
        "options": [
            "Supplying an object's collaborators from outside instead of constructing them internally",
            "Copying a dependency's source code into a class",
            "Making all collaborators global variables",
            "Removing all dependencies from a program",
        ],
        "correct_option": 0,
        "explanation": "Dependency injection makes collaborators explicit and replaceable, often improving testability and configuration.",
    },
    {
        "prompt": "Which is more naturally modeled as a value object?",
        "options": [
            "A two-dimensional coordinate defined by its x and y values",
            "A user account tracked through changes over time by a stable ID",
            "A database server process",
            "A shopping session whose lifecycle is audited by identity",
        ],
        "correct_option": 0,
        "explanation": "A coordinate is commonly defined by its values; an entity such as an account is commonly tracked by identity over time.",
    },
    {
        "prompt": "Why can immutability simplify object-oriented design?",
        "options": [
            "An object's state cannot change unexpectedly after construction",
            "It guarantees every algorithm is constant time",
            "It removes the need for equality rules",
            "It prevents objects from being shared",
        ],
        "correct_option": 0,
        "explanation": "Immutable objects reduce shared-state surprises and are often easier to reason about, though updates may require replacement objects.",
    },
    {
        "prompt": "How do method overloading and overriding differ?",
        "options": [
            "Overloading offers different parameter signatures; overriding supplies a subtype implementation",
            "Overloading changes object state; overriding creates a class",
            "They always mean the same thing",
            "Overriding can only apply to constructors",
        ],
        "correct_option": 0,
        "explanation": "Overloading distinguishes operations by signatures; overriding changes inherited behavior while maintaining a compatible contract.",
    },
    {
        "prompt": "What should a constructor generally ensure?",
        "options": [
            "The new object begins in a valid state with required invariants established",
            "Every method has already been called once",
            "The object is saved to a database automatically",
            "The object's fields are public",
        ],
        "correct_option": 0,
        "explanation": "Construction should establish required state so callers do not receive a partially initialized object.",
    },
    {
        "prompt": "Which design pattern encapsulates interchangeable algorithms behind a common contract?",
        "options": ["Strategy", "Observer", "Adapter", "Singleton"],
        "correct_option": 0,
        "explanation": "Strategy lets a client select among interchangeable behaviors through a shared interface.",
    },
    {
        "prompt": "Which design pattern is commonly used to notify subscribers when an event or subject changes?",
        "options": ["Observer", "Factory", "Adapter", "Builder"],
        "correct_option": 0,
        "explanation": "Observer defines a notification relationship from a subject or event source to interested subscribers.",
    },
    {
        "prompt": "Which design pattern can translate one interface into another expected by a client?",
        "options": ["Adapter", "Strategy", "Observer", "Prototype"],
        "correct_option": 0,
        "explanation": "An Adapter wraps an existing component and exposes the interface a client expects.",
    },
    {
        "prompt": "What does the Open/Closed Principle encourage?",
        "options": [
            "Allow expected behavior extension without repeatedly changing stable policy code",
            "Never modify any source file",
            "Put every behavior in a subclass",
            "Make every field immutable",
        ],
        "correct_option": 0,
        "explanation": "The principle encourages extension points for expected variation, without forbidding justified changes to existing code.",
    },
    {
        "prompt": "How can object-oriented code with external collaborators be tested effectively?",
        "options": [
            "Test public behavior and inject controlled fakes at external boundaries",
            "Mock every private method and assert call order only",
            "Avoid tests because dynamic dispatch is unpredictable",
            "Use production credentials for every unit test",
        ],
        "correct_option": 0,
        "explanation": "Behavior-focused tests with controlled collaborators verify contracts without coupling every test to private implementation details.",
    },
    {
        "prompt": "What is a good reason to introduce an interface or abstraction?",
        "options": [
            "A real client boundary needs substitution, independent change, or a stable contract",
            "Every concrete class must have an interface with the same name",
            "A program should maximize the number of files",
            "Inheritance is unavailable in the chosen language",
        ],
        "correct_option": 0,
        "explanation": "Introduce an abstraction when it clarifies a real boundary or expected variation; unnecessary layers increase complexity.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="oop",
            defaults={"name": "Object-Oriented Programming", "icon": "code", "order": 28, "is_published": True},
        )
        if category.name != "Object-Oriented Programming" or not category.is_published:
            category.name = "Object-Oriented Programming"
            category.is_published = True
            category.save(update_fields=["name", "is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="oop-fundamentals-quiz",
            defaults={
                "title": "OOP Fundamentals Quiz",
                "description": "20 questions covering classes, encapsulation, inheritance, polymorphism, composition, SOLID principles, patterns, and testing.",
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