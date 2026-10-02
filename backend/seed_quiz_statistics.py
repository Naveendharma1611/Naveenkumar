"""Seed the Statistics category and its 20-question fundamentals quiz.

Usage: python seed_quiz_statistics.py (run from backend/, same venv as manage.py)
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
        "prompt": "Which measure of center is generally more resistant to extreme values?",
        "options": ["Mean", "Median", "Range", "Standard deviation"],
        "correct_option": 1,
        "explanation": "The median depends on the ordered position of observations and is less affected by extreme values than the mean.",
    },
    {
        "prompt": "What does standard deviation describe?",
        "options": [
            "The typical spread of values around their mean, in the variable's units",
            "The probability that a hypothesis is true",
            "The number of observations in a sample",
            "The difference between the largest and smallest category labels",
        ],
        "correct_option": 0,
        "explanation": "Standard deviation summarizes dispersion around the mean and is expressed in the original measurement units.",
    },
    {
        "prompt": "What does the standard error of the sample mean quantify?",
        "options": [
            "The estimated variability of the sample mean across repeated samples",
            "The spread of individual values around the median only",
            "The probability that a sample contains an outlier",
            "The size of the measurement unit",
        ],
        "correct_option": 0,
        "explanation": "The standard error describes the sampling variability of an estimator such as the sample mean.",
    },
    {
        "prompt": "If sample size increases while population variability stays similar, what generally happens to the standard error of the mean?",
        "options": ["It decreases", "It increases without bound", "It is always exactly zero", "It becomes the sample median"],
        "correct_option": 0,
        "explanation": "For independent observations, the standard error of the mean is approximately the standard deviation divided by the square root of sample size.",
    },
    {
        "prompt": "What does the Central Limit Theorem describe for many sampling settings?",
        "options": [
            "The sampling distribution of a suitably standardized sample mean becomes approximately normal as sample size grows",
            "Every raw dataset becomes normally distributed when it has many rows",
            "The sample mean always equals the population mean",
            "All observations become independent after sampling",
        ],
        "correct_option": 0,
        "explanation": "Under appropriate conditions, the sampling distribution of the mean approaches normality; this does not mean the raw data become normal.",
    },
    {
        "prompt": "Why does independence matter when calculating uncertainty from a sample?",
        "options": [
            "Dependence can change the estimator's sampling variability and invalidate standard formulas",
            "It guarantees a large effect size",
            "It makes every variable normally distributed",
            "It removes the need to define a population",
        ],
        "correct_option": 0,
        "explanation": "Many standard errors and tests rely on assumptions about independent sampling; dependence may require a different design or analysis.",
    },
    {
        "prompt": "For `P(A and B)`, which expression gives `P(A given B)` when `P(B) > 0`?",
        "options": ["`P(A and B) / P(B)`", "`P(A) + P(B)`", "`P(B) / P(A)`", "`1 - P(A)`"],
        "correct_option": 0,
        "explanation": "Conditional probability is `P(A and B) / P(B)` when the conditioning event has positive probability.",
    },
    {
        "prompt": "What does Bayes' rule help calculate?",
        "options": [
            "A posterior probability by combining a likelihood with prior information",
            "A sample variance without data",
            "A guaranteed causal effect from correlation",
            "A population mean from one observation exactly",
        ],
        "correct_option": 0,
        "explanation": "Bayes' rule updates prior probabilities using the likelihood of observed evidence.",
    },
    {
        "prompt": "Under a specified null hypothesis and model assumptions, what does a p-value represent?",
        "options": [
            "The probability of data at least as extreme as observed",
            "The probability that the null hypothesis is true",
            "The probability the result will replicate exactly",
            "The practical size of the effect",
        ],
        "correct_option": 0,
        "explanation": "A p-value is computed assuming the null and model assumptions; it is not the probability that the null is true.",
    },
    {
        "prompt": "What does a test's significance level alpha specify under its assumptions?",
        "options": [
            "The chosen long-run Type I error rate when the null hypothesis is true",
            "The probability that a specific alternative is true",
            "The expected effect size",
            "The sample's standard deviation",
        ],
        "correct_option": 0,
        "explanation": "The significance level controls the test's Type I error probability under the null, subject to the test assumptions.",
    },
    {
        "prompt": "What is a Type I error?",
        "options": [
            "Rejecting a null hypothesis that is true",
            "Failing to reject a false null hypothesis",
            "Choosing the wrong spreadsheet formula",
            "Obtaining a confidence interval with a wide range",
        ],
        "correct_option": 0,
        "explanation": "A Type I error is a false positive: rejecting the null hypothesis when it is true.",
    },
    {
        "prompt": "What is a Type II error?",
        "options": [
            "Failing to reject a false null hypothesis",
            "Rejecting a true null hypothesis",
            "Measuring an outcome in different units",
            "Using a median instead of a mean",
        ],
        "correct_option": 0,
        "explanation": "A Type II error is a false negative: not rejecting the null when a specified alternative is true.",
    },
    {
        "prompt": "What is statistical power?",
        "options": [
            "The probability of rejecting the null under a specified alternative and design",
            "The probability that any hypothesis is true",
            "The sample's maximum observed value",
            "The number of tests run by a computer",
        ],
        "correct_option": 0,
        "explanation": "Power is the probability that a test rejects the null for a specified alternative, given the design and assumptions.",
    },
    {
        "prompt": "What is the frequentist interpretation of a 95% confidence procedure?",
        "options": [
            "In repeated sampling, about 95% of intervals from the procedure cover the fixed parameter, under its assumptions",
            "There is always a 95% probability this observed interval contains the parameter",
            "The estimate is 95% accurate for every individual",
            "The null hypothesis has a 5% probability of being true",
        ],
        "correct_option": 0,
        "explanation": "The confidence level is the long-run coverage rate of the interval procedure under its assumptions.",
    },
    {
        "prompt": "Which is a common starting test for comparing means from two independent groups with potentially unequal variances?",
        "options": ["Welch's two-sample t-test", "A paired t-test without pairs", "A chi-square test on raw means", "A one-sample sign test on group labels"],
        "correct_option": 0,
        "explanation": "Welch's t-test compares independent group means without assuming equal population variances.",
    },
    {
        "prompt": "For measurements taken on the same participants before and after treatment, what is a common t-test approach?",
        "options": [
            "A paired t-test on within-participant differences",
            "An independent-groups t-test that ignores pairing",
            "A chi-square test on the participant IDs",
            "A one-way ANOVA with no outcome variable",
        ],
        "correct_option": 0,
        "explanation": "A paired t-test analyzes the differences within matched pairs, accounting for the repeated-measures design.",
    },
    {
        "prompt": "A chi-square test of independence is commonly used for what kind of data?",
        "options": ["Counts in categorical combinations", "Means of paired continuous values only", "A single continuous time series only", "The slope of a regression line only"],
        "correct_option": 0,
        "explanation": "A chi-square test of independence assesses association between categorical variables using counts, subject to expected-count assumptions.",
    },
    {
        "prompt": "What does a nonzero correlation between two variables establish by itself?",
        "options": [
            "An association measure, not that one variable caused the other",
            "That changing one variable will change the other",
            "That no confounders exist",
            "That the relationship is linear for every correlation measure",
        ],
        "correct_option": 0,
        "explanation": "Correlation alone does not establish causation or eliminate confounding and other explanations.",
    },
    {
        "prompt": "What is a confounder in an observational study?",
        "options": [
            "A factor related to both an exposure and an outcome that can distort their observed association",
            "A random sample with no missing values",
            "A plot used to display a mean",
            "A parameter that is always held at zero",
        ],
        "correct_option": 0,
        "explanation": "A confounder is associated with exposure and outcome and can bias the observed relationship.",
    },
    {
        "prompt": "Why can testing many hypotheses at the same significance level increase false-positive risk?",
        "options": [
            "The chance of at least one false positive across the family of tests can increase",
            "Each p-value becomes a confidence interval automatically",
            "The sample size becomes zero",
            "All effects become statistically significant by definition",
        ],
        "correct_option": 0,
        "explanation": "Repeated testing can inflate family-wise false-positive risk; use a planned analysis and appropriate multiplicity strategy when needed.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="statistics",
            defaults={"name": "Statistics", "icon": "analytics", "order": 90, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="statistics-fundamentals-quiz",
            defaults={
                "title": "Statistics Fundamentals Quiz",
                "description": "20 questions covering descriptive statistics, probability, inference, test selection, and interpretation.",
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