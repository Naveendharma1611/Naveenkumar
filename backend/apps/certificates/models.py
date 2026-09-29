from django.db import models

from apps.core.models import PublishableModel
from apps.core.validators import image_validators, pdf_validators


class Certificate(PublishableModel):
    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=150)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(
        max_length=100, unique=True, help_text="Used in the verification URL: /certificate/<credential_id>"
    )
    credential_url = models.URLField(blank=True, help_text="Official verification link from the provider")
    image = models.ImageField(upload_to="certificates/", blank=True, validators=image_validators)
    pdf = models.FileField(upload_to="certificates/pdf/", blank=True, validators=pdf_validators)
    description = models.TextField(blank=True)
    skills = models.CharField(max_length=300, blank=True, help_text="Comma separated")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-issue_date"]

    def __str__(self):
        return f"{self.name} ({self.provider})"
