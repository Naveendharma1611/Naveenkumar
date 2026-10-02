"""Seed the Seaborn category and its 20-question fundamentals quiz.

Usage: python seed_quiz_seaborn.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is tidy data's common structure?",
        "options": [
            "Each variable is a column, each observation is a row, and each observational unit forms a table",
            "Each observation is a column and each variable is a workbook",
            "Every value must be stored in a separate file",
            "Columns are ordered alphabetically and rows are grouped by color",
        ],
        "correct_option": 0,
        "explanation": "Tidy data commonly assigns variables to columns, observations to rows, and observational units to tables.",
    },
    {
        "prompt": "What is a common distinction between an axes-level Seaborn function and a figure-level function?",
        "options": [
            "Axes-level functions draw on one Axes; figure-level functions manage a figure-level grid and facets",
            "Axes-level functions only load files; figure-level functions only save files",
            "Figure-level functions cannot use data frames",
            "They are identical in return type and layout behavior",
        ],
        "correct_option": 0,
        "explanation": "Axes-level functions draw on a provided or current Axes; figure-level functions manage larger layouts and commonly support faceting.",
    },
    {
        "prompt": "Which function is a common starting point for a histogram of one numeric variable?",
        "options": ["`sns.histplot`", "`sns.heatmap`", "`sns.countplot`", "`sns.pairplot`"],
        "correct_option": 0,
        "explanation": "`histplot` shows a numeric distribution using bins and can optionally overlay a KDE estimate.",
    },
    {
        "prompt": "What does a KDE plot estimate?",
        "options": [
            "A smoothed estimate of a variable's probability density",
            "The exact count of every category",
            "A regression coefficient with no assumptions",
            "A matrix of pairwise missing values only",
        ],
        "correct_option": 0,
        "explanation": "Kernel density estimation creates a smoothed estimate of a continuous distribution; bandwidth affects the smoothness.",
    },
    {
        "prompt": "What does an ECDF plot show?",
        "options": [
            "The fraction of observations at or below each value",
            "Only the mean and standard error of a category",
            "A matrix of correlations",
            "The number of columns in a DataFrame",
        ],
        "correct_option": 0,
        "explanation": "An empirical cumulative distribution function maps values to the cumulative fraction of observations at or below them.",
    },
    {
        "prompt": "Which plot is commonly useful for visualizing the relationship between two numeric variables?",
        "options": ["`scatterplot`", "`countplot`", "`heatmap`", "`boxenplot` only"],
        "correct_option": 0,
        "explanation": "A scatterplot displays paired numeric values and can encode additional variables with hue, size, or style.",
    },
    {
        "prompt": "What should you consider when a lineplot has repeated observations at the same x value?",
        "options": [
            "The function may aggregate estimates and uncertainty; inspect or set the estimator and error-bar behavior deliberately",
            "It always plots every observation as an unrelated line",
            "It automatically proves a causal trend",
            "It drops every repeated x value without notice",
        ],
        "correct_option": 0,
        "explanation": "Seaborn's relational estimators can aggregate repeated observations; configure and interpret the estimator and uncertainty display intentionally.",
    },
    {
        "prompt": "What does `countplot` commonly display?",
        "options": ["Counts of observations in categorical groups", "A continuous probability density only", "A correlation matrix", "A sequence of date ticks only"],
        "correct_option": 0,
        "explanation": "`countplot` displays the number of observations in each categorical group.",
    },
    {
        "prompt": "What does a boxplot commonly summarize?",
        "options": [
            "Median, quartiles, and whisker range according to its rule",
            "Every raw observation as a separate line",
            "A fitted regression equation only",
            "The mean with no information about spread",
        ],
        "correct_option": 0,
        "explanation": "A boxplot summarizes a distribution with quartiles, median, and whiskers; outlier display depends on the whisker rule.",
    },
    {
        "prompt": "What additional distribution information can a violin plot communicate compared with a basic boxplot?",
        "options": [
            "A smoothed density shape around the distribution",
            "The exact identity of every observation by default",
            "A guaranteed causal effect",
            "The source database's schema",
        ],
        "correct_option": 0,
        "explanation": "A violin plot overlays a density estimate, which can reveal distribution shape but depends on smoothing choices.",
    },
    {
        "prompt": "What is the `hue` semantic commonly used for?",
        "options": [
            "Represent another variable using color grouping",
            "Set the plot's x-axis scale to logarithmic",
            "Choose the number of rows in a facet grid",
            "Rename the DataFrame index",
        ],
        "correct_option": 0,
        "explanation": "`hue` maps a variable to color, often to compare groups within the same plot.",
    },
    {
        "prompt": "What does the `col` parameter commonly do in a Seaborn function that supports faceting?",
        "options": [
            "Create separate subplot facets for levels of the `site` variable",
            "Color the x-axis label by site name only",
            "Drop every row whose site is missing",
            "Set the figure's DPI based on the number of sites",
        ],
        "correct_option": 0,
        "explanation": "Figure-level functions can create a grid of facets, with each panel showing a subset such as one level of a variable.",
    },
    {
        "prompt": "What is a typical use of `pairplot`?",
        "options": [
            "Quickly inspect pairwise relationships among several numeric variables",
            "Display a single categorical count only",
            "Create an interactive map",
            "Validate database foreign keys",
        ],
        "correct_option": 0,
        "explanation": "`pairplot` creates pairwise plots among selected variables and can be useful for an exploratory overview of smaller datasets.",
    },
    {
        "prompt": "What is a common input to `sns.heatmap`?",
        "options": [
            "A two-dimensional matrix or table of numeric values to encode by color",
            "A list of image file paths only",
            "A single string label",
            "An HTTP response object",
        ],
        "correct_option": 0,
        "explanation": "A heatmap encodes values from a two-dimensional matrix-like input with color.",
    },
    {
        "prompt": "When is a sequential colormap generally appropriate?",
        "options": [
            "For ordered values progressing from lower to higher magnitude",
            "For unrelated categories that must have no ordering",
            "For hiding missing observations",
            "For encoding two opposing directions around a meaningful midpoint only",
        ],
        "correct_option": 0,
        "explanation": "Sequential palettes are appropriate for ordered values; diverging or qualitative palettes serve different data structures.",
    },
    {
        "prompt": "Why might an Axes-level Seaborn function accept an `ax=` argument?",
        "options": [
            "To draw the plot on a specific Matplotlib Axes in a custom layout",
            "To select the database connection",
            "To return the original DataFrame without plotting",
            "To override all Seaborn themes globally",
        ],
        "correct_option": 0,
        "explanation": "Passing `ax=` lets an axes-level function draw within a Matplotlib subplot layout that the caller controls.",
    },
    {
        "prompt": "What is one benefit of `sns.set_theme`?",
        "options": [
            "Apply consistent plotting defaults such as style, context, and palette",
            "Validate every statistical assumption automatically",
            "Convert a DataFrame to tidy format",
            "Create a different Figure for each column automatically",
        ],
        "correct_option": 0,
        "explanation": "`set_theme` configures consistent visual defaults for Seaborn and Matplotlib plots.",
    },
    {
        "prompt": "What is a useful way to reduce overplotting in a dense scatter plot?",
        "options": [
            "Use transparency, sample carefully, or switch to a binned density display",
            "Increase marker size until points overlap completely",
            "Remove axis labels",
            "Use a different random color for every point only",
        ],
        "correct_option": 0,
        "explanation": "Transparency, sampling, hexbinning, or two-dimensional binning can make dense data patterns more interpretable.",
    },
    {
        "prompt": "Why should a barplot estimate be supplemented by distribution inspection when appropriate?",
        "options": [
            "A summary estimate can hide spread, skew, or multimodality within groups",
            "Barplots cannot display numeric values",
            "A barplot automatically removes uncertainty",
            "Distribution plots are always more accurate than raw data",
        ],
        "correct_option": 0,
        "explanation": "A group estimate and interval can conceal underlying distribution shape; inspect raw or distributional views when that shape matters.",
    },
    {
        "prompt": "What should be considered when selecting colors for a Seaborn plot?",
        "options": [
            "Whether the palette matches the data type and remains distinguishable and accessible",
            "Whether every category is represented only by red or green",
            "Whether the palette has the most possible colors regardless of groups",
            "Whether color can replace all labels and legends",
        ],
        "correct_option": 0,
        "explanation": "Choose qualitative, sequential, or diverging palettes based on the data and use redundant encodings for accessibility.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="seaborn",
            defaults={"name": "Seaborn", "icon": "analytics", "order": 190, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="seaborn-fundamentals-quiz",
            defaults={
                "title": "Seaborn Fundamentals Quiz",
                "description": "20 questions covering tidy data, plot selection, distributions, relationships, facets, and visual design.",
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