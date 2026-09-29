from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from apps.core.models import PublishableModel, SluggedModel, TimeStampedModel
from apps.core.validators import image_validators, study_file_validators


class StudyCategory(SluggedModel, TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=60, blank=True, help_text="Icon key, e.g. python, database, brain")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Study categories"

    def __str__(self):
        return self.name


class Level(models.TextChoices):
    BEGINNER = "BEGINNER", "Beginner"
    INTERMEDIATE = "INTERMEDIATE", "Intermediate"
    ADVANCED = "ADVANCED", "Advanced"
    INTERVIEW = "INTERVIEW", "Interview Preparation"
    PROJECTS = "PROJECTS", "Projects"
    PRACTICE = "PRACTICE", "Practice Questions"


class Course(SluggedModel, PublishableModel):
    """A track inside a category, e.g. 'Python - Beginner'."""

    category = models.ForeignKey(StudyCategory, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=15, choices=Level.choices, default=Level.BEGINNER, db_index=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="courses/", blank=True, validators=image_validators)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "title"]

    def __str__(self):
        return f"{self.category} / {self.title}"


class Lesson(PublishableModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    # Denormalised from course so URLs can be /study-materials/<category>/<lesson>.
    category = models.ForeignKey(StudyCategory, on_delete=models.CASCADE, related_name="lessons", editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    summary = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True, help_text="Markdown: headings, tables, code blocks, images")
    video_url = models.URLField(blank=True)
    estimated_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["course", "order", "id"]
        constraints = [models.UniqueConstraint(fields=["category", "slug"], name="unique_lesson_slug_per_category")]
        indexes = [models.Index(fields=["course", "order"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.category_id = self.course.category_id
        if not self.slug:
            base = slugify(self.title)[:200] or "lesson"
            slug, n = base, 2
            while Lesson.objects.filter(category_id=self.category_id, slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class StudyMaterial(TimeStampedModel):
    class Kind(models.TextChoices):
        PDF = "PDF", "PDF"
        NOTES = "NOTES", "Notes"
        CODE = "CODE", "Code"
        VIDEO = "VIDEO", "Video"
        SLIDES = "SLIDES", "Slides"
        DATASET = "DATASET", "Dataset"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=200)
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.PDF)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials", null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="materials", null=True, blank=True)
    file = models.FileField(upload_to="study/", blank=True, validators=study_file_validators)
    external_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_downloadable = models.BooleanField(default=True)
    requires_login = models.BooleanField(default=False, help_text="Only logged-in users see the download link")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def clean(self):
        if not self.course and not self.lesson:
            raise ValidationError("Attach the material to a course or a lesson.")
        if not self.file and not self.external_url:
            raise ValidationError("Upload a file or provide an external URL.")


class InterviewQuestion(PublishableModel):
    class Difficulty(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"

    category = models.ForeignKey(StudyCategory, on_delete=models.CASCADE, related_name="interview_questions")
    question = models.TextField()
    short_answer = models.TextField()
    detailed_answer = models.TextField(blank=True, help_text="Markdown")
    example = models.TextField(blank=True, help_text="Markdown")
    code = models.TextField(blank=True)
    code_language = models.CharField(max_length=30, default="python")
    interview_tip = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY, db_index=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "id"]

    def __str__(self):
        return self.question[:80]


class Bookmark(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="bookmarks")

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["user", "lesson"], name="unique_bookmark")]


class Progress(TimeStampedModel):
    """One row per completed lesson."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Progress"
        constraints = [models.UniqueConstraint(fields=["user", "lesson"], name="unique_progress")]


class LessonNote(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_notes")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField(max_length=20000, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "lesson"], name="unique_lesson_note")]
