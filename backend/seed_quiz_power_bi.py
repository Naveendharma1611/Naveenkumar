"""Seed the Power BI category and its 20-question fundamentals quiz.

Usage: python seed_quiz_power_bi.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is Power Query primarily used for in Power BI?",
        "options": [
            "Connecting to, shaping, and loading data through repeatable transformation steps",
            "Writing DAX measures only",
            "Creating user accounts for the Power BI service",
            "Replacing the semantic model with a PDF",
        ],
        "correct_option": 0,
        "explanation": "Power Query provides a repeatable data connection and transformation process before data is loaded to the model.",
    },
    {
        "prompt": "What does a fact table commonly contain in a star schema?",
        "options": [
            "Events or measurements at a defined grain, with keys to dimensions",
            "Only descriptive labels and no keys",
            "One row for every report visual",
            "DAX formulas stored as text only",
        ],
        "correct_option": 0,
        "explanation": "A fact table records measurable events at a declared grain and typically references dimension tables through keys.",
    },
    {
        "prompt": "How does a DAX measure generally differ from a calculated column?",
        "options": [
            "A measure is evaluated in filter context; a calculated column is computed per row and stored at refresh",
            "A measure is always stored for every row; a calculated column is never stored",
            "A measure can only return text",
            "There is no difference in evaluation or storage",
        ],
        "correct_option": 0,
        "explanation": "Measures are evaluated for the current query context, while calculated columns are computed row by row and stored in the model.",
    },
    {
        "prompt": "What is filter context in DAX?",
        "options": [
            "The set of filters affecting which model rows a calculation sees",
            "The order of columns in Power Query",
            "A visual's background color",
            "The file format used for a report",
        ],
        "correct_option": 0,
        "explanation": "Filter context is the collection of filters from visuals, slicers, relationships, and DAX expressions that affects a calculation.",
    },
    {
        "prompt": "What is row context in DAX?",
        "options": [
            "The current row being evaluated by a calculated column or iterator",
            "A filter applied only by a report page",
            "The number of rows in a visual",
            "A Power Query connection mode",
        ],
        "correct_option": 0,
        "explanation": "Row context identifies the current row during row-by-row evaluation, such as in a calculated column or iterator.",
    },
    {
        "prompt": "What does `CALCULATE` do in DAX?",
        "options": [
            "Evaluates an expression under a modified filter context",
            "Changes a Power Query column's data type",
            "Creates a new relationship automatically",
            "Sorts a table in the model permanently",
        ],
        "correct_option": 0,
        "explanation": "`CALCULATE` evaluates an expression after adding, modifying, or removing filters in the filter context.",
    },
    {
        "prompt": "What is `SUMX`?",
        "options": [
            "An iterator that evaluates an expression for each row of a table and sums the results",
            "A function that sorts a table by its sum",
            "A relationship type between two tables",
            "A Power Query import connector",
        ],
        "correct_option": 0,
        "explanation": "`SUMX` iterates a table, evaluates its expression for each row, and sums those row results.",
    },
    {
        "prompt": "Why is a star schema often preferred for a Power BI semantic model?",
        "options": [
            "It provides clear fact/dimension roles and predictable filter paths for analysis",
            "It removes the need for data types",
            "It guarantees every DAX measure is correct",
            "It requires every table to have the same number of rows",
        ],
        "correct_option": 0,
        "explanation": "A clear star schema improves understandability and typically supports more predictable filtering and analysis.",
    },
    {
        "prompt": "What is a common difference between Import and DirectQuery storage modes?",
        "options": [
            "Import stores data in the model; DirectQuery queries the source for interactions",
            "DirectQuery always stores a full local copy; Import never loads data",
            "Import cannot use relationships",
            "They differ only in report theme behavior",
        ],
        "correct_option": 0,
        "explanation": "Import loads data into the model and requires refresh; DirectQuery sends queries to the source, with source and feature trade-offs.",
    },
    {
        "prompt": "What is a common purpose of a marked date table?",
        "options": [
            "Provide a continuous date dimension for time-based analysis and time-intelligence patterns",
            "Store user passwords for report access",
            "Replace the fact table's date key",
            "Automatically fix every time zone in source data",
        ],
        "correct_option": 0,
        "explanation": "A date table with unique, continuous dates supports reliable calendar filtering and many time-intelligence calculations.",
    },
    {
        "prompt": "What does Power BI Row-Level Security (RLS) control?",
        "options": [
            "Which model rows a user can see based on assigned roles or identity rules",
            "Which visual types can be placed on a page",
            "Whether the report uses a dark theme",
            "The number of refreshes permitted by a gateway",
        ],
        "correct_option": 0,
        "explanation": "RLS filters model rows for users according to role definitions and, where configured, identity-based rules.",
    },
    {
        "prompt": "What is the difference between Power Query Merge and Append?",
        "options": [
            "Merge joins columns using keys; Append stacks rows from tables",
            "Merge stacks rows; Append joins on a key",
            "Both only rename columns",
            "Append creates a DAX measure",
        ],
        "correct_option": 0,
        "explanation": "Merge combines tables horizontally using matching keys; Append combines rows from compatible tables.",
    },
    {
        "prompt": "Why is the DAX `DIVIDE` function often used instead of the `/` operator?",
        "options": [
            "It supports an alternate result when the denominator is zero or blank",
            "It always converts a measure to a date",
            "It creates a relationship between operands",
            "It sorts the numerator before dividing",
        ],
        "correct_option": 0,
        "explanation": "`DIVIDE` accepts an alternate result for zero or blank denominators, helping define safe ratio behavior.",
    },
    {
        "prompt": "What does a slicer do in a Power BI report?",
        "options": [
            "Provides an interactive filter control for report data",
            "Changes a column's data type during refresh",
            "Creates an RLS role automatically",
            "Replaces the semantic model with a spreadsheet",
        ],
        "correct_option": 0,
        "explanation": "A slicer is a report visual that lets users interactively filter data in connected visuals.",
    },
    {
        "prompt": "What is a common use of drill-through in Power BI?",
        "options": [
            "Navigate to a detail page filtered by the selected entity or context",
            "Change the source database schema",
            "Apply a DAX filter to every workspace",
            "Refresh an on-premises gateway",
        ],
        "correct_option": 0,
        "explanation": "Drill-through carries selected context to a detail page so users can investigate a specific entity or slice.",
    },
    {
        "prompt": "What is one purpose of Performance Analyzer in Power BI Desktop?",
        "options": [
            "Inspect how long report visuals and their queries take to render",
            "Generate passwords for workspace users",
            "Write all measures automatically",
            "Convert every Import model to DirectQuery",
        ],
        "correct_option": 0,
        "explanation": "Performance Analyzer helps identify visual rendering and query time that may need investigation.",
    },
    {
        "prompt": "When might an on-premises data gateway be needed?",
        "options": [
            "When the Power BI service must reach supported data sources inside an on-premises network",
            "Whenever a report contains a slicer",
            "To create a calculated column",
            "To change a report's page size",
        ],
        "correct_option": 0,
        "explanation": "A gateway can provide a secure bridge for supported service operations such as refresh against on-premises data sources.",
    },
    {
        "prompt": "What should be verified after defining an RLS role?",
        "options": [
            "Test as role and verify behavior in the published service with intended users",
            "Only change the report's theme",
            "Delete all dimension tables",
            "Assume desktop preview proves every service identity path",
        ],
        "correct_option": 0,
        "explanation": "Test role filters and service assignment behavior; desktop checks alone do not verify every published identity and sharing path.",
    },
    {
        "prompt": "What does a many-to-many relationship require the modeler to consider?",
        "options": [
            "Ambiguous filter paths and whether a bridge table or clearer dimensional design is appropriate",
            "It always filters more predictably than one-to-many",
            "It removes the need for keys",
            "It can only connect date tables",
        ],
        "correct_option": 0,
        "explanation": "Many-to-many relationships can create ambiguous filter behavior; model the grain and filter paths deliberately, often using a bridge table.",
    },
    {
        "prompt": "What is a key benefit of separating report presentation from a well-designed semantic model?",
        "options": [
            "Measures, relationships, and governed definitions can be reused across reports",
            "Every report automatically gains row-level security",
            "The model no longer needs refresh or quality checks",
            "Visual filters stop affecting measures",
        ],
        "correct_option": 0,
        "explanation": "A shared semantic model can provide reusable relationships, measures, and definitions across multiple reports, subject to governance.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="power-bi",
            defaults={"name": "Power BI", "icon": "analytics", "order": 150, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="power-bi-fundamentals-quiz",
            defaults={
                "title": "Power BI Fundamentals Quiz",
                "description": "20 questions covering data modeling, Power Query, DAX, report interactions, security, and performance.",
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