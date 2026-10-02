"""Seed the CSS category and its 20-question fundamentals quiz.

Usage: python seed_quiz_css.py (run from backend/, same venv as manage.py)
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
        "prompt": "Which selector has the highest specificity among these choices?",
        "options": ["`#panel`", "`.panel`", "`section`", "`*`"],
        "correct_option": 0,
        "explanation": "An ID selector has a higher specificity category than a class, type, or universal selector, subject to cascade origin, importance, and layers.",
    },
    {
        "prompt": "Which selector component contributes to the class/attribute/pseudo-class specificity category?",
        "options": ["`.card`", "`#card`", "`article`", "`::before`"],
        "correct_option": 0,
        "explanation": "Class selectors, attribute selectors, and pseudo-classes contribute to the middle specificity category.",
    },
    {
        "prompt": "What does `box-sizing: border-box` include in an element's declared width?",
        "options": ["Content, padding, and border", "Content and margin only", "Margin and border only", "Content only"],
        "correct_option": 0,
        "explanation": "With border-box sizing, the declared width includes content, padding, and border; margin remains outside.",
    },
    {
        "prompt": "In a Flexbox row, which axis does `justify-content` distribute items along?",
        "options": ["The main axis", "The cross axis only", "The z-axis", "The viewport axis"],
        "correct_option": 0,
        "explanation": "`justify-content` operates along the main axis, whose direction depends on `flex-direction`.",
    },
    {
        "prompt": "Which CSS layout system is designed to arrange items in rows and columns together?",
        "options": ["CSS Grid", "Float layout only", "Inline formatting only", "The cascade"],
        "correct_option": 0,
        "explanation": "Grid is a two-dimensional layout system that manages rows and columns; Flexbox primarily arranges items along one axis.",
    },
    {
        "prompt": "What does the `fr` unit represent in CSS Grid?",
        "options": [
            "A share of available grid space after other sizing contributions",
            "A fixed number of pixels",
            "The root font size",
            "A percentage of the viewport height only",
        ],
        "correct_option": 0,
        "explanation": "An `fr` track receives a fraction of the available space after fixed and intrinsic sizing contributions are considered.",
    },
    {
        "prompt": "What does `position: sticky` generally do?",
        "options": [
            "Keeps the element in normal flow, then sticks relative to its scroll container after an inset threshold",
            "Removes the element from normal flow and fixes it to the viewport in every case",
            "Positions the element relative to the mouse pointer",
            "Prevents the element from scrolling at all",
        ],
        "correct_option": 0,
        "explanation": "Sticky positioning retains normal-flow space and sticks within its scroll container after reaching its inset threshold.",
    },
    {
        "prompt": "What does `display: none` do to an element's layout?",
        "options": [
            "Removes it from layout",
            "Hides it but always reserves its original space",
            "Moves it behind every other element",
            "Makes it transparent while preserving its box",
        ],
        "correct_option": 0,
        "explanation": "`display: none` means the element generates no layout box; `visibility: hidden` generally retains layout space.",
    },
    {
        "prompt": "Which statement about CSS inheritance is generally true?",
        "options": [
            "Text properties such as `color` commonly inherit, while many box properties do not",
            "Every CSS property always inherits",
            "No CSS property can inherit",
            "Only width and margin inherit by default",
        ],
        "correct_option": 0,
        "explanation": "Inheritance is property-specific; many text-related properties inherit, while layout and box properties commonly do not.",
    },
    {
        "prompt": "What is `1rem` relative to by default?",
        "options": ["The root element's computed font size", "The current element's width", "The viewport height", "The parent element's margin"],
        "correct_option": 0,
        "explanation": "The `rem` unit is relative to the computed font size of the root element.",
    },
    {
        "prompt": "What can a media query respond to?",
        "options": [
            "Environment features such as viewport width or reduced-motion preference",
            "Only the number of child elements in a container",
            "Only the value of a JavaScript variable",
            "Only a server's database schema",
        ],
        "correct_option": 0,
        "explanation": "Media queries test media or environment features, including viewport dimensions and user preferences.",
    },
    {
        "prompt": "What does a CSS container query respond to?",
        "options": [
            "The size or style of a designated ancestor container",
            "The browser's URL path only",
            "The number of pixels in a PNG file",
            "The text content of any sibling element by default",
        ],
        "correct_option": 0,
        "explanation": "Container queries let styles respond to a designated container's size or supported style conditions.",
    },
    {
        "prompt": "How are CSS custom properties commonly consumed?",
        "options": ["With `var(--token)`", "With `@include(--token)`", "With `#token()`", "With `envvar(--token)`"],
        "correct_option": 0,
        "explanation": "Custom properties are referenced with `var(--name)` and inherit through the element tree unless overridden.",
    },
    {
        "prompt": "What is one use of `minmax(0, 1fr)` in a Grid track?",
        "options": [
            "Allow the track to shrink below its min-content contribution while sharing available space",
            "Force the track to be exactly zero pixels",
            "Make the track larger than the viewport in every case",
            "Set the root font size to one pixel",
        ],
        "correct_option": 0,
        "explanation": "A zero minimum can prevent intrinsic min-content sizing from forcing a track wider than its available space.",
    },
    {
        "prompt": "What does `:focus-visible` help style?",
        "options": [
            "A focus indicator when the browser determines a visible focus cue is appropriate",
            "An element only when it is the first child",
            "Every hovered element on a touch screen",
            "A control only after it has been submitted",
        ],
        "correct_option": 0,
        "explanation": "`:focus-visible` supports visible focus styling, commonly for keyboard interaction, based on browser heuristics.",
    },
    {
        "prompt": "How should a stylesheet respond to `prefers-reduced-motion: reduce`?",
        "options": [
            "Reduce or remove nonessential motion while keeping state changes understandable",
            "Add more animated transitions",
            "Disable all keyboard focus indicators",
            "Hide all page content",
        ],
        "correct_option": 0,
        "explanation": "Respect the user's reduced-motion preference by reducing nonessential animation and preserving clear feedback.",
    },
    {
        "prompt": "What can a CSS transform do to stacking behavior?",
        "options": [
            "Create a new stacking context",
            "Remove all child elements from layout",
            "Change a media query into a container query",
            "Make every child position fixed",
        ],
        "correct_option": 0,
        "explanation": "A transform is one property that creates a stacking context, affecting how descendant `z-index` values are compared.",
    },
    {
        "prompt": "What does a mobile-first media query commonly use to add wider-screen styles?",
        "options": ["`min-width`", "`max-height` only", "`orientation: portrait` only", "`resolution: 0dpi`"],
        "correct_option": 0,
        "explanation": "Mobile-first styles establish a base layout and commonly add enhancements with `min-width` breakpoints.",
    },
    {
        "prompt": "What does `object-fit: cover` do to replaced content such as an image?",
        "options": [
            "Fills its box while preserving aspect ratio, cropping excess content if needed",
            "Stretches content to fill without preserving aspect ratio",
            "Hides the image unless it is square",
            "Changes the image's actual file dimensions",
        ],
        "correct_option": 0,
        "explanation": "`object-fit: cover` preserves aspect ratio while filling the content box, cropping where necessary.",
    },
    {
        "prompt": "What is a main accessibility benefit of a visible keyboard focus style?",
        "options": [
            "It shows keyboard users which interactive element currently has focus",
            "It automatically labels every form field",
            "It replaces semantic HTML",
            "It prevents all color-contrast problems",
        ],
        "correct_option": 0,
        "explanation": "A clear focus indicator helps keyboard users track where interactions will apply.",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="css",
            defaults={"name": "CSS", "icon": "code", "order": 130, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save(update_fields=["is_published"])

        quiz, _ = Quiz.objects.get_or_create(
            slug="css-fundamentals-quiz",
            defaults={
                "title": "CSS Fundamentals Quiz",
                "description": "20 questions covering the cascade, Flexbox, Grid, responsive design, accessibility, and visual behavior.",
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