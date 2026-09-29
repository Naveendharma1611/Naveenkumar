import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublishableModel, SluggedModel, TimeStampedModel
from apps.learning.models import StudyCategory


class Quiz(SluggedModel, PublishableModel):
    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        StudyCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="quizzes"
    )
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)
    time_limit_minutes = models.PositiveSmallIntegerField(default=10, help_text="0 = no time limit")
    show_leaderboard = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title


def normalize_answer(value: str) -> str:
    return re.sub(r"\s+", " ", str(value)).strip().rstrip(";").lower()


class QuizQuestion(TimeStampedModel):
    class Type(models.TextChoices):
        MCQ = "MCQ", "Multiple choice"
        CODING = "CODING", "Coding"
        OUTPUT = "OUTPUT", "Output prediction"
        SQL = "SQL", "SQL query"
        DEBUGGING = "DEBUGGING", "Debugging"
        THEORY = "THEORY", "Theory"

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.MCQ)
    prompt = models.TextField(help_text="Markdown")
    code = models.TextField(blank=True, help_text="Code shown with the question")
    code_language = models.CharField(max_length=30, default="python")
    options = models.JSONField(default=list, blank=True, help_text='MCQ options, e.g. ["list", "tuple", "dict"]')
    correct_option = models.PositiveSmallIntegerField(null=True, blank=True, help_text="0-based index for MCQ")
    accepted_answers = models.JSONField(
        default=list, blank=True, help_text="Accepted text answers (case/whitespace-insensitive). Empty = self-review."
    )
    explanation = models.TextField(blank=True, help_text="Markdown")
    points = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.prompt[:80]

    @property
    def is_auto_graded(self) -> bool:
        return self.type == self.Type.MCQ or bool(self.accepted_answers)

    def clean(self):
        if self.type == self.Type.MCQ:
            if not isinstance(self.options, list) or len(self.options) < 2:
                raise ValidationError({"options": "MCQ needs at least two options."})
            if self.correct_option is None or self.correct_option >= len(self.options):
                raise ValidationError({"correct_option": "Pick a valid option index."})

    def grade(self, answer) -> bool | None:
        """True/False when auto-gradable, None when the student should self-review."""
        if answer in (None, ""):
            return False if self.is_auto_graded else None
        if self.type == self.Type.MCQ:
            try:
                return int(answer) == self.correct_option
            except (TypeError, ValueError):
                return False
        if not self.accepted_answers:
            return None
        return normalize_answer(answer) in {normalize_answer(a) for a in self.accepted_answers}


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    answers = models.JSONField(default=dict, blank=True)
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    percent = models.PositiveSmallIntegerField(default=0)
    timed_out = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]
        indexes = [models.Index(fields=["quiz", "-percent"])]

    def __str__(self):
        return f"{self.user} - {self.quiz} ({self.percent}%)"
