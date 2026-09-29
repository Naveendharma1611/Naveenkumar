from django.contrib import admin

from apps.core.admin import PublishAdminMixin

from .models import Project, ProjectCodeSnippet, ProjectImage, ProjectVideo, Technology


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectVideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 0


class ProjectCodeSnippetInline(admin.StackedInline):
    model = ProjectCodeSnippet
    extra = 0


@admin.register(Project)
class ProjectAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["title", "category", "is_published", "is_featured", "is_sample", "order", "updated_at"]
    list_editable = ["is_published", "is_featured", "order"]
    list_filter = ["category", "is_published", "is_featured", "is_sample", "technologies"]
    search_fields = ["title", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["technologies"]
    inlines = [ProjectImageInline, ProjectVideoInline, ProjectCodeSnippetInline]
    fieldsets = (
        ("Card", {"fields": ("title", "slug", "category", "summary", "cover_image", "technologies")}),
        ("Links", {"fields": ("github_url", "live_demo_url", "demo_video_url")}),
        ("Overview", {"fields": ("problem_statement", "objective", "dataset")}),
        ("Architecture", {"fields": ("pipeline_steps", "architecture", "data_flow")}),
        ("Implementation", {"fields": ("implementation", "algorithm", "model_training")}),
        ("Results", {"fields": ("evaluation", "results", "future_improvements")}),
        ("Documentation & 3D", {"fields": ("documentation", "documentation_pdf", "model_3d")}),
        ("Publishing", {"fields": ("is_published", "is_featured", "is_sample", "order")}),
    )


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
