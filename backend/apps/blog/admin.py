from django.contrib import admin

from apps.core.admin import PublishAdminMixin

from .models import BlogCategory, BlogPost, Tag


@admin.register(BlogPost)
class BlogPostAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["title", "category", "is_published", "is_featured", "published_at"]
    list_editable = ["is_published", "is_featured"]
    list_filter = ["category", "tags", "is_published", "is_featured"]
    search_fields = ["title", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    readonly_fields = ["published_at"]

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
