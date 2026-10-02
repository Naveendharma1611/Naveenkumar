"""Seed the Machine Learning category and its 20-question fundamentals quiz.

Usage: python seed_quiz_machine_learning.py (run from backend/, same venv as manage.py)
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
        "prompt": "What distinguishes supervised learning from unsupervised learning?",
        "options": [
            "Supervised learning uses examples with target labels",
            "Supervised learning never uses training data",
            "Unsupervised learning always predicts a numeric target",
            "They differ only in programming language",
        ],
        "correct_option": 0,
        "explanation": "Supervised learning uses labeled examples to learn a mapping to a target; unsupervised learning does not require supplied target labels.",
    },
    {
        "prompt": "Which situation is an example of target leakage?",
        "options": [
            "Using a feature that would not be available when the prediction is made",
            "Holding out a test set before model fitting",
            "Comparing a model against a baseline",
            "Scaling features inside a fitted training pipeline",
        ],
        "correct_option": 0,
        "explanation": "A feature containing information unavailable at prediction time can make evaluation unrealistically optimistic.",
    },
    {
        "prompt": "A model fits training data closely but performs poorly on new data. What is the likely issue?",
        "options": ["Overfitting", "Underfitting", "Feature scaling", "Calibration"],
        "correct_option": 0,
        "explanation": "Overfitting occurs when a model captures training-specific patterns that do not generalize.",
    },
    {
        "prompt": "What is a common purpose of regularization?",
        "options": [
            "Increase model complexity without limit",
            "Penalize complexity to reduce overfitting risk",
            "Guarantee perfect training accuracy",
            "Replace the need for validation data",
        ],
        "correct_option": 1,
        "explanation": "Regularization discourages overly complex fits; select its strength with training data or cross-validation.",
    },
    {
        "prompt": "When should an untouched test set generally be used?",
        "options": [
            "For repeatedly selecting features during development",
            "For fitting imputation values before splitting",
            "For a final evaluation after model selection is complete",
            "For choosing every training hyperparameter",
        ],
        "correct_option": 2,
        "explanation": "Repeated development decisions based on test results leak information; reserve it for final evaluation.",
    },
    {
        "prompt": "What does cross-validation commonly estimate?",
        "options": [
            "How performance varies across training and validation folds",
            "Whether a feature causes the target",
            "The exact future score on every deployment dataset",
            "The amount of missing data in a table",
        ],
        "correct_option": 0,
        "explanation": "Cross-validation estimates generalization performance across multiple folds and supports model selection.",
    },
    {
        "prompt": "Why is feature scaling often important for k-nearest neighbors?",
        "options": [
            "Distance calculations can otherwise be dominated by large-scale features",
            "Scaling makes labels unnecessary",
            "k-nearest neighbors accepts only integer features",
            "Scaling removes all outliers",
        ],
        "correct_option": 0,
        "explanation": "Distance-based models can overweight features with larger numeric scales unless scaling is handled appropriately.",
    },
    {
        "prompt": "Logistic regression is commonly used for which task?",
        "options": ["Classification", "Image compression only", "Clustering without labels only", "Sorting records"],
        "correct_option": 0,
        "explanation": "Logistic regression models class probabilities and is commonly used for classification.",
    },
    {
        "prompt": "How does a decision tree typically make a prediction?",
        "options": [
            "By following feature-based splits from a root to a leaf",
            "By computing only the nearest training row",
            "By averaging all feature names alphabetically",
            "By multiplying every feature by the same fixed constant",
        ],
        "correct_option": 0,
        "explanation": "A tree routes an observation through feature-based splits to a leaf that provides its prediction.",
    },
    {
        "prompt": "What is a common effect of bagging trees in a random forest?",
        "options": [
            "Averaging varied trees can reduce prediction variance",
            "Forcing every tree to use exactly the same split",
            "Converting classification into clustering",
            "Guaranteeing that the model is causal",
        ],
        "correct_option": 0,
        "explanation": "Bagging trains trees on resampled data and aggregates them; this often reduces variance compared with a single tree.",
    },
    {
        "prompt": "How does boosting generally build an ensemble?",
        "options": [
            "By adding models sequentially to improve errors or an objective",
            "By selecting one random feature and stopping",
            "By averaging labels without training models",
            "By removing all validation data",
        ],
        "correct_option": 0,
        "explanation": "Boosting adds models in stages, with each stage improving the ensemble according to a loss or error-focused procedure.",
    },
    {
        "prompt": "Which statement about k-nearest neighbors is correct?",
        "options": [
            "It predicts using nearby training examples under a distance measure",
            "It always learns a single linear boundary",
            "It requires no stored training examples at prediction time",
            "It can only solve regression tasks",
        ],
        "correct_option": 0,
        "explanation": "k-nearest neighbors compares an input with stored examples using a distance or similarity measure.",
    },
    {
        "prompt": "Precision is the ratio of which quantities?",
        "options": ["True positives to predicted positives", "True positives to actual positives", "True negatives to all negatives", "Correct predictions to all samples"],
        "correct_option": 0,
        "explanation": "Precision is TP / (TP + FP): among predicted positives, the fraction that are true positives.",
    },
    {
        "prompt": "Recall is the ratio of which quantities?",
        "options": ["True positives to predicted positives", "True positives to actual positives", "True negatives to all predictions", "False positives to all samples"],
        "correct_option": 1,
        "explanation": "Recall is TP / (TP + FN): among actual positives, the fraction identified by the model.",
    },
    {
        "prompt": "For a rare positive class, which evaluation view is often especially informative?",
        "options": ["Precision-recall curve", "Training accuracy alone", "Number of model parameters", "A plot of feature names"],
        "correct_option": 0,
        "explanation": "Precision-recall analysis focuses on positive-class precision and recall and is often informative under substantial class imbalance.",
    },
    {
        "prompt": "Compared with MAE, what does RMSE penalize more strongly?",
        "options": ["Large errors", "Only positive errors", "Missing labels", "Small feature values"],
        "correct_option": 0,
        "explanation": "Squaring residuals before averaging makes RMSE more sensitive to larger errors than MAE.",
    },
    {
        "prompt": "What does principal component analysis (PCA) seek in its standard form?",
        "options": [
            "Directions capturing high variance in a linear projection",
            "A causal graph of all features",
            "A guaranteed class label for each row",
            "The feature with the largest name length",
        ],
        "correct_option": 0,
        "explanation": "PCA finds orthogonal directions ordered by the variance captured in a linear projection of the data.",
    },
    {
        "prompt": "What is the goal of k-means clustering?",
        "options": [
            "Assign observations to clusters around learned centroids",
            "Predict a supervised target with a decision tree",
            "Maximize a classifier's recall threshold",
            "Estimate confidence intervals for a mean only",
        ],
        "correct_option": 0,
        "explanation": "K-means partitions observations into a chosen number of clusters by iteratively updating assignments and centroids.",
    },
    {
        "prompt": "How can a fitted preprocessing pipeline help prevent leakage?",
        "options": [
            "It fits transformations within training folds and applies them to held-out data",
            "It makes every feature independent",
            "It automatically chooses a causal model",
            "It evaluates only on training accuracy",
        ],
        "correct_option": 0,
        "explanation": "A pipeline keeps learned transformations within each training fold and applies the fitted steps to validation data.",
    },
    {
        "prompt": "What does probability calibration assess?",
        "options": [
            "Whether predictions assigned a probability match observed frequencies over comparable cases",
            "Whether all features have zero mean",
            "Whether a model's training score is exactly 100 percent",
            "Whether a model can be compressed into a single feature",
        ],
        "correct_option": 0,
        "explanation": "A calibrated model's predicted probabilities correspond to observed outcome frequencies over groups of similar predictions.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="machine-learning",
            defaults={"name": "Machine Learning", "icon": "brain", "order": 50, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="machine-learning-fundamentals-quiz",
            defaults={
                "title": "Machine Learning Fundamentals Quiz",
                "description": "20 questions covering supervised learning, leakage, validation, algorithms, metrics, and calibration.",
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