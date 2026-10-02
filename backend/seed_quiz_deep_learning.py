"""Seed the Deep Learning category and its 20-question fundamentals quiz.

Usage: python seed_quiz_deep_learning.py (run from backend/, same venv as manage.py)
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
        "prompt": "What does a typical artificial neuron compute before applying an activation?",
        "options": [
            "A weighted sum of inputs plus a bias",
            "A random class label only",
            "The maximum value of the entire training set",
            "A database join",
        ],
        "correct_option": 0,
        "explanation": "A neuron typically computes a weighted sum of its inputs plus a bias, then applies an activation function.",
    },
    {
        "prompt": "What is the goal of gradient descent during training?",
        "options": [
            "Update parameters in a direction that reduces the loss",
            "Increase the loss after every batch",
            "Remove the training labels",
            "Choose a new test set after each epoch",
        ],
        "correct_option": 0,
        "explanation": "Gradient descent uses loss gradients to update parameters toward lower objective values.",
    },
    {
        "prompt": "What mathematical rule is central to backpropagation?",
        "options": ["The chain rule", "The binomial theorem", "The pigeonhole principle", "Bayes' rule only"],
        "correct_option": 0,
        "explanation": "Backpropagation applies the chain rule to compute derivatives through a composed network.",
    },
    {
        "prompt": "What is one epoch in model training?",
        "options": [
            "One complete pass through the training dataset",
            "One update using exactly one training example",
            "One evaluation on the test dataset",
            "One layer in a neural network",
        ],
        "correct_option": 0,
        "explanation": "An epoch is one pass through the training examples, often divided into multiple batches.",
    },
    {
        "prompt": "What does the learning rate control?",
        "options": [
            "The scale of parameter updates during optimization",
            "The number of labels in the dataset",
            "The number of test examples",
            "The activation function's output type only",
        ],
        "correct_option": 0,
        "explanation": "The learning rate scales optimizer updates; values that are too large can destabilize training.",
    },
    {
        "prompt": "Training loss is low but validation loss is high. What is a likely concern?",
        "options": ["Overfitting", "Underfitting", "Perfect generalization", "A missing activation in every layer"],
        "correct_option": 0,
        "explanation": "A large training/validation gap often indicates overfitting or an unrepresentative validation setup.",
    },
    {
        "prompt": "What is a common purpose of dropout during training?",
        "options": [
            "Regularize a network by randomly disabling some activations during training",
            "Increase the number of labels in a batch",
            "Replace the loss function",
            "Guarantee that validation accuracy increases",
        ],
        "correct_option": 0,
        "explanation": "Dropout randomly masks activations during training and can reduce co-adaptation; it is disabled in evaluation mode.",
    },
    {
        "prompt": "Why are convolutional layers useful for image data?",
        "options": [
            "They apply shared filters to local spatial patterns",
            "They require every pixel to be an independent model",
            "They remove the need for labeled data in every task",
            "They sort image pixels alphabetically",
        ],
        "correct_option": 0,
        "explanation": "Convolutions use local connectivity and shared filters to detect spatial patterns across an image.",
    },
    {
        "prompt": "What is a common effect of pooling in a CNN?",
        "options": [
            "Reduce spatial resolution while summarizing local neighborhoods",
            "Increase the number of image channels to infinity",
            "Shuffle labels between images",
            "Convert a classification task into regression automatically",
        ],
        "correct_option": 0,
        "explanation": "Pooling aggregates local regions and commonly reduces spatial dimensions.",
    },
    {
        "prompt": "What kind of data is naturally suited to recurrent neural network processing?",
        "options": ["Ordered sequences", "Unrelated scalar constants only", "Database schemas", "Unordered file names only"],
        "correct_option": 0,
        "explanation": "RNNs process ordered sequences while carrying a hidden state between steps.",
    },
    {
        "prompt": "What do LSTM gates help control?",
        "options": [
            "Information retained, added to, or removed from the cell state",
            "The order of database migrations",
            "The number of image labels only",
            "Whether the optimizer computes gradients at all",
        ],
        "correct_option": 0,
        "explanation": "LSTM gates regulate information flow through the cell state and hidden state.",
    },
    {
        "prompt": "What is a central mechanism in a Transformer?",
        "options": ["Attention", "A fixed convolution kernel only", "A linked list of database rows", "A hard-coded class lookup table"],
        "correct_option": 0,
        "explanation": "Attention lets a model compute context-dependent relationships between positions in its input.",
    },
    {
        "prompt": "Why do Transformer models need positional information for ordered sequences?",
        "options": [
            "Self-attention alone does not inherently encode token order",
            "To remove all token embeddings",
            "To ensure every token has the same representation",
            "To convert text into a CNN automatically",
        ],
        "correct_option": 0,
        "explanation": "Positional encodings or embeddings provide order information that self-attention alone does not inherently represent.",
    },
    {
        "prompt": "What does softmax commonly produce from a vector of class logits?",
        "options": [
            "Normalized nonnegative values summing to one",
            "A sorted list of input examples",
            "A binary mask with no probabilities",
            "A guaranteed calibrated probability distribution",
        ],
        "correct_option": 0,
        "explanation": "Softmax maps logits to normalized nonnegative class scores that sum to one; calibration is not guaranteed.",
    },
    {
        "prompt": "Which objective is commonly used for single-label multiclass classification?",
        "options": ["Cross-entropy loss", "Mean absolute error only", "K-means inertia", "Cosine distance only"],
        "correct_option": 0,
        "explanation": "Cross-entropy is a common objective for classification over mutually exclusive classes.",
    },
    {
        "prompt": "What does gradient clipping help prevent?",
        "options": [
            "An excessively large gradient update",
            "Every model from learning any parameters",
            "The validation set from being evaluated",
            "The forward pass from computing outputs",
        ],
        "correct_option": 0,
        "explanation": "Gradient clipping limits gradient magnitude and can mitigate unstable large updates, such as exploding gradients.",
    },
    {
        "prompt": "What is transfer learning?",
        "options": [
            "Reusing a model or learned representations from one task as a starting point for another",
            "Moving a model file between folders without training",
            "Changing a test label after evaluation",
            "Training only on random noise",
        ],
        "correct_option": 0,
        "explanation": "Transfer learning reuses pretrained parameters or representations and adapts them to a target task.",
    },
    {
        "prompt": "What is a common benefit of freezing pretrained layers initially?",
        "options": [
            "Reduce trainable parameters and preserve learned features while training a new head",
            "Guarantee the pretrained model is optimal for every task",
            "Make the test set part of the training data",
            "Remove the need for a validation set",
        ],
        "correct_option": 0,
        "explanation": "Freezing layers can reduce compute and limit changes to pretrained representations while a task-specific head is trained.",
    },
    {
        "prompt": "In PyTorch, what is a suitable inference pattern for a trained model?",
        "options": [
            "Call `model.eval()` and use `torch.inference_mode()` around inference",
            "Call `model.train()` and always calculate gradients",
            "Call `optimizer.step()` for each prediction",
            "Fit the model again on the test labels",
        ],
        "correct_option": 0,
        "explanation": "Evaluation mode changes modules such as dropout and batch normalization; inference_mode disables autograd bookkeeping.",
    },
    {
        "prompt": "Why should model selection use validation data rather than the final test set?",
        "options": [
            "Repeated test-set selection leaks information and biases the final performance estimate",
            "The test set cannot contain labels",
            "Validation data always has more examples",
            "The test set is only for training neural networks",
        ],
        "correct_option": 0,
        "explanation": "Repeatedly selecting models based on test results adapts development to the test set; reserve it for final evaluation.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="deep-learning",
            defaults={"name": "Deep Learning", "icon": "brain", "order": 80, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="deep-learning-fundamentals-quiz",
            defaults={
                "title": "Deep Learning Fundamentals Quiz",
                "description": "20 questions covering neural network training, CNNs, sequence models, Transformers, regularization, and inference.",
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