from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_read", "created_at"]
    list_editable = ["is_read"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message", "ip_address", "user_agent", "created_at"]

    def has_add_permission(self, request):
        return False
