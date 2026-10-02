"""Seed the AI category and its 20-question fundamentals quiz.

Usage: python seed_quiz_ai.py (run from backend/, same venv as manage.py)
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
        "prompt": "What does an intelligent agent generally do?",
        "options": [
            "Perceive an environment and select actions toward objectives",
            "Only store a static list of answers",
            "Guarantee a correct outcome for every input",
            "Replace the need to define a task",
        ],
        "correct_option": 0,
        "explanation": "An agent uses observations and objectives to choose actions in an environment; its success depends on its design and setting.",
    },
    {
        "prompt": "What is a heuristic used for in informed search?",
        "options": [
            "Estimate remaining cost or distance from a state toward a goal",
            "Encrypt the search frontier",
            "Guarantee that every search has a solution",
            "Remove all repeated states from every possible algorithm",
        ],
        "correct_option": 0,
        "explanation": "A heuristic guides search using an estimate of the remaining cost; properties such as admissibility matter for optimality guarantees.",
    },
    {
        "prompt": "What is supervised machine learning?",
        "options": [
            "Learning a mapping from examples that include target labels",
            "Searching a graph without observing any data",
            "Generating text without an objective or evaluation",
            "Grouping values only by their file names",
        ],
        "correct_option": 0,
        "explanation": "Supervised learning uses labeled examples to estimate a predictive relationship between inputs and targets.",
    },
    {
        "prompt": "What does overfitting mean?",
        "options": [
            "A model captures training-specific patterns that do not generalize well",
            "A model has not been given any training examples",
            "A model's output is always shorter than expected",
            "A dataset contains no missing values",
        ],
        "correct_option": 0,
        "explanation": "Overfitting occurs when a model fits training details or noise and performs worse on new data.",
    },
    {
        "prompt": "Precision is the fraction of which predictions that are correct?",
        "options": ["Predicted positives", "Actual positives", "Predicted negatives", "All features"],
        "correct_option": 0,
        "explanation": "Precision is true positives divided by all predicted positives.",
    },
    {
        "prompt": "Recall is the fraction of which cases that are correctly identified as positive?",
        "options": ["Actual positives", "Predicted positives only", "Actual negatives", "All model parameters"],
        "correct_option": 0,
        "explanation": "Recall is true positives divided by all actual positives.",
    },
    {
        "prompt": "Why are convolutional neural networks often used for image tasks?",
        "options": [
            "They learn local spatial patterns using shared filters",
            "They require no training data",
            "They guarantee perfect image recognition",
            "They store every image as a separate hand-written rule",
        ],
        "correct_option": 0,
        "explanation": "Convolutions use local connectivity and shared filters to learn spatial patterns in images.",
    },
    {
        "prompt": "What does self-attention allow a Transformer layer to do?",
        "options": [
            "Compute context-dependent relationships between sequence positions",
            "Guarantee each token has the same representation",
            "Remove the need for training objectives",
            "Convert all inputs directly into database rows",
        ],
        "correct_option": 0,
        "explanation": "Self-attention lets representations incorporate information from other positions in the input sequence.",
    },
    {
        "prompt": "What is a foundation model?",
        "options": [
            "A broadly trained model that can be adapted to multiple downstream tasks",
            "A database schema for storing images",
            "A model that is guaranteed to be unbiased",
            "A model that never requires evaluation",
        ],
        "correct_option": 0,
        "explanation": "Foundation models are trained broadly and can be adapted or prompted for a range of downstream tasks.",
    },
    {
        "prompt": "What is a hallucination in generative AI?",
        "options": [
            "A plausible-sounding output that is unsupported or incorrect",
            "A guaranteed retrieval result from an authoritative source",
            "A GPU memory allocation strategy",
            "A model that refuses every request",
        ],
        "correct_option": 0,
        "explanation": "A hallucination is generated content that may sound plausible but is unsupported, fabricated, or incorrect.",
    },
    {
        "prompt": "What is the retrieval step in retrieval-augmented generation (RAG) for?",
        "options": [
            "Find relevant external context to provide to a generator",
            "Guarantee every generated statement is true",
            "Replace access-control checks",
            "Train a foundation model from scratch on every question",
        ],
        "correct_option": 0,
        "explanation": "Retrieval supplies relevant context to the generator; retrieval quality, permissions, and answer grounding still need evaluation.",
    },
    {
        "prompt": "What do text embeddings commonly represent?",
        "options": [
            "Text as numeric vectors used to compare semantic relationships",
            "A cryptographic proof that a document is correct",
            "An encrypted copy of the original text",
            "A list of all possible responses from a model",
        ],
        "correct_option": 0,
        "explanation": "Embeddings map text into vector representations that can support similarity search and other downstream operations.",
    },
    {
        "prompt": "What is a tool-using AI agent designed to do?",
        "options": [
            "Select and invoke permitted functions or services to accomplish a task",
            "Execute any action without authorization",
            "Avoid observing tool results",
            "Guarantee exactly-once execution of every external operation",
        ],
        "correct_option": 0,
        "explanation": "Tool-using agents can call functions or services; tools should be narrowly scoped, validated, and permission-checked.",
    },
    {
        "prompt": "Why evaluate an AI system on representative examples beyond its training data?",
        "options": [
            "To estimate generalization and uncover failures on relevant inputs",
            "To guarantee there will be no production incidents",
            "To make training labels unnecessary",
            "To prove every feature is causal",
        ],
        "correct_option": 0,
        "explanation": "Representative evaluation helps measure performance and discover failure modes beyond the examples used for training.",
    },
    {
        "prompt": "What is one way historical bias can enter an AI system?",
        "options": [
            "Training data can reflect unequal past decisions or coverage gaps",
            "Using a validation set always creates bias",
            "A model's file extension determines fairness",
            "All algorithms produce identical outcomes across groups",
        ],
        "correct_option": 0,
        "explanation": "Data can encode historical inequities or omit groups, and modeling choices can preserve or amplify those patterns.",
    },
    {
        "prompt": "What does a human approval gate provide before a consequential automated action?",
        "options": [
            "A review point for checking context and authorizing the action",
            "A guarantee that the model's output is accurate",
            "A substitute for access control",
            "Automatic removal of all model bias",
        ],
        "correct_option": 0,
        "explanation": "An approval gate lets an authorized person review and confirm high-impact or difficult-to-reverse actions.",
    },
    {
        "prompt": "Which practice supports privacy when sending user data to an AI service?",
        "options": [
            "Minimize sensitive data and enforce access and retention rules",
            "Include every available user record in every prompt",
            "Log credentials for easier debugging",
            "Assume a prompt is private without checking service terms",
        ],
        "correct_option": 0,
        "explanation": "Data minimization, authorization, retention controls, and service-specific privacy review reduce exposure risk.",
    },
    {
        "prompt": "What is prompt injection?",
        "options": [
            "Untrusted content attempts to override instructions or misuse a model's tools",
            "A method for calculating standard deviation",
            "A guaranteed way to improve factual accuracy",
            "A type of image convolution",
        ],
        "correct_option": 0,
        "explanation": "Prompt injection uses untrusted instructions, often in retrieved content or user input, to influence model behavior in unintended ways.",
    },
    {
        "prompt": "Why validate model output before using it in an application?",
        "options": [
            "Generated output can be malformed, unsupported, or unsafe for the next operation",
            "A language model always returns valid application data",
            "Validation makes authorization unnecessary",
            "Output validation guarantees fairness",
        ],
        "correct_option": 0,
        "explanation": "Validate schemas, permissions, and safety constraints before rendering output or passing it to tools and downstream systems.",
    },
    {
        "prompt": "What does explainability provide to an AI system's users or reviewers?",
        "options": [
            "Information that helps understand factors behind a model output, with method-specific limits",
            "Proof that the model is always correct",
            "A guarantee that no training data is needed",
            "Automatic deletion of biased examples",
        ],
        "correct_option": 0,
        "explanation": "Explainability methods can provide insight into model behavior, but they do not prove correctness or causality and have limitations.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="ai",
            defaults={"name": "Artificial Intelligence", "icon": "brain", "order": 100, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="ai-fundamentals-quiz",
            defaults={
                "title": "Artificial Intelligence Fundamentals Quiz",
                "description": "20 questions covering intelligent agents, machine learning, generative AI, retrieval, evaluation, and responsible AI.",
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