from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import image_validators, pdf_validators


class SiteProfile(TimeStampedModel):
    """Singleton holding the site owner's personal info. Edit it in the admin; nothing is hardcoded."""

    full_name = models.CharField(max_length=150, default="Naveenkumar")
    headline = models.CharField(max_length=200, default="AI / Data Science / Python Developer")
    tagline = models.TextField(
        default="I build intelligent applications, machine learning solutions, "
        "data-driven systems, and modern web applications."
    )
    short_bio = models.TextField(blank=True)
    about = models.TextField(blank=True, help_text="Markdown")
    career_objective = models.TextField(blank=True)
    technical_interests = models.TextField(blank=True, help_text="One per line")
    current_learning = models.TextField(blank=True, help_text="One per line")
    professional_goals = models.TextField(blank=True)
    hero_badges = models.CharField(
        max_length=300,
        default="Python,Machine Learning,Deep Learning,Data Science,SQL,Django,GenAI",
        help_text="Comma separated",
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    photo = models.ImageField(upload_to="profile/", blank=True, validators=image_validators)
    resume_pdf = models.FileField(upload_to="resume/", blank=True, validators=pdf_validators)

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return self.full_name

    def clean(self):
        if not self.pk and SiteProfile.objects.exists():
            raise ValidationError("Only one site profile can exist. Edit the existing one.")

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Skill(TimeStampedModel):
    class Category(models.TextChoices):
        PROGRAMMING = "PROGRAMMING", "Programming"
        DATA_SCIENCE = "DATA_SCIENCE", "Data Science"
        MACHINE_LEARNING = "MACHINE_LEARNING", "Machine Learning"
        DEEP_LEARNING = "DEEP_LEARNING", "Deep Learning"
        DATABASE = "DATABASE", "Database"
        WEB = "WEB", "Web Development"
        ANALYTICS = "ANALYTICS", "Data Analytics"
        GENAI = "GENAI", "Generative AI"
        AGENTIC_AI = "AGENTIC_AI", "Agentic AI"
        TOOLS = "TOOLS", "Tools & Cloud"

    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    description = models.TextField(blank=True)
    # Admin-controlled label (e.g. "Learning", "Comfortable", "Proficient"); never auto-assigned.
    proficiency_label = models.CharField(max_length=40, blank=True)
    proficiency_percent = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Optional 0-100")
    icon = models.CharField(max_length=60, blank=True, help_text="Icon key, e.g. python, database, brain")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "order", "name"]
        unique_together = [("name", "category")]

    def __str__(self):
        return self.name


class Education(TimeStampedModel):
    degree = models.CharField(max_length=150)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    start_year = models.PositiveSmallIntegerField(null=True, blank=True)
    end_year = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Leave blank if ongoing")
    score = models.CharField(max_length=40, blank=True, help_text="Percentage or CGPA")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-end_year"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(TimeStampedModel):
    class Type(models.TextChoices):
        JOB = "JOB", "Job"
        INTERNSHIP = "INTERNSHIP", "Internship"
        FREELANCE = "FREELANCE", "Freelance"
        VOLUNTEER = "VOLUNTEER", "Volunteer"

    role = models.CharField(max_length=150)
    organization = models.CharField(max_length=200)
    type = models.CharField(max_length=15, choices=Type.choices, default=Type.JOB)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(null=True, blank=True, help_text="Leave blank if unknown")
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if current")
    description = models.TextField(blank=True, help_text="Markdown; use bullet points for responsibilities")
    technologies = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.organization}"


class Achievement(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date"]

    def __str__(self):
        return self.title
