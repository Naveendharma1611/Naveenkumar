import math

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import PublishableModel, SluggedModel
from apps.core.validators import image_validators


class BlogCategory(SluggedModel):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Blog categories"

    def __str__(self):
        return self.name


class Tag(SluggedModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPost(SluggedModel, PublishableModel):
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField(help_text="Markdown")
    featured_image = models.ImageField(upload_to="blog/", blank=True, validators=image_validators)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def reading_minutes(self) -> int:
        return max(1, math.ceil(len(self.content.split()) / 200))

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
