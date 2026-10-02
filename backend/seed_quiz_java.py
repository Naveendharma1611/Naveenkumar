"""Seed the Java category and its 20-question fundamentals quiz.

Usage: python seed_quiz_java.py (run from backend/, same venv as manage.py)
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
        "prompt": "Which component executes Java bytecode?",
        "options": ["JDK", "JVM", "Javadoc", "JShell"],
        "correct_option": 1,
        "explanation": "The Java Virtual Machine loads and executes Java bytecode.",
    },
    {
        "prompt": "What is the main purpose of the JDK?",
        "options": [
            "Only to execute bytecode without development tools",
            "To provide development tools and runtime components for Java",
            "To replace the operating system",
            "To convert Java into JavaScript",
        ],
        "correct_option": 1,
        "explanation": "The JDK includes tools such as the compiler and debugger, together with runtime components.",
    },
    {
        "prompt": "What does the Java compiler normally produce from a `.java` source file?",
        "options": ["Native machine code for every CPU", "Bytecode in a `.class` file", "A JAR file automatically", "A running JVM process"],
        "correct_option": 1,
        "explanation": "The compiler normally produces JVM bytecode stored in `.class` files.",
    },
    {
        "prompt": "Why is `String` considered immutable in Java?",
        "options": [
            "A String's contents cannot be changed after the object is created",
            "A String variable cannot be reassigned",
            "Strings can only contain constants",
            "String methods are unavailable after construction",
        ],
        "correct_option": 0,
        "explanation": "String operations that appear to modify text return a new String rather than changing the existing object's contents.",
    },
    {
        "prompt": "If two objects are equal according to `equals`, what must be true of their `hashCode` values?",
        "options": [
            "Their hash codes must be different",
            "Their hash codes must be the same",
            "Their hash codes must both be zero",
            "Their hash codes are never used by collections",
        ],
        "correct_option": 1,
        "explanation": "Equal objects must have equal hash codes; unequal objects are allowed to collide.",
    },
    {
        "prompt": "How does method overloading differ from method overriding?",
        "options": [
            "Overloading changes a method's parameter list; overriding supplies a subtype implementation",
            "Overloading applies only to fields; overriding applies only to constructors",
            "They are two names for the same feature",
            "Overriding is resolved only by changing parameter names",
        ],
        "correct_option": 0,
        "explanation": "Overloading uses different parameter lists; overriding replaces a compatible inherited instance method implementation.",
    },
    {
        "prompt": "What does a `static` field belong to?",
        "options": ["Each method invocation", "The class rather than each individual instance", "Only the JVM", "The current thread"],
        "correct_option": 1,
        "explanation": "A static field is associated with the class, not a separate copy on each instance.",
    },
    {
        "prompt": "What does `final` on a class prevent?",
        "options": ["Creating instances", "Calling its methods", "Subclassing that class", "Using it as a variable type"],
        "correct_option": 2,
        "explanation": "A final class cannot be extended by a subclass.",
    },
    {
        "prompt": "Which statement about Java interfaces is correct?",
        "options": [
            "A class can implement multiple interfaces",
            "A class can implement only one interface",
            "Interfaces cannot define any methods",
            "An interface is always instantiated directly",
        ],
        "correct_option": 0,
        "explanation": "A class may implement multiple interfaces, even though it can extend only one class.",
    },
    {
        "prompt": "Which collection is generally a good default for a list with frequent indexed reads?",
        "options": ["ArrayList", "LinkedList", "HashSet", "TreeMap"],
        "correct_option": 0,
        "explanation": "ArrayList supports efficient indexed reads; choose collections based on the actual access pattern.",
    },
    {
        "prompt": "Does `HashMap` guarantee iteration order for its entries?",
        "options": ["Yes, insertion order is always guaranteed", "Yes, sorted-key order is always guaranteed", "No, it does not guarantee a particular iteration order", "Only when keys are strings"],
        "correct_option": 2,
        "explanation": "HashMap does not guarantee a particular iteration order; use LinkedHashMap or TreeMap when that behavior is needed.",
    },
    {
        "prompt": "What is generally required for a checked exception?",
        "options": [
            "It must be caught or declared by the method",
            "It must always be ignored",
            "It must extend `Error`",
            "It cannot be thrown by application code",
        ],
        "correct_option": 0,
        "explanation": "Java requires checked exceptions to be caught or declared in the method signature.",
    },
    {
        "prompt": "What is a key benefit of try-with-resources?",
        "options": [
            "It retries every failed operation automatically",
            "It closes AutoCloseable resources when the block exits",
            "It prevents all exceptions from occurring",
            "It makes every resource thread-safe",
        ],
        "correct_option": 1,
        "explanation": "Resources declared in try-with-resources are closed automatically when the block exits.",
    },
    {
        "prompt": "What does Java generic type erasure mean in general?",
        "options": [
            "Generic type arguments are generally not retained as ordinary runtime type information",
            "The compiler deletes all generic type checking",
            "Every generic value becomes a String",
            "Generic classes cannot be instantiated",
        ],
        "correct_option": 0,
        "explanation": "The compiler enforces generic types, but parameterized type arguments are generally erased from ordinary runtime types.",
    },
    {
        "prompt": "What does `volatile` not guarantee for a shared integer counter?",
        "options": [
            "Visibility of reads and writes to that variable",
            "Ordering guarantees for volatile access",
            "Atomicity of a compound increment operation",
            "That the field is shared between threads",
        ],
        "correct_option": 2,
        "explanation": "Volatile provides visibility and ordering guarantees, but a read-modify-write increment is not atomic.",
    },
    {
        "prompt": "What is a primary purpose of `synchronized`?",
        "options": [
            "To make a class immutable",
            "To provide mutual exclusion around code guarded by the same monitor",
            "To start a new JVM",
            "To make every method static",
        ],
        "correct_option": 1,
        "explanation": "Synchronized code uses a monitor to provide mutual exclusion and memory-visibility guarantees.",
    },
    {
        "prompt": "Why might an application use an `ExecutorService`?",
        "options": [
            "To manage and reuse worker threads for submitted tasks",
            "To convert checked exceptions into unchecked exceptions",
            "To replace the Java compiler",
            "To guarantee tasks always run in submission order",
        ],
        "correct_option": 0,
        "explanation": "An executor manages task submission and worker-thread reuse; ordering depends on the executor and task design.",
    },
    {
        "prompt": "When are intermediate Java Stream operations such as `map` generally evaluated?",
        "options": [
            "Immediately when declared",
            "When a terminal operation triggers the pipeline",
            "Only when a stream is parallel",
            "When the source collection is constructed",
        ],
        "correct_option": 1,
        "explanation": "Stream intermediate operations are lazy; a terminal operation initiates traversal and evaluation.",
    },
    {
        "prompt": "What does dependency injection do?",
        "options": [
            "Supplies a class's dependencies from outside instead of constructing them directly inside it",
            "Automatically encrypts all fields",
            "Removes the need for interfaces",
            "Turns a class into a static utility",
        ],
        "correct_option": 0,
        "explanation": "Dependency injection supplies collaborators externally, reducing coupling and improving testability.",
    },
    {
        "prompt": "What does `Optional<T>` primarily represent?",
        "options": [
            "A value that may be present or absent",
            "A value that is always null",
            "A thread-safe mutable field",
            "A collection that accepts duplicate values only",
        ],
        "correct_option": 0,
        "explanation": "Optional represents a possibly absent value and is commonly useful as a return type.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="java",
            defaults={"name": "Java", "icon": "java", "order": 10, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="java-fundamentals-quiz",
            defaults={
                "title": "Java Fundamentals Quiz",
                "description": "20 questions covering the JVM, object-oriented design, collections, exceptions, generics, concurrency, and streams.",
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