"""Seed the Pandas category and its 20-question fundamentals quiz.

Usage: python seed_quiz_pandas.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is the main difference between a pandas Series and a DataFrame?",
        "options": [
            "A Series is one-dimensional; a DataFrame is two-dimensional",
            "A Series can only store strings",
            "A DataFrame can only store numeric values",
            "They are unrelated to tabular data",
        ],
        "correct_option": 0,
        "explanation": "A Series is a labeled one-dimensional array; a DataFrame is a labeled two-dimensional structure with columns.",
    },
    {
        "prompt": "What does `.loc` primarily use to select rows and columns?",
        "options": ["Labels and Boolean conditions", "Integer positions only", "Memory addresses", "SQL table names"],
        "correct_option": 0,
        "explanation": "`.loc` is label-oriented and also accepts Boolean masks; `.iloc` selects by integer position.",
    },
    {
        "prompt": "What does `.iloc` use for selection?",
        "options": ["Integer positions", "Index labels only", "Column value names", "File offsets"],
        "correct_option": 0,
        "explanation": "`.iloc` selects rows and columns by zero-based integer position.",
    },
    {
        "prompt": "Which method is the standard way to detect missing values in a DataFrame?",
        "options": ["`df.isna()`", "`df == NaN`", "`df.missing()`", "`df.isnullvalue()`"],
        "correct_option": 0,
        "explanation": "Use `isna()` (or its alias `isnull()`) because missing values such as NaN do not compare equal to themselves.",
    },
    {
        "prompt": "What does `groupby(...).agg(...)` generally produce?",
        "options": [
            "A summary with aggregated results for each group",
            "A DataFrame with exactly the original row count in every case",
            "A sorted copy of every source file",
            "A Boolean mask only",
        ],
        "correct_option": 0,
        "explanation": "Aggregation reduces each group to one or more summary values, so the result commonly has fewer rows.",
    },
    {
        "prompt": "How does `groupby(...).transform(...)` commonly differ from aggregation?",
        "options": [
            "It returns values aligned to the original rows, often with the same length",
            "It always returns one row per group",
            "It converts every column to a string",
            "It merges with a second DataFrame automatically",
        ],
        "correct_option": 0,
        "explanation": "A group transform returns results aligned with the original index, which makes it useful for adding group-level values to rows.",
    },
    {
        "prompt": "What does a left merge preserve when each left key has at most one match on the right?",
        "options": [
            "All rows from the left DataFrame",
            "Only keys present in both DataFrames",
            "All rows from the right DataFrame only",
            "No rows with missing values",
        ],
        "correct_option": 0,
        "explanation": "A left join preserves every left row; duplicate right-side keys may still multiply rows, so validate the relationship.",
    },
    {
        "prompt": "What does the `many_to_one` validation mode check in `DataFrame.merge`?",
        "options": [
            "The right-side merge keys are unique for the relationship",
            "Both input DataFrames have exactly one row",
            "The result contains no missing values",
            "The merge keys are sorted alphabetically",
        ],
        "correct_option": 0,
        "explanation": "For a many-to-one merge, pandas checks that each key on the right appears at most once.",
    },
    {
        "prompt": "What does `pd.concat([a, b], axis=0)` commonly do?",
        "options": ["Stacks objects along the row axis", "Joins on matching key values", "Pivots columns into rows", "Sorts both objects in place"],
        "correct_option": 0,
        "explanation": "Concatenation along axis 0 appends objects row-wise, aligning their columns by labels.",
    },
    {
        "prompt": "What is `DataFrame.melt` commonly used for?",
        "options": [
            "Reshape wide data into a longer key-value form",
            "Remove rows with missing data",
            "Aggregate every numeric column",
            "Join two tables using a foreign key",
        ],
        "correct_option": 0,
        "explanation": "`melt` unpivots selected columns into variable and value columns, producing a long-form table.",
    },
    {
        "prompt": "What does `pivot_table` provide that `pivot` does not generally provide for duplicate index/column combinations?",
        "options": [
            "An aggregation function to summarize duplicate combinations",
            "Automatic file encryption",
            "A guarantee that the output is sorted by every column",
            "A replacement for all missing values",
        ],
        "correct_option": 0,
        "explanation": "`pivot_table` aggregates duplicate combinations using an aggregation function; `pivot` requires unique combinations.",
    },
    {
        "prompt": "Which is an explicit pattern for assigning to rows selected by a condition?",
        "options": [
            "`df.loc[mask, score_column] = value`",
            "`df[mask][score_column] = value`",
            "`df.where = value`",
            "`df.assign(mask, value)`",
        ],
        "correct_option": 0,
        "explanation": "Use `.loc[mask, column] = value` for explicit assignment and to avoid ambiguous chained indexing.",
    },
    {
        "prompt": "What does coercion do to values `pd.to_datetime` cannot parse?",
        "options": ["Converts them to `NaT`", "Raises an error for every invalid value", "Converts them to today's date", "Drops their rows automatically"],
        "correct_option": 0,
        "explanation": "With coercion enabled, invalid date values are represented as `NaT`.",
    },
    {
        "prompt": "What is one benefit of using `usecols` when reading a large CSV?",
        "options": [
            "It can reduce memory and parsing work by loading only needed columns",
            "It automatically validates all business rules",
            "It removes duplicate rows",
            "It guarantees numeric dtypes for every field",
        ],
        "correct_option": 0,
        "explanation": "Reading only required columns can reduce I/O, parsing, and memory use.",
    },
    {
        "prompt": "What should you check after a merge that is expected to preserve a one-to-one relationship?",
        "options": [
            "Key uniqueness and expected row counts before and after the merge",
            "Only the color of the resulting chart",
            "Only whether the output index starts at zero",
            "The order in which columns appear in the source file only",
        ],
        "correct_option": 0,
        "explanation": "Validate key cardinality and reconcile row counts to detect dropped or multiplied records.",
    },
    {
        "prompt": "What does `drop_duplicates(subset=[id_column])` do?",
        "options": [
            "Keep one row per distinct `id` value according to the chosen keep rule",
            "Delete the `id` column",
            "Sort the DataFrame by `id`",
            "Fill missing IDs from neighboring rows",
        ],
        "correct_option": 0,
        "explanation": "`drop_duplicates` removes duplicate rows based on selected columns and a configurable keep policy.",
    },
    {
        "prompt": "Why can a categorical dtype reduce memory usage?",
        "options": [
            "Repeated labels can be stored as category codes plus a shared category set",
            "It deletes all repeated values",
            "It compresses every numeric column losslessly",
            "It stores each label as a Python function",
        ],
        "correct_option": 0,
        "explanation": "Categorical data can store repeated values as integer codes referencing a shared set of categories, especially useful for low-cardinality columns.",
    },
    {
        "prompt": "What does the pandas `.str` accessor provide?",
        "options": [
            "Vectorized string operations on string-like Series values",
            "A string conversion for every DataFrame in memory",
            "A database connection string",
            "A regular expression compiler only",
        ],
        "correct_option": 0,
        "explanation": "The `.str` accessor exposes string operations across Series values without writing a Python loop for each row.",
    },
    {
        "prompt": "What is commonly required to use `resample` on a time series?",
        "options": [
            "A datetime-like index or a datetime column specified with `on`",
            "A unique integer index only",
            "A categorical column as the index",
            "A DataFrame with exactly one row",
        ],
        "correct_option": 0,
        "explanation": "Resampling groups time-indexed data into frequency bins and requires datetime-like values in the index or an `on` column.",
    },
    {
        "prompt": "Why is vectorized pandas or NumPy code often preferred over iterating row by row in Python?",
        "options": [
            "It can move work into optimized array operations and reduce Python-level loop overhead",
            "It always uses zero memory",
            "It guarantees that the calculation is statistically valid",
            "It automatically prevents every data-quality problem",
        ],
        "correct_option": 0,
        "explanation": "Vectorized operations often use optimized lower-level implementations and avoid much per-row Python overhead; correctness still requires validation.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="pandas",
            defaults={"name": "Pandas", "icon": "analytics", "order": 140, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="pandas-fundamentals-quiz",
            defaults={
                "title": "Pandas Fundamentals Quiz",
                "description": "20 questions covering Series and DataFrames, selection, cleaning, aggregation, joins, reshaping, and performance.",
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