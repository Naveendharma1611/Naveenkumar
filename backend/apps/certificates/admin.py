from django.contrib import admin

from apps.core.admin import PublishAdminMixin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["name", "provider", "issue_date", "credential_id", "is_published", "order"]
    list_editable = ["is_published", "order"]
    list_filter = ["provider", "is_published"]
    search_fields = ["name", "provider", "credential_id"]
