"""Seed the Excel category and its 20-question fundamentals quiz.

Usage: python seed_quiz_excel.py (run from backend/, same venv as manage.py)
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
        "prompt": "Which reference keeps both the row and column fixed when a formula is copied?",
        "options": ["`A1`", "`$A$1`", "`A$1`", "`$A1`"],
        "correct_option": 1,
        "explanation": "The dollar signs in `$A$1` anchor both the column and row.",
    },
    {
        "prompt": "What happens to a relative reference such as `A1` when its formula is copied one column to the right?",
        "options": [
            "It normally shifts to `B1`",
            "It always remains `A1`",
            "It changes to `$A$1`",
            "It is removed from the formula",
        ],
        "correct_option": 0,
        "explanation": "Relative references adjust according to the formula's new position.",
    },
    {
        "prompt": "Which function adds values using multiple criteria ranges?",
        "options": ["`SUMIF`", "`SUMIFS`", "`COUNTIFS`", "`SUBTOTAL`"],
        "correct_option": 1,
        "explanation": "`SUMIFS` adds values that satisfy multiple criteria; `SUMIF` handles one criteria range.",
    },
    {
        "prompt": "Which function counts records matching multiple criteria?",
        "options": ["`COUNTA`", "`COUNTIF`", "`COUNTIFS`", "`SUMPRODUCT`"],
        "correct_option": 2,
        "explanation": "`COUNTIFS` counts rows whose corresponding ranges meet all specified criteria.",
    },
    {
        "prompt": "What does the first argument of `IF(logical_test, value_if_true, value_if_false)` represent?",
        "options": ["The result when the test is false", "The condition to evaluate", "A range to sum", "The error message"],
        "correct_option": 1,
        "explanation": "The logical test determines which of the two result arguments is returned.",
    },
    {
        "prompt": "What is the default match mode of modern `XLOOKUP`?",
        "options": ["Exact match", "Approximate match only", "Wildcard match only", "Case-sensitive match"],
        "correct_option": 0,
        "explanation": "XLOOKUP defaults to exact matching unless another match mode is specified.",
    },
    {
        "prompt": "What does the fourth argument `FALSE` request in `VLOOKUP`?",
        "options": ["Approximate match", "Exact match", "A case-sensitive match", "Return the last match"],
        "correct_option": 1,
        "explanation": "Setting the range_lookup argument to FALSE requests an exact match.",
    },
    {
        "prompt": "Which error commonly indicates that a lookup did not find a matching value?",
        "options": ["`#N/A`", "`#REF!`", "`#DIV/0!`", "`#NAME?`"],
        "correct_option": 0,
        "explanation": "`#N/A` commonly indicates that a lookup or match operation did not find a result.",
    },
    {
        "prompt": "What does `IFERROR(value, value_if_error)` do?",
        "options": [
            "Returns the fallback when evaluating the first expression produces an error",
            "Converts every value to text",
            "Prevents a formula from recalculating",
            "Counts error cells in a range",
        ],
        "correct_option": 0,
        "explanation": "IFERROR returns its second argument when the first expression evaluates to an error.",
    },
    {
        "prompt": "What is a key benefit of formatting a data range as an Excel Table?",
        "options": [
            "Structured references and automatic expansion with added rows",
            "It permanently removes formulas",
            "It converts every value to text",
            "It prevents filtering or sorting",
        ],
        "correct_option": 0,
        "explanation": "Tables provide structured references and typically expand to include adjacent data added to the table.",
    },
    {
        "prompt": "What is a PivotTable primarily used for?",
        "options": [
            "Summarizing and exploring data by categories and aggregations",
            "Writing VBA code automatically",
            "Validating a password",
            "Replacing every source record with a chart",
        ],
        "correct_option": 0,
        "explanation": "PivotTables let users group, aggregate, and explore source data interactively.",
    },
    {
        "prompt": "What does a slicer provide for a PivotTable or connected report?",
        "options": [
            "An interactive visual filter",
            "A formula auditing trace",
            "A database relationship key",
            "A replacement for a worksheet name",
        ],
        "correct_option": 0,
        "explanation": "A slicer is an interactive visual control for filtering connected PivotTables or supported data objects.",
    },
    {
        "prompt": "What is the typical Power Query workflow?",
        "options": [
            "Import data, transform it, load it, and refresh when needed",
            "Format cells, run a macro, and delete the source",
            "Create a PivotChart, then rename a worksheet",
            "Write formulas only in VBA",
        ],
        "correct_option": 0,
        "explanation": "Power Query supports repeatable data import and transformation, followed by loading and refresh.",
    },
    {
        "prompt": "What does the Excel Data Model enable?",
        "options": [
            "Related tables and measures for analysis across multiple tables",
            "Only formatting on one worksheet",
            "Automatic protection from incorrect source data",
            "Editing CSV files as databases without import",
        ],
        "correct_option": 0,
        "explanation": "The Data Model supports related tables and analytical calculations such as measures over multiple tables.",
    },
    {
        "prompt": "How does a DAX measure generally differ from a calculated column?",
        "options": [
            "A measure is evaluated in filter context; a calculated column is computed for rows and stored",
            "A measure is always stored in each worksheet cell",
            "A calculated column can only contain text",
            "There is no difference in evaluation or storage",
        ],
        "correct_option": 0,
        "explanation": "Measures are evaluated in the current filter context; calculated columns are computed per row and stored in the model.",
    },
    {
        "prompt": "What happens when a dynamic-array formula returns multiple values?",
        "options": [
            "Results spill into neighboring cells if the spill range is available",
            "Only the first result can ever be displayed",
            "Excel automatically creates a new workbook",
            "Every result is written into a comment",
        ],
        "correct_option": 0,
        "explanation": "Dynamic-array results spill into adjacent cells; blocked spill ranges produce a spill error.",
    },
    {
        "prompt": "Which function returns rows that meet a condition in modern Excel?",
        "options": ["`FILTER`", "`ROUND`", "`SUBTOTAL`", "`INDIRECT`"],
        "correct_option": 0,
        "explanation": "FILTER returns an array of rows or values matching a Boolean include condition.",
    },
    {
        "prompt": "What does Data Validation commonly do?",
        "options": [
            "Restricts or guides which values can be entered in a cell",
            "Changes every formula into a value",
            "Builds a relationship between two tables",
            "Creates a PivotChart from the current selection",
        ],
        "correct_option": 0,
        "explanation": "Data Validation can constrain input, for example to a range, list, date, or permitted text length.",
    },
    {
        "prompt": "What is conditional formatting used for?",
        "options": [
            "Applying visual formatting when cell values meet rules",
            "Changing the underlying value into a formula",
            "Creating a worksheet from each row",
            "Protecting a workbook with a password",
        ],
        "correct_option": 0,
        "explanation": "Conditional formatting applies visual styles based on cell values or specified rules.",
    },
    {
        "prompt": "Which limitation applies to a typical CSV file compared with an Excel workbook?",
        "options": [
            "It stores plain delimited text rather than multiple sheets, formulas, and workbook formatting",
            "It can only store numeric values",
            "It cannot be opened by spreadsheet software",
            "It automatically preserves charts and PivotTables",
        ],
        "correct_option": 0,
        "explanation": "CSV stores delimited text values and does not preserve workbook features such as multiple sheets, formatting, formulas, or charts.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="excel",
            defaults={"name": "Excel", "icon": "spreadsheet", "order": 120, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="excel-fundamentals-quiz",
            defaults={
                "title": "Excel Fundamentals Quiz",
                "description": "20 questions covering references, formulas, lookups, PivotTables, Power Query, and the Data Model.",
                "category": category,
                "difficulty": Quiz.Difficulty.EASY,
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