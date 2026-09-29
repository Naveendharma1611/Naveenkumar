from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishableModel(TimeStampedModel):
    is_published = models.BooleanField(default=False, db_index=True)

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True


class SluggedModel(models.Model):
    """Fills `slug` from `title` (or `name`) on first save, keeping it unique."""

    slug = models.SlugField(max_length=220, unique=True, blank=True)

    class Meta:
        abstract = True

    def slug_source(self) -> str:
        return getattr(self, "title", None) or getattr(self, "name", "")

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.slug_source())[:200] or "item"
            slug, n = base, 2
            while type(self).objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
