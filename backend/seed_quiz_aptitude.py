"""Seed the Aptitude category and its 20-question fundamentals quiz.

Usage: python seed_quiz_aptitude.py (run from backend/, same venv as manage.py)
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
        "prompt": "What is 15% of 240?",
        "options": ["24", "30", "36", "40"],
        "correct_option": 2,
        "explanation": "10% of 240 is 24 and 5% is 12, so 15% is 36.",
    },
    {
        "prompt": "An item costs 800 and sells for 920. What is the profit percentage on cost?",
        "options": ["12%", "15%", "18%", "20%"],
        "correct_option": 1,
        "explanation": "Profit is 120; 120 divided by the cost 800 is 15%.",
    },
    {
        "prompt": "A total of 100 is divided in the ratio 2:3. What is the smaller share?",
        "options": ["20", "40", "50", "60"],
        "correct_option": 1,
        "explanation": "There are 5 parts, so each is 20; the smaller share is 2 × 20 = 40.",
    },
    {
        "prompt": "The mean of 12, 15, 17, and x is 16. What is x?",
        "options": ["18", "20", "22", "24"],
        "correct_option": 1,
        "explanation": "The total must be 4 × 16 = 64; the known values sum to 44, so x = 20.",
    },
    {
        "prompt": "Worker A finishes a job in 8 days and worker B in 12 days. How long do they take together at constant rates?",
        "options": ["4 days", "4.8 days", "5 days", "6 days"],
        "correct_option": 1,
        "explanation": "Their combined rate is 1/8 + 1/12 = 5/24 job per day, so the time is 24/5 = 4.8 days.",
    },
    {
        "prompt": "A vehicle travels 150 km in 2.5 hours at a constant speed. What is its speed?",
        "options": ["50 km/h", "55 km/h", "60 km/h", "65 km/h"],
        "correct_option": 2,
        "explanation": "Speed is distance divided by time: 150 / 2.5 = 60 km/h.",
    },
    {
        "prompt": "What is the simple interest on 5,000 at 4% per year for 2 years?",
        "options": ["200", "300", "400", "500"],
        "correct_option": 2,
        "explanation": "Simple interest is P × r × t / 100 = 5000 × 4 × 2 / 100 = 400.",
    },
    {
        "prompt": "What is the HCF of 24 and 36?",
        "options": ["6", "8", "12", "18"],
        "correct_option": 2,
        "explanation": "12 is the greatest positive integer that divides both 24 and 36.",
    },
    {
        "prompt": "What is the next term: 2, 6, 12, 20, 30, __?",
        "options": ["36", "40", "42", "44"],
        "correct_option": 2,
        "explanation": "The differences are 4, 6, 8, 10, so the next difference is 12 and the next term is 42.",
    },
    {
        "prompt": "All analysts are readers. No readers are careless. Which conclusion must follow?",
        "options": [
            "Some analysts are careless",
            "No analysts are careless",
            "All readers are analysts",
            "Some careless people are readers",
        ],
        "correct_option": 1,
        "explanation": "Analysts are a subset of readers, and readers are disjoint from careless people; therefore analysts are not careless.",
    },
    {
        "prompt": "A person walks 3 km east, then 4 km north. How far are they from the starting point in a straight line?",
        "options": ["4 km", "5 km", "6 km", "7 km"],
        "correct_option": 1,
        "explanation": "The displacement forms a right triangle with legs 3 and 4; the hypotenuse is 5 km.",
    },
    {
        "prompt": "If x + y = 12 and x − y = 4, what is x?",
        "options": ["4", "6", "8", "10"],
        "correct_option": 2,
        "explanation": "Adding the equations gives 2x = 16, so x = 8.",
    },
    {
        "prompt": "How many ways can 3 people be selected from 5 distinct people when order does not matter?",
        "options": ["10", "15", "30", "60"],
        "correct_option": 0,
        "explanation": "The number is 5 choose 3 = 5 × 4 × 3 / (3 × 2 × 1) = 10.",
    },
    {
        "prompt": "Two fair six-sided dice are rolled. What is the probability their sum is 7?",
        "options": ["1/12", "1/9", "1/6", "1/4"],
        "correct_option": 2,
        "explanation": "Six of the 36 equally likely ordered outcomes sum to 7, so the probability is 6/36 = 1/6.",
    },
    {
        "prompt": "Four people sit in a row. How many different orders are possible?",
        "options": ["12", "16", "24", "36"],
        "correct_option": 2,
        "explanation": "The number of orders is 4! = 4 × 3 × 2 × 1 = 24.",
    },
    {
        "prompt": "Choose the grammatically correct sentence.",
        "options": [
            "Each of the reports are ready.",
            "Each of the reports is ready.",
            "Each reports is ready.",
            "Each of reports are ready.",
        ],
        "correct_option": 1,
        "explanation": "The subject `each` is singular, so it takes the singular verb `is`.",
    },
    {
        "prompt": "Choose the sentence with parallel list structure.",
        "options": [
            "She enjoys reading, to swim, and cycling.",
            "She enjoys reading, swimming, and cycling.",
            "She enjoys to read, swimming, and to cycle.",
            "She enjoys read, swim, and cycling.",
        ],
        "correct_option": 1,
        "explanation": "Each item uses the same gerund form: reading, swimming, and cycling.",
    },
    {
        "prompt": "A pilot program improved results in two schools. Which conclusion is best supported?",
        "options": [
            "The program will work in every school.",
            "The result is promising in the tested settings but needs broader evidence.",
            "The program caused every improvement.",
            "The program should replace every existing program immediately.",
        ],
        "correct_option": 1,
        "explanation": "The evidence supports a limited conclusion about the tested settings, not universal effectiveness or proven causation.",
    },
    {
        "prompt": "A report says revenue rose from 80 to 100. What was the percentage increase relative to the original value?",
        "options": ["20%", "25%", "80%", "125%"],
        "correct_option": 1,
        "explanation": "The increase is 20; 20 divided by the original 80 is 25%.",
    },
    {
        "prompt": "An argument claims a new bus route reduced commute times because average times fell afterward. Which evidence most directly strengthens a causal interpretation?",
        "options": [
            "A comparable route without the change had no similar decrease over the same period.",
            "The new buses are painted blue.",
            "The route map uses a larger font.",
            "More people own bicycles in another city.",
        ],
        "correct_option": 0,
        "explanation": "A comparable control helps distinguish the route's effect from broader time trends or unrelated changes.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="aptitude",
            defaults={"name": "Aptitude", "icon": "brain", "order": 27, "is_published": True},
        )
        if category.name != "Aptitude" or not category.is_published:
            category.name = "Aptitude"
            category.is_published = True
            category.save(update_fields=["name", "is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="aptitude-fundamentals-quiz",
            defaults={
                "title": "Aptitude Fundamentals Quiz",
                "description": "20 questions across quantitative, logical, and verbal reasoning.",
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