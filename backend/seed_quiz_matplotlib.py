"""Seed the Matplotlib category and its 20-question fundamentals quiz.

Usage: python seed_quiz_matplotlib.py (run from backend/, same venv as manage.py)
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
        "prompt": "In Matplotlib, what is the usual relationship between a Figure and an Axes?",
        "options": [
            "A Figure is the overall container and can contain one or more Axes",
            "An Axes is the overall container and can contain multiple Figures",
            "They are two names for a data array",
            "A Figure can only display text, not charts",
        ],
        "correct_option": 0,
        "explanation": "A Figure is the top-level canvas-like container; Axes objects inside it contain plotting areas and chart elements.",
    },
    {
        "prompt": "What is a benefit of Matplotlib's object-oriented interface?",
        "options": [
            "It keeps figure and axes operations explicit, supporting reusable multi-axes code",
            "It automatically chooses a truthful chart for any data",
            "It removes the need to label plots",
            "It prevents saving figures",
        ],
        "correct_option": 0,
        "explanation": "Using explicit Figure and Axes objects makes plotting code clearer and easier to compose or reuse.",
    },
    {
        "prompt": "Which Axes method is commonly used to create a line chart?",
        "options": ["`ax.plot(x, y)`", "`ax.hist(x, y)`", "`ax.imshow(x, y)`", "`ax.box(x, y)`"],
        "correct_option": 0,
        "explanation": "`ax.plot` is commonly used to draw line charts, optionally with markers and a label.",
    },
    {
        "prompt": "Which plot is commonly useful for showing the relationship between two numeric variables?",
        "options": ["Scatter plot", "Pie chart only", "Text title", "Legend"],
        "correct_option": 0,
        "explanation": "A scatter plot displays paired numeric values and can reveal association, clusters, and outliers.",
    },
    {
        "prompt": "What does a histogram show?",
        "options": [
            "A binned distribution of numeric observations",
            "Only the relationship between two named categories",
            "A time series with one point per month by definition",
            "The source code used to create a chart",
        ],
        "correct_option": 0,
        "explanation": "A histogram groups numeric observations into bins to show their distribution.",
    },
    {
        "prompt": "Which chart is a common choice for comparing values across discrete categories?",
        "options": ["Bar chart", "Histogram only", "Colorbar", "Axis spine"],
        "correct_option": 0,
        "explanation": "A bar chart is commonly used to compare values for distinct categories.",
    },
    {
        "prompt": "Why label both axes with units when applicable?",
        "options": [
            "So viewers can interpret what each value measures and in which units",
            "So the chart automatically sorts the data",
            "So every chart is statistically significant",
            "So the legend becomes unnecessary in every case",
        ],
        "correct_option": 0,
        "explanation": "Axis labels and units provide essential context for correctly interpreting plotted values.",
    },
    {
        "prompt": "How can plotted series be identified in a legend?",
        "options": [
            "Set labels on the plotted artists and call `ax.legend()`",
            "Set the Figure's DPI to zero",
            "Call `ax.set_xlim()` only",
            "Change the x-axis unit to a string",
        ],
        "correct_option": 0,
        "explanation": "Assign labels to plotted artists and call `ax.legend()` to display them.",
    },
    {
        "prompt": "What does `fig, ax = plt.subplots()` commonly return?",
        "options": ["A Figure and a single Axes", "Two Figures", "Two arrays of data", "A saved PNG and a PDF"],
        "correct_option": 0,
        "explanation": "With default arguments, `plt.subplots()` returns a Figure and one Axes object.",
    },
    {
        "prompt": "What is one benefit of constrained layout or `tight_layout`?",
        "options": [
            "Reduce overlap among axes, labels, and titles when arranging a figure",
            "Choose the correct statistical test",
            "Remove the need for data validation",
            "Increase the number of observations",
        ],
        "correct_option": 0,
        "explanation": "These layout tools help fit axes decorations and labels into the figure, though complex layouts still need visual checking.",
    },
    {
        "prompt": "What does `sharex=True` commonly do in a grid of subplots?",
        "options": [
            "Share x-axis limits and related axis behavior across the subplots",
            "Combine all y values into one array",
            "Share one legend across every open Figure automatically",
            "Save each subplot as a separate file",
        ],
        "correct_option": 0,
        "explanation": "Shared axes synchronize the selected axis across related subplots and can reduce repeated tick labels.",
    },
    {
        "prompt": "What does the `dpi` argument to `savefig` primarily control for raster output?",
        "options": ["The raster resolution", "The number of plotted data points", "The legend's font family", "The x-axis data type"],
        "correct_option": 0,
        "explanation": "DPI controls dots per inch for rasterized output and affects pixel dimensions at a given figure size.",
    },
    {
        "prompt": "What is a common advantage of saving a figure as PDF?",
        "options": [
            "Many plot elements can remain vector-based and scale cleanly",
            "It always makes the file smaller than PNG",
            "It preserves interactive mouse events in every viewer",
            "It automatically embeds the source dataset",
        ],
        "correct_option": 0,
        "explanation": "PDF can preserve vector elements that scale cleanly, although some artists may be rasterized depending on the plot.",
    },
    {
        "prompt": "Which colormap is commonly a perceptually uniform sequential choice for continuous values?",
        "options": ["`viridis`", "A rainbow palette with arbitrary hue jumps", "A list of unrelated named colors", "A binary transparency mask"],
        "correct_option": 0,
        "explanation": "`viridis` is a perceptually uniform sequential colormap commonly used for ordered continuous values.",
    },
    {
        "prompt": "What does a colorbar explain in a scatter plot whose points are colored by a numeric variable?",
        "options": [
            "The mapping between data values and colors",
            "The order in which Python imported packages",
            "The chart's source file name",
            "The number of Axes in every open Figure",
        ],
        "correct_option": 0,
        "explanation": "A colorbar provides a scale that maps colors to the numeric values encoded by color.",
    },
    {
        "prompt": "Why should a chart not rely on color alone to distinguish important series?",
        "options": [
            "Some viewers may not distinguish the colors, and grayscale output can remove the difference",
            "Color is never supported in Matplotlib",
            "Color always changes the data values",
            "Legends cannot display colored artists",
        ],
        "correct_option": 0,
        "explanation": "Use redundant channels such as markers, line styles, or direct labels for accessibility and grayscale reproduction.",
    },
    {
        "prompt": "Why can a truncated axis be misleading in a bar chart?",
        "options": [
            "Bar length visually encodes magnitude from a baseline, so truncation can exaggerate differences",
            "Bar charts cannot display negative values",
            "It changes the underlying observations",
            "It prevents the legend from being created",
        ],
        "correct_option": 0,
        "explanation": "Bars encode values through length, so a nonzero baseline can visually exaggerate differences and should be clearly justified.",
    },
    {
        "prompt": "What is a potential risk of using a second y-axis with `twinx()`?",
        "options": [
            "Independent scales can make unrelated series appear to move together",
            "It always deletes the first Axes",
            "It converts line data into categories",
            "It prevents the Figure from being saved",
        ],
        "correct_option": 0,
        "explanation": "Independent y-axis limits can visually imply relationships that are artifacts of the chosen scales.",
    },
    {
        "prompt": "Why call `plt.close(fig)` in a batch plotting script?",
        "options": [
            "Release figure resources after saving or displaying them",
            "Delete the source data file",
            "Reset all NumPy arrays to zero",
            "Increase the figure's DPI",
        ],
        "correct_option": 0,
        "explanation": "Closing figures in batch workflows releases resources and avoids accumulating open figures.",
    },
    {
        "prompt": "What do error bars commonly communicate?",
        "options": [
            "A defined measure of variability or uncertainty around an estimate",
            "The exact value of every raw observation",
            "A guarantee that a difference is statistically significant",
            "The number of rows in the source file",
        ],
        "correct_option": 0,
        "explanation": "Error bars can represent standard deviations, standard errors, confidence intervals, or other quantities; label what they mean.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="matplotlib",
            defaults={"name": "Matplotlib", "icon": "analytics", "order": 160, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="matplotlib-fundamentals-quiz",
            defaults={
                "title": "Matplotlib Fundamentals Quiz",
                "description": "20 questions covering the Figure/Axes model, chart types, layout, accessibility, and export.",
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