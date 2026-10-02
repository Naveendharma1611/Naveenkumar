# -*- coding: utf-8 -*-
"""Seeds the StudyCategory (if missing) and a 20-question MCQ quiz for HTML.

Usage: python seed_quiz_html.py   (run from backend/, same venv as manage.py)
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
        "prompt": "Which tag must be the very first line of every HTML5 document?",
        "options": ["<html>", "<!DOCTYPE html>", "<head>", "<meta charset=\"utf-8\">"],
        "correct_option": 1,
        "explanation": "`<!DOCTYPE html>` tells the browser to render in standards mode rather than quirks mode.",
    },
    {
        "prompt": "Which element is the correct semantic choice for a page's main navigation links?",
        "options": ["<div class=\"nav\">", "<nav>", "<section>", "<menu>"],
        "correct_option": 1,
        "explanation": "`<nav>` is the dedicated semantic landmark for primary navigation, improving accessibility and SEO.",
    },
    {
        "prompt": "What is the main difference between `<div>` and `<span>`?",
        "options": [
            "<div> is inline, <span> is block-level",
            "<div> is block-level, <span> is inline",
            "They are identical in every way",
            "<span> can only hold text, <div> cannot",
        ],
        "correct_option": 1,
        "explanation": "<div> is a block-level generic container; <span> is an inline generic container used within text flow.",
    },
    {
        "prompt": "Which attribute makes an <img> accessible to screen readers and is required for meaningful images?",
        "options": ["title", "alt", "longdesc", "aria-label"],
        "correct_option": 1,
        "explanation": "`alt` provides a text alternative read by screen readers and shown if the image fails to load.",
    },
    {
        "prompt": "What does the `required` attribute do on a form input?",
        "options": [
            "Hides the field until filled",
            "Prevents form submission until the field has a value",
            "Auto-fills the field with a default value",
            "Makes the field read-only",
        ],
        "correct_option": 1,
        "explanation": "`required` triggers built-in HTML5 validation, blocking submission until the field is filled.",
    },
    {
        "prompt": "Which HTML element correctly associates a label with a specific input for accessibility?",
        "options": [
            "<label name=\"email\">",
            "<label for=\"email\"> paired with <input id=\"email\">",
            "<label input=\"email\">",
            "Labels don't need to be associated with inputs",
        ],
        "correct_option": 1,
        "explanation": "The label's `for` attribute must match the input's `id` so clicking the label focuses the input, and screen readers announce it correctly.",
    },
    {
        "prompt": "What is the purpose of `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">`?",
        "options": [
            "It sets the page's title in search results",
            "It controls how the page scales on mobile devices for responsive design",
            "It loads a responsive CSS framework",
            "It blocks zooming entirely",
        ],
        "correct_option": 1,
        "explanation": "This meta tag tells mobile browsers to match the viewport width to the device width, the foundation of responsive design.",
    },
    {
        "prompt": "Which script loading attribute downloads the script in parallel with HTML parsing and executes it only after parsing completes, in document order?",
        "options": ["async", "defer", "sync", "preload"],
        "correct_option": 1,
        "explanation": "`defer` scripts run in order after the HTML is fully parsed; `async` scripts run as soon as they finish downloading, potentially out of order.",
    },
    {
        "prompt": "Which element represents a self-contained piece of content that could be distributed independently, like a blog post?",
        "options": ["<section>", "<article>", "<aside>", "<div>"],
        "correct_option": 1,
        "explanation": "<article> is for independent, reusable content; <section> groups thematically related content within a page that isn't necessarily standalone.",
    },
    {
        "prompt": "What does an HTTP form with `method=\"GET\"` do with its field data?",
        "options": [
            "Sends it in the request body, hidden from the URL",
            "Appends it as a query string in the URL",
            "Encrypts it automatically",
            "Discards it after submission",
        ],
        "correct_option": 1,
        "explanation": "GET appends form data as URL query parameters (visible, bookmarkable, size-limited); POST sends it in the request body instead.",
    },
    {
        "prompt": "Which input type provides built-in email format validation without JavaScript?",
        "options": ["type=\"text\"", "type=\"email\"", "type=\"mail\"", "type=\"string\""],
        "correct_option": 1,
        "explanation": "`type=\"email\"` triggers the browser's built-in format validation and often shows an email-optimized mobile keyboard.",
    },
    {
        "prompt": "What is the correct way to include a responsive image that serves different file sizes based on viewport?",
        "options": [
            "<img src=\"a.jpg\" responsive>",
            "<img srcset=\"a-480.jpg 480w, a-800.jpg 800w\" sizes=\"...\" src=\"a-800.jpg\">",
            "<img scale=\"auto\" src=\"a.jpg\">",
            "CSS media queries only, HTML cannot do this",
        ],
        "correct_option": 1,
        "explanation": "`srcset` + `sizes` let the browser choose the most appropriate image file for the viewport and pixel density.",
    },
    {
        "prompt": "Which tag is used to embed a standalone HTML page inside another page?",
        "options": ["<embed>", "<iframe>", "<object>", "<frame>"],
        "correct_option": 1,
        "explanation": "<iframe> embeds another HTML document; it's useful for widgets/maps but should set `sandbox`/`loading` attributes carefully for security and performance.",
    },
    {
        "prompt": "What does the `alt=\"\"` (empty alt) attribute mean on an image?",
        "options": [
            "The image failed to load",
            "The image is purely decorative and should be skipped by screen readers",
            "It's a required placeholder with no real meaning",
            "It disables the image entirely",
        ],
        "correct_option": 1,
        "explanation": "An empty `alt=\"\"` explicitly marks an image as decorative, so assistive technology skips announcing it instead of reading the filename.",
    },
    {
        "prompt": "Which element should wrap the main, unique content of a page (used only once per page)?",
        "options": ["<main>", "<content>", "<body>", "<primary>"],
        "correct_option": 0,
        "explanation": "<main> marks the dominant, unique content of the document, distinct from repeated elements like headers/navigation/footers.",
    },
    {
        "prompt": "What is the effect of the `lazy` value on an <img> tag's `loading` attribute?",
        "options": [
            "The image loads before anything else on the page",
            "The browser defers loading the image until it's near the viewport",
            "It compresses the image automatically",
            "It disables the image on slow connections",
        ],
        "correct_option": 1,
        "explanation": "`loading=\"lazy\"` improves initial page load performance by deferring offscreen images until the user scrolls near them.",
    },
    {
        "prompt": "Which data-* style custom attribute usage is valid HTML5?",
        "options": [
            "<div custom-id=\"42\">",
            "<div data-id=\"42\">",
            "<div x-id=\"42\">",
            "Custom attributes aren't allowed in HTML5",
        ],
        "correct_option": 1,
        "explanation": "The `data-*` attribute prefix is the standard, validator-safe way to embed custom data readable via JavaScript's `dataset` API.",
    },
    {
        "prompt": "Which ARIA attribute is commonly used to give an accessible name to an interactive element with no visible text (like an icon-only button)?",
        "options": ["aria-hidden", "aria-label", "aria-disabled", "role"],
        "correct_option": 1,
        "explanation": "`aria-label` provides an accessible name announced by screen readers when there's no visible text label, e.g. an icon-only close button.",
    },
    {
        "prompt": "What happens to form data in an <input> field that has the `disabled` attribute when the form is submitted?",
        "options": [
            "It is submitted as an empty string",
            "It is NOT included in the submitted form data at all",
            "It is submitted with its last value before being disabled",
            "The whole form submission is blocked",
        ],
        "correct_option": 1,
        "explanation": "Disabled fields are excluded entirely from form submission, unlike `readonly` fields, which ARE still submitted.",
    },
    {
        "prompt": "Which tag correctly marks up a table header cell?",
        "options": ["<td header>", "<th>", "<head>", "<table-header>"],
        "correct_option": 1,
        "explanation": "<th> marks header cells (with an implicit bold/center style and an accessibility role distinct from <td> data cells).",
    },
]


def run():
    with transaction.atomic():
        category, _ = StudyCategory.objects.get_or_create(
            slug="html",
            defaults={"name": "HTML", "icon": "code", "order": 100, "is_published": True},
        )
        if not category.is_published:
            category.is_published = True
            category.save()

        quiz, _ = Quiz.objects.get_or_create(
            slug="html-fundamentals-quiz",
            defaults={
                "title": "HTML Fundamentals Quiz",
                "description": "20 questions covering semantics, accessibility, forms and performance basics.",
                "category": category,
                "difficulty": Quiz.Difficulty.EASY,
                "time_limit_minutes": 15,
                "show_leaderboard": True,
                "order": 1,
                "is_published": True,
            },
        )
        QuizQuestion.objects.filter(quiz=quiz, order__gt=len(QUESTIONS)).delete()
        for idx, q in enumerate(QUESTIONS, start=1):
            QuizQuestion.objects.update_or_create(
                quiz=quiz,
                order=idx,
                defaults={
                    "type": QuizQuestion.Type.MCQ,
                    "prompt": q["prompt"],
                    "options": q["options"],
                    "correct_option": q["correct_option"],
                    "explanation": q["explanation"],
                    "points": 1,
                },
            )

    print(f"Category: {category.slug} (published={category.is_published})")
    print(f"Quiz: {quiz.slug} — {quiz.questions.count()} questions")


if __name__ == "__main__":
    run()
