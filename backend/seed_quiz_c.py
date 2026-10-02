"""Seed the C category and its 20-question fundamentals quiz.

Usage: python seed_quiz_c.py (run from backend/, same venv as manage.py)
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
        "prompt": "Within the scope where `values` is declared as an actual array, what does `sizeof values` report?",
        "options": [
            "The total size in bytes of the array",
            "The number of elements in every context",
            "The size of the first element only",
            "The size of a pointer on the system",
        ],
        "correct_option": 0,
        "explanation": "`sizeof` applied to an actual array in its defining scope reports the total bytes of the array object.",
    },
    {
        "prompt": "What does `sizeof(pointer)` report when `pointer` is an `int *`?",
        "options": [
            "The size of the pointer object",
            "The size of the pointed-to array",
            "The number of pointed-to integers",
            "The size of one `int`",
        ],
        "correct_option": 0,
        "explanation": "`sizeof` on a pointer reports the size of the pointer object, not the allocation it may point to.",
    },
    {
        "prompt": "What commonly happens to an array expression in most C expressions?",
        "options": [
            "It converts to a pointer to its first element",
            "It becomes a copy of the full array",
            "It converts to an integer count",
            "It is freed automatically",
        ],
        "correct_option": 0,
        "explanation": "In most expressions an array converts to a pointer to its first element, with important exceptions such as `sizeof` and unary `&`.",
    },
    {
        "prompt": "What is a null pointer guaranteed to indicate?",
        "options": [
            "It does not point to an object or function",
            "It points to the first array element",
            "It points to address zero as a portable physical address",
            "It can be safely dereferenced once",
        ],
        "correct_option": 0,
        "explanation": "A null pointer compares unequal to every pointer to an object or function and must not be dereferenced.",
    },
    {
        "prompt": "Within which range is pointer arithmetic on an array pointer defined?",
        "options": [
            "Within the same array object or one past its end",
            "Across any two adjacent allocations",
            "At any numeric address in memory",
            "Only at the first element",
        ],
        "correct_option": 0,
        "explanation": "Pointer arithmetic may produce pointers within the same array object or one past its end; the one-past pointer cannot be dereferenced.",
    },
    {
        "prompt": "What terminates a C string?",
        "options": ["A null character `\\0`", "A newline in every case", "A space character", "The array's last allocated byte automatically"],
        "correct_option": 0,
        "explanation": "A C string is terminated by a null character, and its buffer must include space for that terminator.",
    },
    {
        "prompt": "When `fgets` reads a newline before filling its buffer, what does it normally do?",
        "options": [
            "Stores the newline and then appends a terminating null character",
            "Removes every whitespace character",
            "Stores no characters",
            "Appends a second newline after the buffer",
        ],
        "correct_option": 0,
        "explanation": "`fgets` retains a newline if it is read and has room, then null-terminates the stored string.",
    },
    {
        "prompt": "Why should code check the return value of `scanf`?",
        "options": [
            "It reports how many input items were successfully assigned",
            "It gives the current file size",
            "It always returns the number of bytes in the buffer",
            "It validates memory allocation",
        ],
        "correct_option": 0,
        "explanation": "The return value is the number of input items successfully matched and assigned, which may be fewer than expected.",
    },
    {
        "prompt": "What should a program do if `malloc` returns `NULL`?",
        "options": [
            "Handle allocation failure before using the pointer",
            "Dereference the pointer once to test it",
            "Call `free` on an unrelated pointer",
            "Assume the allocation has succeeded",
        ],
        "correct_option": 0,
        "explanation": "A failed allocation returns a null pointer; check it before accessing allocated storage.",
    },
    {
        "prompt": "How does `calloc` differ from `malloc`?",
        "options": [
            "It allocates an array and initializes the allocated bytes to zero",
            "It always returns stack storage",
            "It never fails",
            "It automatically frees memory after one use",
        ],
        "correct_option": 0,
        "explanation": "`calloc` allocates space for an array and sets its bytes to zero; check for allocation failure and size overflow.",
    },
    {
        "prompt": "Why assign `realloc` to a temporary pointer first?",
        "options": [
            "If it fails, the original allocation remains available to free or use",
            "It guarantees the allocation is always enlarged in place",
            "It automatically initializes all new bytes to zero",
            "It prevents all pointer arithmetic",
        ],
        "correct_option": 0,
        "explanation": "For a nonzero requested size, a failed `realloc` leaves the original allocation intact; a temporary prevents losing its pointer.",
    },
    {
        "prompt": "What happens when `free(NULL)` is called?",
        "options": ["Nothing", "The program must terminate", "It allocates one byte", "It frees every allocation in the process"],
        "correct_option": 0,
        "explanation": "Passing a null pointer to `free` has no effect.",
    },
    {
        "prompt": "What is a use-after-free?",
        "options": [
            "Accessing an object through a pointer after its allocation has been released",
            "Calling `free` with a null pointer",
            "Reading a valid local variable before returning",
            "Allocating an array with `calloc`",
        ],
        "correct_option": 0,
        "explanation": "Using an object after its lifetime or allocated storage has ended is invalid and can cause undefined behavior.",
    },
    {
        "prompt": "What is a typical property of a block-scope `static` variable?",
        "options": [
            "It retains its value between function calls",
            "It is recreated and initialized on every call",
            "It is visible in every source file",
            "It must be allocated with `malloc`",
        ],
        "correct_option": 0,
        "explanation": "A block-scope static object has static storage duration and retains its stored value between calls.",
    },
    {
        "prompt": "What does `static` on a function defined at file scope generally do?",
        "options": [
            "Gives the function internal linkage to the current translation unit",
            "Makes the function run only once",
            "Makes all its parameters constant",
            "Places the function on the stack",
        ],
        "correct_option": 0,
        "explanation": "A file-scope static function has internal linkage and is not callable by name from other translation units.",
    },
    {
        "prompt": "What does an `extern` declaration commonly indicate for a file-scope object?",
        "options": [
            "The object is defined in another translation unit",
            "The object is local to a block",
            "The object has no type",
            "The object is automatically freed",
        ],
        "correct_option": 0,
        "explanation": "An extern declaration commonly refers to an object with external linkage whose definition is provided elsewhere.",
    },
    {
        "prompt": "Which operator accesses a structure member through a structure pointer `p`?",
        "options": ["`->`", "`.`", "`::`", "`#`"],
        "correct_option": 0,
        "explanation": "The `->` operator accesses a member through a structure pointer; `.` is used with a structure object.",
    },
    {
        "prompt": "What does the qualifier in `const int *p` prevent?",
        "options": [
            "Modifying the pointed-to integer through `p`",
            "Changing `p` to point elsewhere",
            "Reading the pointed-to integer",
            "Passing `p` to another function",
        ],
        "correct_option": 0,
        "explanation": "The pointed-to integer cannot be modified through this pointer, although the pointer itself may be reassigned.",
    },
    {
        "prompt": "What is undefined behavior in C?",
        "options": [
            "Behavior for which the C standard imposes no requirements",
            "A runtime error that must always print a diagnostic",
            "A syntax error caught before compilation",
            "A defined exception that can be handled with `catch`",
        ],
        "correct_option": 0,
        "explanation": "Undefined behavior has no required result under the C standard, so the program must not rely on a particular outcome.",
    },
    {
        "prompt": "What should a program do after successfully opening a file with `fopen`?",
        "options": [
            "Check the result, use the stream as needed, then close it with `fclose`",
            "Assume the file pointer can never be null",
            "Call `free` on the `FILE` pointer directly",
            "Keep the stream open for the rest of the process in every case",
        ],
        "correct_option": 0,
        "explanation": "Check for a null result from `fopen` and close a successfully opened stream with `fclose` when finished.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="c",
            defaults={"name": "C", "icon": "code", "order": 100, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="c-fundamentals-quiz",
            defaults={
                "title": "C Fundamentals Quiz",
                "description": "20 questions covering arrays, pointers, memory management, strings, linkage, and safe file I/O.",
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