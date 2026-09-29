from django.contrib import admin


class PublishAdminMixin:
    """Adds bulk Publish / Unpublish actions to any admin whose model has `is_published`."""

    actions = ["publish", "unpublish"]

    @admin.action(description="Publish selected items")
    def publish(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} item(s) published.")

    @admin.action(description="Unpublish selected items")
    def unpublish(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} item(s) unpublished.")
