"""Seed the NumPy category and its 20-question fundamentals quiz.

Usage: python seed_quiz_numpy.py (run from backend/, same venv as manage.py)
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
        "prompt": "What does the `dtype` attribute of an ndarray describe?",
        "options": ["Its number of dimensions", "Its element data type", "Its shape tuple", "Its memory address"],
        "correct_option": 1,
        "explanation": "The dtype describes the type used to represent the array's elements.",
    },
    {
        "prompt": "For an array `a`, what does `a.ndim` report?",
        "options": ["Total element count", "Number of dimensions", "Element data type", "Number of bytes per element"],
        "correct_option": 1,
        "explanation": "`ndim` is the number of axes or dimensions in the array.",
    },
    {
        "prompt": "What must be true when reshaping an array to a new shape?",
        "options": [
            "The new shape must have the same number of dimensions",
            "The new shape must contain the same total number of elements",
            "The array must contain only floating-point numbers",
            "The new shape must be one-dimensional",
        ],
        "correct_option": 1,
        "explanation": "Reshaping must preserve the total number of elements; memory layout determines whether a view or copy is possible.",
    },
    {
        "prompt": "For `a` with shape `(2, 3)`, what is the shape of `a.sum(axis=0)`?",
        "options": ["`(2,)`", "`(3,)`", "`(2, 3)`", "`()`"],
        "correct_option": 1,
        "explanation": "Reducing axis 0 combines the two rows and leaves one result for each of the three columns.",
    },
    {
        "prompt": "What is the shape of the broadcast result for arrays with shapes `(3, 1)` and `(1, 4)`?",
        "options": ["`(3, 4)`", "`(4, 3)`", "`(3, 1, 4)`", "The shapes are incompatible"],
        "correct_option": 0,
        "explanation": "The singleton dimensions expand to produce a result shape of `(3, 4)`.",
    },
    {
        "prompt": "Which operation performs matrix multiplication for NumPy arrays?",
        "options": ["`a * b`", "`a @ b`", "`a + b`", "`a ** b`"],
        "correct_option": 1,
        "explanation": "`@` performs matrix multiplication; `*` is elementwise multiplication.",
    },
    {
        "prompt": "What does `np.arange(0, 5, 2)` produce?",
        "options": ["`[0, 2, 4]`", "`[0, 2, 4, 5]`", "`[2, 4, 5]`", "`[0, 1, 2, 3, 4]`"],
        "correct_option": 0,
        "explanation": "`arange` starts at 0, advances by 2, and excludes the stop value 5.",
    },
    {
        "prompt": "What does `np.linspace(0, 1, 5)` specify?",
        "options": [
            "A step size of 5",
            "Five evenly spaced samples from 0 to 1 by default including the endpoint",
            "Five random values between 0 and 1",
            "An array with shape `(0, 1, 5)`",
        ],
        "correct_option": 1,
        "explanation": "`linspace` takes the desired number of samples; its endpoint is included by default.",
    },
    {
        "prompt": "What does basic slicing such as `a[1:4]` commonly return for an ndarray?",
        "options": ["A view sharing the original data", "Always a deep copy", "A Python set", "A scalar regardless of input"],
        "correct_option": 0,
        "explanation": "Basic slicing commonly returns a view, so changes may be visible through both arrays.",
    },
    {
        "prompt": "What does integer-array advanced indexing commonly return?",
        "options": ["A view of the original data", "A copy of the selected values", "A generator", "A tuple of indexes only"],
        "correct_option": 1,
        "explanation": "Integer-array advanced indexing returns a copy of the selected values.",
    },
    {
        "prompt": "Which expression selects values in `a` that are greater than 10?",
        "options": ["`a > 10`", "`a[a > 10]`", "`a.where(10)`", "`a.filter(10)`"],
        "correct_option": 1,
        "explanation": "`a > 10` creates a Boolean mask, and indexing with that mask selects matching values.",
    },
    {
        "prompt": "Which function detects NaN values in a NumPy array?",
        "options": ["`np.isnull(a)`", "`np.isnan(a)`", "`a == np.nan`", "`np.nancheck(a)`"],
        "correct_option": 1,
        "explanation": "Use `np.isnan` because NaN is not equal to itself.",
    },
    {
        "prompt": "Why is `a == np.nan` not a reliable NaN test?",
        "options": [
            "NaN compares unequal to itself",
            "NaN is always converted to zero",
            "Equality works only for integer arrays",
            "NumPy arrays cannot be compared",
        ],
        "correct_option": 0,
        "explanation": "IEEE floating-point NaN is not equal to any value, including itself; use `np.isnan`.",
    },
    {
        "prompt": "Which is the recommended way to create a modern NumPy random generator?",
        "options": ["`np.random.default_rng(seed)`", "`np.array.random(seed)`", "`np.seed(seed)`", "`np.random.Random(seed)`"],
        "correct_option": 0,
        "explanation": "`np.random.default_rng(seed)` creates a Generator instance for random sampling.",
    },
    {
        "prompt": "What is a NumPy ufunc designed to do?",
        "options": [
            "Operate elementwise on values and participate in broadcasting",
            "Compile Python code into a standalone application",
            "Create only one-dimensional arrays",
            "Sort every array automatically",
        ],
        "correct_option": 0,
        "explanation": "Universal functions apply operations elementwise and support array broadcasting.",
    },
    {
        "prompt": "Which method combines arrays by adding a new axis?",
        "options": ["`np.concatenate`", "`np.stack`", "`np.reshape`", "`np.ravel`"],
        "correct_option": 1,
        "explanation": "`np.stack` combines arrays along a new axis and requires matching input shapes.",
    },
    {
        "prompt": "Which method joins arrays along an existing axis?",
        "options": ["`np.concatenate`", "`np.stack`", "`np.broadcast_to`", "`np.meshgrid`"],
        "correct_option": 0,
        "explanation": "`np.concatenate` joins arrays along an existing axis; other dimensions must be compatible.",
    },
    {
        "prompt": "What does `keepdims=True` do in a reduction?",
        "options": [
            "Keeps the reduced dimensions with length one",
            "Prevents the reduction from running",
            "Converts all values to integers",
            "Keeps only missing values",
        ],
        "correct_option": 0,
        "explanation": "`keepdims=True` retains reduced axes as dimensions of length one, which can help broadcasting.",
    },
    {
        "prompt": "How can you check whether two arrays share underlying memory?",
        "options": ["`np.same_shape(a, b)`", "`np.shares_memory(a, b)`", "`a is b` only", "`np.shared(a, b)`"],
        "correct_option": 1,
        "explanation": "`np.shares_memory` checks whether the arrays share at least one memory location.",
    },
    {
        "prompt": "For two 2D arrays multiplied with `@`, which dimensions must match?",
        "options": [
            "The left array's number of rows and the right array's number of columns",
            "The left array's number of columns and the right array's number of rows",
            "Both arrays must be square",
            "Both arrays must have exactly the same shape",
        ],
        "correct_option": 1,
        "explanation": "Matrix multiplication requires the left operand's column count to equal the right operand's row count.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="numpy",
            defaults={"name": "NumPy", "icon": "code", "order": 30, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="numpy-fundamentals-quiz",
            defaults={
                "title": "NumPy Fundamentals Quiz",
                "description": "20 questions covering ndarray structure, indexing, broadcasting, reductions, randomness, and numerical operations.",
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