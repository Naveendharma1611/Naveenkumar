"""Seed the SQL category and its 20-question fundamentals quiz.

Usage: python seed_quiz_sql.py (run from backend/, same venv as manage.py)
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
        "prompt": "Which clause filters individual rows before grouping?",
        "options": ["`WHERE`", "`HAVING`", "`ORDER BY`", "`SELECT`"],
        "correct_option": 0,
        "explanation": "`WHERE` filters rows before grouping and aggregate evaluation.",
    },
    {
        "prompt": "Which clause filters groups after aggregation?",
        "options": ["`WHERE`", "`HAVING`", "`FROM`", "`LIMIT`"],
        "correct_option": 1,
        "explanation": "`HAVING` filters groups, commonly using aggregate conditions.",
    },
    {
        "prompt": "How should a query test whether `manager_id` has no value?",
        "options": ["`manager_id = NULL`", "`manager_id IS NULL`", "`manager_id == NULL`", "`manager_id IN NULL`"],
        "correct_option": 1,
        "explanation": "SQL uses `IS NULL` because NULL represents an unknown or missing value and does not behave like an ordinary comparable value.",
    },
    {
        "prompt": "Which rows does an `INNER JOIN` return?",
        "options": [
            "Rows with matching join values in both inputs",
            "Every row from the left input regardless of a match",
            "Only rows with NULL join values",
            "Every possible pair of rows from both inputs",
        ],
        "correct_option": 0,
        "explanation": "An inner join returns rows for which the join condition matches across both inputs.",
    },
    {
        "prompt": "What does a `LEFT JOIN` preserve?",
        "options": [
            "Every row from the left input, with NULLs for unmatched right-side columns",
            "Only rows that match on both sides",
            "Every row from the right input only",
            "Only rows with duplicate keys",
        ],
        "correct_option": 0,
        "explanation": "A left join retains all left-side rows and fills right-side columns with NULL where no match exists.",
    },
    {
        "prompt": "What does `COUNT(*)` count?",
        "options": ["Rows in the group", "Only non-NULL values in the first column", "Distinct values in every column", "Groups after ordering"],
        "correct_option": 0,
        "explanation": "`COUNT(*)` counts rows; `COUNT(expression)` counts rows where that expression is not NULL.",
    },
    {
        "prompt": "Why is `GROUP BY department_id` used with `SUM(salary)`?",
        "options": [
            "To calculate a separate salary total for each department",
            "To sort employees alphabetically",
            "To remove the salary column",
            "To filter rows before joining",
        ],
        "correct_option": 0,
        "explanation": "Grouping partitions rows by department so an aggregate can be computed per group.",
    },
    {
        "prompt": "What does `SELECT DISTINCT city` do?",
        "options": [
            "Returns unique city values in the result",
            "Sorts cities in descending order",
            "Removes duplicate rows from the table permanently",
            "Counts the number of cities",
        ],
        "correct_option": 0,
        "explanation": "`DISTINCT` removes duplicate result rows for the selected expressions; it does not modify stored data.",
    },
    {
        "prompt": "Which statement about `WHERE` and `HAVING` is correct?",
        "options": [
            "`WHERE` filters rows before grouping; `HAVING` filters groups after grouping",
            "`WHERE` always runs after `HAVING`",
            "`HAVING` can never use aggregate functions",
            "They are identical clauses",
        ],
        "correct_option": 0,
        "explanation": "WHERE operates on rows before grouping, while HAVING filters the grouped results.",
    },
    {
        "prompt": "How does `DENSE_RANK` handle tied ordering values compared with `RANK`?",
        "options": [
            "`DENSE_RANK` does not leave gaps after ties; `RANK` can leave gaps",
            "`DENSE_RANK` removes all tied rows",
            "`RANK` always assigns unique consecutive numbers",
            "They both ignore the `ORDER BY` clause",
        ],
        "correct_option": 0,
        "explanation": "Both assign the same rank to ties; RANK leaves gaps after ties, while DENSE_RANK does not.",
    },
    {
        "prompt": "What is a common purpose of a Common Table Expression introduced with `WITH`?",
        "options": [
            "Name a query result for reuse within the following statement",
            "Create a permanent table automatically",
            "Open a database transaction",
            "Add an index to every referenced table",
        ],
        "correct_option": 0,
        "explanation": "A CTE names a query expression for use by the statement that follows it.",
    },
    {
        "prompt": "What distinguishes a window function from a grouped aggregate in a typical query?",
        "options": [
            "A window function can calculate across related rows while retaining each input row",
            "A window function always deletes duplicate rows",
            "A grouped aggregate always retains every original row",
            "Window functions cannot use `ORDER BY`",
        ],
        "correct_option": 0,
        "explanation": "Window functions compute over related rows while preserving the row-level result; GROUP BY typically collapses rows into groups.",
    },
    {
        "prompt": "What is the main purpose of a foreign key constraint?",
        "options": [
            "Maintain referential integrity between related tables",
            "Guarantee that every query uses an index",
            "Sort rows automatically",
            "Encrypt the referenced values",
        ],
        "correct_option": 0,
        "explanation": "A foreign key constrains references so they point to valid related rows, subject to the database's constraint rules.",
    },
    {
        "prompt": "Which statement best describes a primary key?",
        "options": [
            "A key that uniquely identifies rows and does not allow NULL values",
            "A column that may repeat and contain NULLs freely",
            "A query that runs before every SELECT",
            "An index that always contains every text column",
        ],
        "correct_option": 0,
        "explanation": "A primary key uniquely identifies each row and is non-NULL; a table has one primary key constraint, which can be composite.",
    },
    {
        "prompt": "What does a transaction's atomicity property mean?",
        "options": [
            "The transaction's operations commit as a unit or are rolled back as a unit",
            "Every query runs without a database server",
            "All rows are sorted before commit",
            "The transaction cannot read existing data",
        ],
        "correct_option": 0,
        "explanation": "Atomicity means a transaction is treated as an all-or-nothing unit of work.",
    },
    {
        "prompt": "What is a common trade-off of adding an index?",
        "options": [
            "It can speed some reads but requires storage and can add write overhead",
            "It makes every query faster with no cost",
            "It automatically validates application permissions",
            "It prevents updates to the table",
        ],
        "correct_option": 0,
        "explanation": "Indexes can improve selected access patterns but consume storage and must be maintained during writes.",
    },
    {
        "prompt": "What is a common goal of database normalization?",
        "options": [
            "Reduce avoidable redundancy and update anomalies through a suitable schema",
            "Store every value in one text column",
            "Remove all foreign keys",
            "Guarantee that no query uses a join",
        ],
        "correct_option": 0,
        "explanation": "Normalization organizes data to reduce redundancy and anomalies, balanced against the application's query needs.",
    },
    {
        "prompt": "How should an application safely include a user-supplied value in a SQL query?",
        "options": [
            "Pass it as a bound parameter through the database driver",
            "Concatenate it directly into the SQL string",
            "Remove spaces and concatenate it",
            "Encode it as HTML and concatenate it",
        ],
        "correct_option": 0,
        "explanation": "Parameterized queries keep data separate from SQL syntax and help prevent SQL injection.",
    },
    {
        "prompt": "What does `UNION ALL` do compared with `UNION`?",
        "options": [
            "Keeps duplicate result rows instead of removing them",
            "Sorts the result by every column",
            "Combines tables with different column counts",
            "Deletes duplicates from the source tables",
        ],
        "correct_option": 0,
        "explanation": "UNION removes duplicate result rows; UNION ALL preserves them and can avoid the deduplication work.",
    },
    {
        "prompt": "Which database transaction outcome is appropriate if a multi-step update fails partway through?",
        "options": [
            "Roll back the transaction when the operations must succeed together",
            "Commit the partial result by default",
            "Delete the database schema",
            "Disable the foreign-key constraints permanently",
        ],
        "correct_option": 0,
        "explanation": "When steps form one logical unit, a failure should roll back the transaction so partial changes are not committed.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="sql",
            defaults={"name": "SQL", "icon": "database", "order": 70, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="sql-fundamentals-quiz",
            defaults={
                "title": "SQL Fundamentals Quiz",
                "description": "20 questions covering filtering, joins, grouping, window functions, constraints, transactions, and query safety.",
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