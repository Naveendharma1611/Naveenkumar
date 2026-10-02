"""Seed the Data Science category and its 20-question fundamentals quiz.

Usage: python seed_quiz_data_science.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is a key distinction between supervised and unsupervised learning?",
        "options": [
            "Supervised learning uses labeled targets; unsupervised learning does not require supplied targets",
            "Unsupervised learning can only use images",
            "Supervised learning never uses training data",
            "They are identical approaches with different names",
        ],
        "correct_option": 0,
        "explanation": "Supervised methods learn from examples with target labels; unsupervised methods seek structure without a supplied target.",
    },
    {
        "prompt": "What is the unit of analysis in a dataset?",
        "options": [
            "The smallest numeric value in a column",
            "What one row or observation represents",
            "The number of columns in a table",
            "The file format used to store the data",
        ],
        "correct_option": 1,
        "explanation": "The unit of analysis defines the entity or event represented by each observation.",
    },
    {
        "prompt": "What is data leakage in model evaluation?",
        "options": [
            "Using information unavailable at prediction time or allowing evaluation data to influence fitting",
            "Compressing a dataset before saving it",
            "Dropping duplicate rows from raw data",
            "Using a model with too few parameters",
        ],
        "correct_option": 0,
        "explanation": "Leakage lets information unavailable to a legitimate prediction enter training or evaluation, inflating apparent performance.",
    },
    {
        "prompt": "Why should learned preprocessing be fit only on the training partition?",
        "options": [
            "To prevent information from validation or test data influencing the fitted transformation",
            "To make the test partition larger",
            "Because validation data cannot contain numbers",
            "To eliminate the need for a baseline",
        ],
        "correct_option": 0,
        "explanation": "Fitting transformations on the full dataset can leak information from held-out data into model development.",
    },
    {
        "prompt": "What is a common purpose of cross-validation?",
        "options": [
            "Estimate performance across multiple training/validation partitions",
            "Replace all data quality checks",
            "Guarantee a model will never overfit",
            "Make an independent test set unnecessary in every project",
        ],
        "correct_option": 0,
        "explanation": "Cross-validation evaluates across multiple folds and helps estimate variability and select models using training data.",
    },
    {
        "prompt": "A model that is too simple to capture important patterns is most associated with which issue?",
        "options": ["High bias", "High variance", "Data drift", "Target encoding"],
        "correct_option": 0,
        "explanation": "High bias is associated with an overly constrained model that underfits relevant patterns.",
    },
    {
        "prompt": "What is one purpose of regularization?",
        "options": [
            "Discourage excessive model complexity or large parameter values",
            "Guarantee zero training error",
            "Make every feature causal",
            "Remove the need for validation data",
        ],
        "correct_option": 0,
        "explanation": "Regularization penalizes complexity to reduce overfitting risk; its strength should be selected without using the final test set.",
    },
    {
        "prompt": "Precision is calculated as which ratio?",
        "options": ["TP / (TP + FP)", "TP / (TP + FN)", "TN / (TN + FP)", "(TP + TN) / all cases"],
        "correct_option": 0,
        "explanation": "Precision is true positives divided by all predicted positives: TP / (TP + FP).",
    },
    {
        "prompt": "Recall is calculated as which ratio?",
        "options": ["TP / (TP + FP)", "TP / (TP + FN)", "TN / (TN + FN)", "FP / (FP + TN)"],
        "correct_option": 1,
        "explanation": "Recall is true positives divided by all actual positives: TP / (TP + FN).",
    },
    {
        "prompt": "Why can accuracy be misleading for a highly imbalanced classification problem?",
        "options": [
            "A model can predict the majority class most of the time and still ignore the minority class",
            "Accuracy cannot be calculated for classifiers",
            "Accuracy always gives the same value as recall",
            "Imbalanced data contains no labels",
        ],
        "correct_option": 0,
        "explanation": "A majority-class predictor can have high accuracy while failing to identify the minority class of interest.",
    },
    {
        "prompt": "Compared with MAE, what does RMSE emphasize more strongly?",
        "options": ["Larger errors", "Only negative errors", "Errors in a different unit", "Missing values only"],
        "correct_option": 0,
        "explanation": "Squaring errors before averaging causes RMSE to penalize larger errors more heavily than MAE.",
    },
    {
        "prompt": "What should you investigate before choosing an imputation method for missing data?",
        "options": [
            "Why values are missing and whether missingness relates to other variables or the outcome",
            "Only the color palette of the final chart",
            "Whether the model has the largest possible parameter count",
            "The row order in the CSV file",
        ],
        "correct_option": 0,
        "explanation": "The missingness mechanism and its relationship to the problem help determine whether exclusion, imputation, or indicators are defensible.",
    },
    {
        "prompt": "What is confounding in an observational analysis?",
        "options": [
            "A factor related to both exposure and outcome that can distort their observed relationship",
            "A random seed used during model training",
            "A chart with two axes",
            "A method for sorting a dataset",
        ],
        "correct_option": 0,
        "explanation": "A confounder is associated with both exposure and outcome and can bias an observed association.",
    },
    {
        "prompt": "Under a specified null hypothesis and assumptions, what does a p-value describe?",
        "options": [
            "The probability of data at least as extreme as observed",
            "The probability that the null hypothesis is true",
            "The probability that a result will replicate exactly",
            "The size of the effect in practical units",
        ],
        "correct_option": 0,
        "explanation": "A p-value is calculated assuming the null and model assumptions; it is not the probability that the null is true.",
    },
    {
        "prompt": "What does a frequentist 95% confidence procedure mean in repeated sampling?",
        "options": [
            "About 95% of intervals constructed by the procedure would contain the fixed parameter, under its assumptions",
            "There is always a 95% probability that this one interval contains the parameter",
            "The estimate is correct 95% of the time",
            "The data contain no sampling uncertainty",
        ],
        "correct_option": 0,
        "explanation": "The confidence level describes the long-run coverage of the procedure under its assumptions.",
    },
    {
        "prompt": "Why is random assignment useful in an A/B test?",
        "options": [
            "It helps balance measured and unmeasured factors between groups in expectation",
            "It guarantees every participant responds",
            "It removes the need to define a metric",
            "It proves that all observed differences are large",
        ],
        "correct_option": 0,
        "explanation": "Random assignment supports causal comparison by balancing factors between groups in expectation, subject to sound implementation and analysis.",
    },
    {
        "prompt": "Why build a simple baseline before a complex model?",
        "options": [
            "To establish a clear reference for whether added complexity improves the decision",
            "To guarantee the complex model will outperform it",
            "To avoid defining a success metric",
            "To eliminate all uncertainty in the data",
        ],
        "correct_option": 0,
        "explanation": "A baseline provides a reproducible reference and can expose unnecessary complexity or evaluation mistakes.",
    },
    {
        "prompt": "What is data drift?",
        "options": [
            "A change in the distribution of model input data",
            "A change in the model's source code formatting",
            "A fixed train/test split",
            "A type of confidence interval",
        ],
        "correct_option": 0,
        "explanation": "Data drift describes changes in input distributions; concept drift describes changes in the input-target relationship.",
    },
    {
        "prompt": "What information is useful for making an analysis reproducible?",
        "options": [
            "Code, data provenance and versions, dependencies, parameters, and regeneration steps",
            "Only a screenshot of the final chart",
            "Only the name of the algorithm",
            "Only the random seed",
        ],
        "correct_option": 0,
        "explanation": "Reproduction requires enough information about inputs, code, environment, parameters, and process; a seed alone is insufficient.",
    },
    {
        "prompt": "Which practice helps prevent a test set from influencing model selection?",
        "options": [
            "Evaluate many candidate models on the test set and pick the best",
            "Keep the test set untouched until final evaluation and use cross-validation for selection",
            "Fit preprocessing on the full dataset before splitting",
            "Remove the test labels before model training but tune against them repeatedly",
        ],
        "correct_option": 1,
        "explanation": "Repeated selection based on test results leaks test information into development; use training data and cross-validation for selection.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="data-science",
            defaults={"name": "Data Science", "icon": "analytics", "order": 40, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="data-science-fundamentals-quiz",
            defaults={
                "title": "Data Science Fundamentals Quiz",
                "description": "20 questions covering problem framing, data quality, validation, statistics, metrics, and responsible analysis.",
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