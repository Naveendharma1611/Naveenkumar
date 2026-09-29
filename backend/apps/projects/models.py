from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import PublishableModel, SluggedModel, TimeStampedModel
from apps.core.validators import image_validators, model_3d_validators, pdf_validators, video_validators


class Technology(SluggedModel):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


class Project(SluggedModel, PublishableModel):
    class Category(models.TextChoices):
        PYTHON = "PYTHON", "Python"
        DATA_SCIENCE = "DATA_SCIENCE", "Data Science"
        ML = "ML", "Machine Learning"
        DL = "DL", "Deep Learning"
        AI = "AI", "AI"
        GENAI = "GENAI", "GenAI"
        DJANGO = "DJANGO", "Django"
        ANALYTICS = "ANALYTICS", "Data Analytics"
        WEB = "WEB", "Web Development"

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    summary = models.CharField(max_length=300, help_text="Short description shown on cards")
    cover_image = models.ImageField(upload_to="projects/covers/", blank=True, validators=image_validators)
    technologies = models.ManyToManyField(Technology, related_name="projects", blank=True)

    # Detail sections (Markdown). Empty sections are hidden on the site.
    problem_statement = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    dataset = models.TextField(blank=True)
    architecture = models.TextField(blank=True)
    data_flow = models.TextField(blank=True)
    implementation = models.TextField(blank=True)
    algorithm = models.TextField(blank=True, verbose_name="Machine learning algorithm")
    model_training = models.TextField(blank=True)
    evaluation = models.TextField(blank=True)
    results = models.TextField(blank=True)
    future_improvements = models.TextField(blank=True)
    documentation = models.TextField(blank=True)

    pipeline_steps = models.JSONField(
        default=list,
        blank=True,
        help_text='Ordered steps for the architecture diagram, e.g. ["Dataset", "Data Cleaning", "EDA"]',
    )
    documentation_pdf = models.FileField(upload_to="projects/docs/", blank=True, validators=pdf_validators)
    model_3d = models.FileField(
        upload_to="projects/models/", blank=True, validators=model_3d_validators, help_text="Optional GLB/GLTF/OBJ"
    )
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    demo_video_url = models.URLField(blank=True, help_text="YouTube/Vimeo or direct video URL")

    is_featured = models.BooleanField(default=False, db_index=True)
    is_sample = models.BooleanField(default=False, help_text="Marks demo content to be replaced")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]
        indexes = [models.Index(fields=["is_published", "category"])]

    def __str__(self):
        return self.title

    def clean(self):
        steps = self.pipeline_steps
        if not isinstance(steps, list) or not all(isinstance(s, str) for s in steps):
            raise ValidationError({"pipeline_steps": "Must be a list of step names."})


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/screenshots/", validators=image_validators)
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


class ProjectVideo(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=200, blank=True)
    video = models.FileField(upload_to="projects/videos/", blank=True, validators=video_validators)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def clean(self):
        if not self.video and not self.url:
            raise ValidationError("Upload a video file or provide a URL.")


class ProjectCodeSnippet(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="code_snippets")
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=30, default="python")
    code = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
