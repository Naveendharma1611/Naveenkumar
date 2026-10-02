"""Seed the C++ category and its 20-question fundamentals quiz.

Usage: python seed_quiz_cpp.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is the default member access in a C++ `class`?",
        "options": ["public", "private", "protected", "friend"],
        "correct_option": 1,
        "explanation": "Members of a `class` are private by default; members of a `struct` are public by default.",
    },
    {
        "prompt": "Why should a polymorphic base class often have a virtual destructor?",
        "options": [
            "So deleting through a base pointer runs the derived destructor too",
            "So every member function becomes static",
            "So the base class cannot be constructed",
            "So exceptions are disabled",
        ],
        "correct_option": 0,
        "explanation": "A virtual base destructor enables correct derived destruction when deleting through a base-class pointer.",
    },
    {
        "prompt": "What ownership model does `std::unique_ptr` represent?",
        "options": ["Exclusive ownership", "Shared ownership by reference count", "Non-owning observation only", "Ownership by a global registry"],
        "correct_option": 0,
        "explanation": "`unique_ptr` represents exclusive ownership and transfers ownership when moved.",
    },
    {
        "prompt": "How does `std::shared_ptr` manage shared ownership?",
        "options": ["With reference counting", "By copying the object every time", "By borrowing without ownership", "By using a global mutex for every access"],
        "correct_option": 0,
        "explanation": "Shared pointers maintain a reference count and destroy the managed object when the last owner releases it.",
    },
    {
        "prompt": "What is a common use of `std::weak_ptr`?",
        "options": [
            "Observe an object managed by shared pointers without extending its lifetime",
            "Create exclusive ownership that cannot move",
            "Automatically lock every shared pointer",
            "Allocate an object on the stack",
        ],
        "correct_option": 0,
        "explanation": "A weak pointer is non-owning and can help break shared-pointer ownership cycles.",
    },
    {
        "prompt": "What does `std::move(value)` do by itself?",
        "options": [
            "Casts the expression to an rvalue category so move-aware operations may be selected",
            "Always transfers every resource immediately",
            "Deletes the source object",
            "Copies the object into a new allocation",
        ],
        "correct_option": 0,
        "explanation": "`std::move` is a cast; the selected constructor or assignment performs any resource transfer.",
    },
    {
        "prompt": "What does the Rule of Zero recommend?",
        "options": [
            "Compose resource-owning standard types and avoid custom special-member functions when possible",
            "Never create a class with data members",
            "Define all five special-member functions for every class",
            "Use raw pointers for every resource",
        ],
        "correct_option": 0,
        "explanation": "The Rule of Zero favors member types that manage their own resources so the enclosing class needs no custom ownership functions.",
    },
    {
        "prompt": "Which statement about a C++ reference is correct?",
        "options": [
            "It must be initialized and cannot later be reseated to another object",
            "It can always be null",
            "It is reassigned to refer to a new object with `=`",
            "It owns the referenced object automatically",
        ],
        "correct_option": 0,
        "explanation": "A reference is an alias that must be initialized; assignment through it assigns to the referred-to object rather than reseating it.",
    },
    {
        "prompt": "What does `const T* pointer` mean?",
        "options": [
            "A pointer to a const-qualified `T`; the pointer itself may be changed",
            "A const pointer to mutable `T`",
            "A pointer that must be null",
            "An owning smart pointer",
        ],
        "correct_option": 0,
        "explanation": "`const T*` prevents modification of the pointee through that pointer, but the pointer may point elsewhere.",
    },
    {
        "prompt": "What can happen to all pointers and references to vector elements when a `std::vector` reallocates?",
        "options": ["They can all be invalidated", "They are automatically updated", "Only iterators at the end remain valid", "The vector becomes immutable"],
        "correct_option": 0,
        "explanation": "Reallocation moves elements to new storage and invalidates pointers, references, and iterators to the old elements.",
    },
    {
        "prompt": "What iteration order does `std::map` provide?",
        "options": ["Keys are ordered according to the map's comparator", "Insertion order is always preserved", "Keys are randomly shuffled", "Only integer keys are ordered"],
        "correct_option": 0,
        "explanation": "`std::map` iterates in key order according to its comparator.",
    },
    {
        "prompt": "What is the average lookup complexity of `std::unordered_map`?",
        "options": ["Average constant time", "Always logarithmic time", "Always linear time", "Constant time in every possible case"],
        "correct_option": 0,
        "explanation": "Hash-table lookup is average constant time, with linear worst-case behavior.",
    },
    {
        "prompt": "What does a C++ template define?",
        "options": [
            "A family of functions or types parameterized by types or values",
            "A runtime-only plugin loaded from a database",
            "A class that cannot have parameters",
            "A preprocessor comment",
        ],
        "correct_option": 0,
        "explanation": "Templates describe parameterized functions and types that the compiler can instantiate for particular arguments.",
    },
    {
        "prompt": "What does RAII connect a resource's lifetime to?",
        "options": ["The lifetime of an owning object", "The name of the source file", "The number of CPU cores", "The current namespace"],
        "correct_option": 0,
        "explanation": "RAII manages resources through object construction and destruction, including scope exit during exceptions.",
    },
    {
        "prompt": "What makes a class abstract in C++?",
        "options": ["It has at least one pure virtual function", "It has a public constructor", "It contains a `std::string`", "It defines a destructor"],
        "correct_option": 0,
        "explanation": "A class with at least one pure virtual function cannot be instantiated directly.",
    },
    {
        "prompt": "What is object slicing?",
        "options": [
            "Copying a derived object into a base object by value and losing the derived portion",
            "Resizing a vector to zero elements",
            "Splitting a string into tokens",
            "Moving a unique pointer",
        ],
        "correct_option": 0,
        "explanation": "Value-copying a derived object into a base object stores only the base subobject, slicing away derived state.",
    },
    {
        "prompt": "What must a program do with a joinable `std::thread` before its thread object is destroyed?",
        "options": ["Join or detach it", "Move it into a vector only", "Call `std::move` on every argument", "Catch a `std::thread` exception"],
        "correct_option": 0,
        "explanation": "Destroying a joinable thread object calls `std::terminate`; resolve its state with `join` or `detach`.",
    },
    {
        "prompt": "In C++, what is the consequence of a data race?",
        "options": ["Undefined behavior", "A guaranteed exception", "Automatic locking", "A deterministic last-write-wins result"],
        "correct_option": 0,
        "explanation": "Unsynchronized conflicting accesses from multiple threads constitute a data race and cause undefined behavior.",
    },
    {
        "prompt": "What does `std::optional<T>` represent?",
        "options": ["A value that may be present or absent", "A shared thread lock", "A sorted collection", "An exception type"],
        "correct_option": 0,
        "explanation": "`std::optional<T>` can contain a `T` value or represent no value.",
    },
    {
        "prompt": "What is the difference between an exception and undefined behavior?",
        "options": [
            "An exception is a defined control-flow mechanism; undefined behavior has no required program outcome",
            "Undefined behavior is always caught by `catch (...)`",
            "Exceptions and undefined behavior are identical",
            "Exceptions only occur during compilation",
        ],
        "correct_option": 0,
        "explanation": "Exceptions can be handled according to language rules; undefined behavior means the standard imposes no requirements on the result.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="cpp",
            defaults={"name": "C++", "icon": "code", "order": 11, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="cpp-fundamentals-quiz",
            defaults={
                "title": "C++ Fundamentals Quiz",
                "description": "20 questions covering object lifetime, RAII, smart pointers, templates, STL containers, and concurrency.",
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